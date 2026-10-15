import os
from pathlib import Path

from analyze_bug.core.paths import get_config_file, iter_legacy_config_files
from analyze_bug.core.responses import CredentialError


_CONFIG_CACHE: dict[Path, tuple[float | None, dict]] = {}
DEFAULT_ALCHEMY_BASE_URL = "https://alchemy.i-tetris.com/api/v1/ops"


def _read_env_file(path: Path) -> dict:
    config = {}
    if not path.exists():
        return config

    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


def load_config(path: Path | None = None) -> dict:
    config_path = Path(path or get_config_file())
    stat = config_path.stat() if config_path.exists() else None
    cache_key = config_path.resolve()
    cached = _CONFIG_CACHE.get(cache_key)
    mtime = stat.st_mtime if stat else None

    if cached and cached[0] == mtime:
        return dict(cached[1])

    data = _read_env_file(config_path)
    _CONFIG_CACHE[cache_key] = (mtime, dict(data))
    return data


def write_config(config: dict, path: Path | None = None) -> Path:
    config_path = Path(path or get_config_file())
    config_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in config.items()]
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if os.name != "nt":
        os.chmod(config_path, 0o600)
    _CONFIG_CACHE.pop(config_path.resolve(), None)
    return config_path


def migrate_legacy_config() -> tuple[Path, bool]:
    new_path = get_config_file()
    merged = load_config(new_path) if new_path.exists() else {}
    changed = False

    for legacy_path in iter_legacy_config_files():
        if not legacy_path.exists():
            continue
        legacy = load_config(legacy_path)
        for key, value in legacy.items():
            if value and not merged.get(key):
                merged[key] = value
                changed = True

    if changed or (merged and not new_path.exists()):
        write_config(merged, new_path)
        return new_path, True
    return new_path, False


def upsert_config(**kwargs) -> Path:
    config = load_config()
    for key, value in kwargs.items():
        if value is not None:
            config[key] = value
    return write_config(config)


def get_jira_auth() -> tuple[str, str]:
    config = load_config()
    username = config.get("JIRA_USERNAME")
    password = config.get("JIRA_PASSWORD")
    if not username or not password:
        raise CredentialError(
            "Jira 凭证未配置或不完整。请运行 `analyze-bug-admin configure-jira`。"
        )
    return username, password


def get_debug_cookie() -> str:
    config = load_config()
    cookie = config.get("DEBUG_COOKIE")
    if not cookie:
        raise CredentialError(
            "Debug 系统 Cookie 未配置。请运行 `analyze-bug-admin configure-debug`。"
        )
    return cookie


def get_ops_cookie() -> str:
    config = load_config()
    cookie = config.get("ALCHEMY_COOKIE")
    if not cookie:
        raise CredentialError(
            "运营系统 Cookie 未配置。请运行 `analyze-bug-admin configure-ops`。"
        )
    return cookie


def get_ops_base_url() -> str:
    config = load_config()
    return (config.get("ALCHEMY_BASE_URL") or DEFAULT_ALCHEMY_BASE_URL).strip().rstrip("/")


def get_online_dialogue_root() -> str | None:
    config = load_config()
    value = (config.get("ONLINE_DIALOGUE_ROOT") or "").strip()
    return value or None


def config_status() -> dict:
    config = load_config()
    return {
        "jira": bool(config.get("JIRA_USERNAME") and config.get("JIRA_PASSWORD")),
        "debug_cookie": bool(config.get("DEBUG_COOKIE")),
        "alchemy_cookie": bool(config.get("ALCHEMY_COOKIE")),
        "alchemy_base_url": get_ops_base_url(),
        "online_dialogue_root": get_online_dialogue_root(),
        "path": str(get_config_file()),
    }
