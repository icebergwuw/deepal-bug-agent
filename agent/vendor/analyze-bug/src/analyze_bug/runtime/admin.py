import argparse
import getpass
import json
import os
import shutil
import subprocess
from pathlib import Path
from urllib import error, request

from analyze_bug import __version__
from analyze_bug.core.config import (
    DEFAULT_ALCHEMY_BASE_URL,
    config_status,
    load_config,
    migrate_legacy_config,
    upsert_config,
)
from analyze_bug.core.paths import (
    LEGACY_COMMAND_DIR,
    LEGACY_COMMAND_FILE,
    get_config_file,
    get_install_root,
    get_skill_dir,
    get_skill_dirs,
    get_legacy_skill_dirs,
    get_user_bin_dir,
    is_windows,
)
from analyze_bug.core.repo_locator import detect_online_dialogue_root
from analyze_bug.core.skills import render_skill


INSTALL_COPY_ITEMS = ["pyproject.toml", "uv.lock", "README.md", "src/resources"]
SOURCE_PACKAGES = ("analyze_bug",)
MCP_SERVERS = (
    ("jira-analyzer", "analyze-bug-jira-mcp"),
    ("debug-analyzer", "analyze-bug-debug-mcp"),
    ("rules-analyzer", "analyze-bug-rules-mcp"),
    ("alchemy-ops", "analyze-bug-ops-mcp"),
)
MCP_REMOVE_TIMEOUT_SECONDS = 10
MCP_REGISTER_TIMEOUT_SECONDS = 120
RegistrationResult = tuple[str, str | None]


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def find_uv() -> str | None:
    candidates = [
        shutil.which("uv"),
        str(Path.home() / ".local" / "bin" / ("uv.exe" if is_windows() else "uv")),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate).resolve())
    return None


def run_command(
    command: list[str],
    check: bool = True,
    quiet: bool = False,
    timeout: float | None = None,
) -> subprocess.CompletedProcess:
    kwargs = {"text": True}
    if quiet:
        kwargs["capture_output"] = True
    if timeout is not None:
        kwargs["timeout"] = timeout
    return subprocess.run(command, check=check, **kwargs)


def copy_runtime(source_root: Path, install_root: Path) -> None:
    source_root = source_root.resolve()
    install_root = install_root.resolve()
    if source_root == install_root:
        return

    staging_root = install_root.parent / f".{install_root.name}.staging"
    if staging_root.exists():
        shutil.rmtree(staging_root)
    staging_root.mkdir(parents=True, exist_ok=True)

    for relative in INSTALL_COPY_ITEMS:
        src = source_root / relative
        dest = staging_root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(
                src,
                dest,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.pyd"),
            )
        else:
            shutil.copy2(src, dest)

    (staging_root / "src").mkdir(parents=True, exist_ok=True)
    for package_name in SOURCE_PACKAGES:
        shutil.copytree(
            source_root / "src" / package_name,
            staging_root / "src" / package_name,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.pyd"),
        )

    if install_root.exists():
        shutil.rmtree(install_root)
    staging_root.rename(install_root)


def cleanup_previous_installation(install_root: Path) -> None:
    for platform in ("codex", "gemini"):
        for skill_dir in get_skill_dirs(platform) + get_legacy_skill_dirs(platform):
            if skill_dir.exists():
                shutil.rmtree(skill_dir)

    cleanup_legacy_gemini_command_install()

    wrapper_dir = get_user_bin_dir()
    for filename in ("analyze-bug-admin", "analyze-bug-admin.cmd"):
        wrapper = wrapper_dir / filename
        if wrapper.exists():
            wrapper.unlink()

    staging_root = install_root.parent / f".{install_root.name}.staging"
    if staging_root.exists():
        shutil.rmtree(staging_root)

    if install_root.exists():
        shutil.rmtree(install_root)


