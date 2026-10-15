#!/bin/zsh
# 启动 analyze-bug 的某一个 MCP。
# 用法：analyze-bug-mcp.sh jira|debug|rules|ops
# Jira 账号来自项目 .env。Debug / Alchemy Cookie 优先用 .env，否则从已登录 Chrome 提取。
# 凭证只写入 gitignore 的 .analyze-bug/，不打印。
set -euo pipefail

SERVER="${1:-}"
case "$SERVER" in
  jira|debug|rules|ops) ;;
  *)
    print -u2 "用法：analyze-bug-mcp.sh jira|debug|rules|ops"
    exit 1
    ;;
esac

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ENV_FILE="$ROOT/.env"
VENDOR="$ROOT/agent/vendor/analyze-bug"
CONFIG_ROOT="$ROOT/.analyze-bug"
CRED="$CONFIG_ROOT/analyze-bug/credentials.env"
PY="$VENDOR/.venv/bin/python"
UV="${UV_BIN:-$HOME/.local/bin/uv}"

if [[ ! -x "$PY" ]]; then
  if [[ ! -x "$UV" ]]; then
    print -u2 "未找到 uv，无法安装 analyze-bug MCP。"
    exit 1
  fi
  "$UV" sync --project "$VENDOR"
fi

if ! "$PY" -c "import browser_cookie3" >/dev/null 2>&1; then
  "$UV" pip install --python "$PY" browser-cookie3 >/dev/null
fi

"$PY" - "$ENV_FILE" "$CRED" "$SERVER" <<'PY'
import sys
from pathlib import Path

env_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
server = sys.argv[3]

def read_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data

def cookie_ok(value: str) -> bool:
    return "ops-name=" in value and "token=" in value and len(value) > 80

existing = read_env(out_path)
project = read_env(env_path) if env_path.exists() else {}
merged = dict(existing)
for key in ("JIRA_USERNAME", "JIRA_PASSWORD", "DEBUG_COOKIE", "ALCHEMY_COOKIE", "ALCHEMY_BASE_URL"):
    if project.get(key):
        merged[key] = project[key]

need_chrome = not cookie_ok(merged.get("DEBUG_COOKIE", "")) or not cookie_ok(merged.get("ALCHEMY_COOKIE", ""))
if need_chrome:
    import multiprocessing

    def chrome_cookies(queue) -> None:
        try:
            import browser_cookie3
        except ImportError:
            queue.put({})
            return
        profiles = ["Profile 1", "Default", "Profile 2", "Profile 3"]
        targets = {
            "ALCHEMY_COOKIE": "alchemy.i-tetris.com",
            "DEBUG_COOKIE": "vos-debug.i-tetris.com",
        }
        found: dict[str, str] = {}
        for key, host in targets.items():
            best = ""
            for profile in profiles:
                cookie_file = Path.home() / f"Library/Application Support/Google/Chrome/{profile}/Cookies"
                if not cookie_file.exists():
                    continue
                try:
                    jar = browser_cookie3.chrome(cookie_file=str(cookie_file))
                except Exception:
                    continue
                parts = []
                for item in jar:
                    domain = (item.domain or "").lstrip(".")
                    if item.name not in ("token", "ops-name"):
                        continue
                    if domain != host and not host.endswith(domain):
                        continue
                    parts.append(f"{item.name}={item.value}")
                parts.sort(key=lambda part: 1 if part.startswith("token=") else 0)
                candidate = "; ".join(parts)
                if cookie_ok(candidate) and len(candidate) > len(best):
                    best = candidate
            if best:
                found[key] = best
        queue.put(found)

    ctx = multiprocessing.get_context("fork")
    queue = ctx.Queue()
    worker = ctx.Process(target=chrome_cookies, args=(queue,))
    worker.start()
    worker.join(20)
    if worker.is_alive():
        worker.terminate()
        worker.join(2)
        sys.stderr.write("chrome_cookie=timeout\n")
    else:
        try:
            found = queue.get_nowait()
        except Exception:
            found = {}
        for key, value in found.items():
            if cookie_ok(value):
                merged[key] = value

if server == "jira" and not (merged.get("JIRA_USERNAME") and merged.get("JIRA_PASSWORD")):
    sys.stderr.write("项目 .env 缺少 JIRA_USERNAME 或 JIRA_PASSWORD\n")
    sys.exit(1)

order = ["JIRA_USERNAME", "JIRA_PASSWORD", "DEBUG_COOKIE", "ALCHEMY_COOKIE", "ALCHEMY_BASE_URL"]
lines = [f"{key}={merged[key]}" for key in order if merged.get(key)]
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
out_path.chmod(0o600)

def flag(key: str) -> str:
    value = merged.get(key, "")
    if key in ("DEBUG_COOKIE", "ALCHEMY_COOKIE"):
        return "ready" if cookie_ok(value) else "missing"
    return "ready" if value else "missing"

sys.stderr.write(
    "credentials"
    f" jira_user={flag('JIRA_USERNAME')}"
    f" jira_password={flag('JIRA_PASSWORD')}"
    f" debug={flag('DEBUG_COOKIE')}"
    f" alchemy={flag('ALCHEMY_COOKIE')}\n"
)
PY

export XDG_CONFIG_HOME="$CONFIG_ROOT"
export PYTHONUNBUFFERED=1
export NO_PROXY="*"
export no_proxy="*"
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy || true

exec "$VENDOR/.venv/bin/analyze-bug-${SERVER}-mcp"