def write_admin_wrapper(uv_executable: str, install_root: Path) -> Path:
    bin_dir = get_user_bin_dir()
    bin_dir.mkdir(parents=True, exist_ok=True)

    if is_windows():
        wrapper = bin_dir / "analyze-bug-admin.cmd"
        content = (
            "@echo off\r\n"
            f"\"{uv_executable}\" run --project \"{install_root}\" analyze-bug-admin %*\r\n"
        )
        wrapper.write_text(content, encoding="utf-8")
    else:
        wrapper = bin_dir / "analyze-bug-admin"
        content = (
            "#!/bin/sh\n"
            f"exec \"{uv_executable}\" run --project \"{install_root}\" analyze-bug-admin \"$@\"\n"
        )
        wrapper.write_text(content, encoding="utf-8")
        os.chmod(wrapper, 0o755)
    return wrapper


def install_skill(source_root: Path, platform: str) -> Path:
    staged_skill = source_root / "skills" / platform / "analyze-bug" / "SKILL.md"
    content = staged_skill.read_text(encoding="utf-8") if staged_skill.exists() else render_skill(platform)

    primary_target = None
    for target_dir in get_skill_dirs(platform):
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "SKILL.md").write_text(content, encoding="utf-8")
        if primary_target is None:
            primary_target = target_dir
    return primary_target


def cleanup_legacy_gemini_command_install() -> None:
    if LEGACY_COMMAND_FILE.exists():
        LEGACY_COMMAND_FILE.unlink()
    if LEGACY_COMMAND_DIR.exists():
        shutil.rmtree(LEGACY_COMMAND_DIR)


def format_command_error(exc: subprocess.CalledProcessError) -> str:
    for value in (exc.stderr, exc.stdout):
        if value:
            text = value.strip()
            if text:
                return text
    return str(exc)


def format_timeout_error(exc: subprocess.TimeoutExpired) -> str:
    return f"命令执行超时（{exc.timeout:.0f}s）: {' '.join(exc.cmd)}"


def best_effort_cleanup_command(command: list[str]) -> None:
    try:
        run_command(
            command,
            check=False,
            quiet=True,
            timeout=MCP_REMOVE_TIMEOUT_SECONDS,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        # Removing stale registrations is a cleanup step only; it should never
        # block the main install flow.
        return


def register_codex_mcp(install_root: Path, uv_executable: str) -> RegistrationResult:
    codex = shutil.which("codex")
    if not codex:
        return "skip", None
    try:
        for name, entrypoint in MCP_SERVERS:
            best_effort_cleanup_command([codex, "mcp", "remove", name])
            print(f"正在注册 Codex MCP: {name}")
            run_command(
                [
                    codex,
                    "mcp",
                    "add",
                    name,
                    "--",
                uv_executable,
                "run",
                "--project",
                str(install_root),
                entrypoint,
                ],
                quiet=True,
                timeout=MCP_REGISTER_TIMEOUT_SECONDS,
            )
            print(f"已注册 Codex MCP: {name}")
    except subprocess.CalledProcessError as exc:
        return "warn", f"Codex MCP 注册失败: {format_command_error(exc)}"
    except subprocess.TimeoutExpired as exc:
        return "warn", f"Codex MCP 注册失败: {format_timeout_error(exc)}"
    return "ok", None


def register_gemini_mcp(install_root: Path, uv_executable: str) -> RegistrationResult:
    gemini = shutil.which("gemini")
    if not gemini:
        return "skip", None
    try:
        for name, entrypoint in MCP_SERVERS:
            best_effort_cleanup_command([gemini, "mcp", "remove", name, "--scope", "user"])
            best_effort_cleanup_command([gemini, "mcp", "remove", name, "--scope", "project"])
            print(f"正在注册 Gemini MCP: {name}")
            run_command(
                [
                    gemini,
                    "mcp",
                    "add",
                    name,
                    "--scope",
                    "user",
                    uv_executable,
                    "run",
                    "--project",
                    str(install_root),
                    entrypoint,
                ],
                quiet=True,
                timeout=MCP_REGISTER_TIMEOUT_SECONDS,
            )
            print(f"已注册 Gemini MCP: {name}")
    except subprocess.CalledProcessError as exc:
        return "warn", f"Gemini MCP 注册失败: {format_command_error(exc)}"
    except subprocess.TimeoutExpired as exc:
        return "warn", f"Gemini MCP 注册失败: {format_timeout_error(exc)}"
    return "ok", None


def prompt_required_value(prompt_text: str, secret: bool = False) -> str:
    while True:
        value = (getpass.getpass(prompt_text) if secret else input(prompt_text)).strip()
        if value:
            return value
        print("输入不能为空，请重新输入。")


def prompt_for_jira_credentials() -> None:
    username = prompt_required_value("请输入 Jira 用户名: ")
    password = prompt_required_value("请输入 Jira 密码: ", secret=True)
    upsert_config(JIRA_USERNAME=username, JIRA_PASSWORD=password)
    print("已保存 Jira 凭证。")


def prompt_for_debug_cookie() -> None:
    cookie = prompt_required_value("请输入 Debug 系统 Cookie: ")
    upsert_config(DEBUG_COOKIE=cookie)
    print("已保存 Debug Cookie。")


def prompt_for_ops_credentials() -> None:
    cookie = prompt_required_value("请输入运营系统 Cookie: ")
    base_url = input(f"请输入运营系统 Base URL（默认 {DEFAULT_ALCHEMY_BASE_URL}）: ").strip()
    upsert_config(
        ALCHEMY_COOKIE=cookie,
        ALCHEMY_BASE_URL=base_url or DEFAULT_ALCHEMY_BASE_URL,
    )
    print("已保存运营系统凭证。")


def print_install_configuration_status() -> None:
    status = config_status()
    print("安装配置向导:")
    print(f"- Jira 凭证: {'已配置' if status['jira'] else '缺失，将引导输入'}")
    print(f"- Debug Cookie: {'已配置' if status['debug_cookie'] else '缺失，将引导输入'}")
    print(f"- 运营系统 Cookie: {'已配置' if status['alchemy_cookie'] else '缺失，将引导输入'}")


def ensure_credentials(no_prompt: bool = False) -> None:
    status = config_status()
    if no_prompt:
        return
    print_install_configuration_status()
    if not status["jira"]:
        prompt_for_jira_credentials()
    if not status["debug_cookie"]:
        prompt_for_debug_cookie()
    if not status["alchemy_cookie"]:
        prompt_for_ops_credentials()


def test_jira_connection() -> tuple[bool, str]:
    config = load_config()
    username = config.get("JIRA_USERNAME")
    password = config.get("JIRA_PASSWORD")
    if not username or not password:
        return False, "Jira 凭证未配置"

    import base64

    auth = base64.b64encode(f"{username}:{password}".encode()).decode()
    req = request.Request(
        "http://jira.i-tetris.com/rest/api/2/myself",
        headers={"Authorization": f"Basic {auth}"},
    )
    try:
        with request.urlopen(req, timeout=10):
            return True, f"Jira 连接成功 ({username})"
    except error.HTTPError as exc:
        return False, f"Jira HTTP {exc.code}"
    except Exception as exc:
        return False, f"Jira 连接失败: {exc}"


def test_debug_connection() -> tuple[bool, str]:
    config = load_config()
    cookie = config.get("DEBUG_COOKIE")
    if not cookie:
        return False, "Debug Cookie 未配置"

    payload = json.dumps(
        {
            "vin": "test",
            "begin_date": "2024-01-01 00:00:00",
            "end_date": "2024-01-01 00:01:00",
            "page_index": 1,
            "page_size": 1,
        }
    ).encode()
    req = request.Request(
        "https://vos-debug.i-tetris.com/api/online_log/list",
        data=payload,
        headers={"Content-Type": "application/json", "Cookie": cookie},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=10) as response:
            body = response.read().decode()
        if "unauthorized" in body.lower() or "login" in body.lower():
            return False, "Debug Cookie 已过期"
        return True, "Debug 连接成功"
    except error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "Debug Cookie 已过期"
        return False, f"Debug HTTP {exc.code}"
    except Exception as exc:
        return False, f"Debug 连接失败: {exc}"


def test_ops_connection() -> tuple[bool, str]:
    config = load_config()
    cookie = config.get("ALCHEMY_COOKIE")
    if not cookie:
        return False, "运营系统 Cookie 未配置"

    base_url = (config.get("ALCHEMY_BASE_URL") or DEFAULT_ALCHEMY_BASE_URL).rstrip("/")
    req = request.Request(
        f"{base_url}/fi/function/list?pageNum=1&pageSize=1",
        headers={"Cookie": cookie, "Referer": "https://alchemy.i-tetris.com/"},
    )
    try:
        with request.urlopen(req, timeout=10) as response:
            body = response.read().decode()
        lowered = body.lower()
        if "auth_failed" in lowered or "login" in lowered or "unauthorized" in lowered:
            return False, "运营系统 Cookie 已失效"
        return True, "运营系统连接成功"
    except error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "运营系统 Cookie 已失效"
        return False, f"运营系统 HTTP {exc.code}"
    except Exception as exc:
        return False, f"运营系统连接失败: {exc}"


def print_test_results() -> bool:
    status = config_status()
    online_dialogue_root = detect_online_dialogue_root()
    jira_ok, jira_message = test_jira_connection()
    debug_ok, debug_message = test_debug_connection()
    ops_ok, ops_message = test_ops_connection()
    print(jira_message)
    print(debug_message)
    if status["alchemy_cookie"]:
        print(ops_message)
    else:
        print("运营系统 Cookie 未配置，已按降级路径跳过 ops 连通性校验。")
    print(
        "online-dialogue root: "
        + (str(online_dialogue_root) if online_dialogue_root else "not found")
    )
    return jira_ok and debug_ok and (ops_ok if status["alchemy_cookie"] else True)


def command_install(args: argparse.Namespace) -> int:
    source_root = Path(args.source_root).resolve() if args.source_root else project_root()
    install_root = get_install_root()
    uv_executable = find_uv()
    if not uv_executable:
        raise SystemExit("未检测到 uv，请先运行 install.sh 或 install.ps1。")

    print("正在清理旧版安装内容...")
    cleanup_previous_installation(install_root)
    print("正在复制运行时...")
    copy_runtime(source_root, install_root)
    print("正在同步 Python 依赖...")
    run_command([uv_executable, "sync", "--frozen", "--project", str(install_root)])

    config_path, migrated = migrate_legacy_config()
    wrapper = write_admin_wrapper(uv_executable, install_root)
    ensure_credentials(no_prompt=args.no_prompt)

    codex_skill_dir = install_skill(source_root, "codex")
    print(f"已安装 Codex skill: {codex_skill_dir}")
    gemini_skill_dir = install_skill(source_root, "gemini")
    print(f"已安装 Gemini skill: {gemini_skill_dir}")
    codex_result, codex_message = register_codex_mcp(install_root, uv_executable)
    gemini_result, gemini_message = register_gemini_mcp(install_root, uv_executable)
    tests_ok = print_test_results()

    print(f"安装版本: {__version__}")
    print(f"运行时目录: {install_root}")
    print(f"配置文件: {config_path}")
    print(f"管理命令: {wrapper}")
    if migrated:
        print("已迁移旧版 Gemini-only 配置。")
    if codex_result == "skip":
        print("未检测到 codex，已跳过 Codex MCP 注册。")
    elif codex_result == "warn" and codex_message:
        print(codex_message)
        print("已继续完成运行时与 skill 安装，可稍后单独重试 Codex MCP 注册。")
    if gemini_result == "skip":
        print("未检测到 gemini，已跳过 Gemini MCP 注册。")
    elif gemini_result == "warn" and gemini_message:
        print(gemini_message)
        print("已继续完成运行时与 skill 安装，可稍后单独重试 Gemini MCP 注册。")

    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    if str(wrapper.parent) not in path_entries:
        print(f"注意: {wrapper.parent} 不在 PATH 中，可能需要手动加入。")

    return 0 if tests_ok else 1


def command_configure_jira(_: argparse.Namespace) -> int:
    prompt_for_jira_credentials()
    print(f"已写入 Jira 凭证: {get_config_file()}")
    return 0


def command_configure_debug(_: argparse.Namespace) -> int:
    prompt_for_debug_cookie()
    print(f"已写入 Debug Cookie: {get_config_file()}")
    return 0


def command_configure_ops(_: argparse.Namespace) -> int:
    prompt_for_ops_credentials()
    print(f"已写入运营系统凭证: {get_config_file()}")
    return 0


def command_test(_: argparse.Namespace) -> int:
    return 0 if print_test_results() else 1


def command_doctor(_: argparse.Namespace) -> int:
    status = config_status()
    install_root = get_install_root()
    online_dialogue_root = detect_online_dialogue_root()
    print(f"analyze-bug version: {__version__}")
    print(f"config: {status['path']}")
    print(f"jira configured: {status['jira']}")
    print(f"debug cookie configured: {status['debug_cookie']}")
    print(f"ops configured: {status['alchemy_cookie']}")
    print(f"ops base url: {status['alchemy_base_url']}")
    print(f"install root: {install_root}")
    print(f"codex installed: {bool(shutil.which('codex'))}")
    print(f"gemini installed: {bool(shutil.which('gemini'))}")
    print(f"codex skill: {get_skill_dir('codex')}")
    print(f"gemini skill: {get_skill_dir('gemini')}")
    print(f"online-dialogue root: {online_dialogue_root or 'not found'}")
    return 0


def command_uninstall(args: argparse.Namespace) -> int:
    install_root = get_install_root()
    for platform in ("codex", "gemini"):
        skill_dir = get_skill_dir(platform)
        if skill_dir.exists():
            shutil.rmtree(skill_dir)

    codex = shutil.which("codex")
    if codex:
        for name, _ in MCP_SERVERS:
            best_effort_cleanup_command([codex, "mcp", "remove", name])

    gemini = shutil.which("gemini")
    if gemini:
        for name, _ in MCP_SERVERS:
            best_effort_cleanup_command([gemini, "mcp", "remove", name])

    if install_root.exists():
        shutil.rmtree(install_root)

    wrapper_dir = get_user_bin_dir()
    for filename in ("analyze-bug-admin", "analyze-bug-admin.cmd"):
        wrapper = wrapper_dir / filename
        if wrapper.exists():
            wrapper.unlink()

    if args.purge_config:
        config_file = get_config_file()
        if config_file.exists():
            config_file.unlink()

    print("已卸载 analyze-bug 运行时、skill 和 MCP 注册。")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="analyze-bug-admin")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install")
    install.add_argument("--source-root", help=argparse.SUPPRESS)
    install.add_argument("--no-prompt", action="store_true")
    install.set_defaults(func=command_install)

    configure_jira = subparsers.add_parser("configure-jira")
    configure_jira.set_defaults(func=command_configure_jira)

    configure_debug = subparsers.add_parser("configure-debug")
    configure_debug.set_defaults(func=command_configure_debug)

    configure_ops = subparsers.add_parser("configure-ops")
    configure_ops.set_defaults(func=command_configure_ops)

    test = subparsers.add_parser("test")
    test.set_defaults(func=command_test)

    doctor = subparsers.add_parser("doctor")
    doctor.set_defaults(func=command_doctor)

    uninstall = subparsers.add_parser("uninstall")
    uninstall.add_argument("--purge-config", action="store_true")
    uninstall.set_defaults(func=command_uninstall)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
