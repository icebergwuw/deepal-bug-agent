#!/bin/zsh
# 启动本仓库里的 analyze-bug Jira MCP。
# 凭证只从项目根目录的 .env 读取，写入 gitignore 的 .analyze-bug/，不打印。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ENV_FILE="$ROOT/.env"
VENDOR="$ROOT/agent/vendor/analyze-bug"
CONFIG_ROOT="$ROOT/.analyze-bug"
CRED="$CONFIG_ROOT/analyze-bug/credentials.env"
UV="${UV_BIN:-$HOME/.local/bin/uv}"

if [[ ! -r "$ENV_FILE" ]]; then
  print -u2 "缺少可读的 $ENV_FILE。请在项目根目录配置 JIRA_USERNAME 和 JIRA_PASSWORD。"
  exit 1
fi

python3 - "$ENV_FILE" "$CRED" <<'PY'
import sys
from pathlib import Path

env_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
wanted = {}
for raw in env_path.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if key in ("JIRA_USERNAME", "JIRA_PASSWORD"):
        wanted[key] = value

missing = [key for key in ("JIRA_USERNAME", "JIRA_PASSWORD") if not wanted.get(key)]
if missing:
    sys.stderr.write("项目 .env 缺少 " + "、".join(missing) + "\n")
    sys.exit(1)

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(
    "".join(f"{key}={wanted[key]}\n" for key in ("JIRA_USERNAME", "JIRA_PASSWORD")),
    encoding="utf-8",
)
out_path.chmod(0o600)
PY

export XDG_CONFIG_HOME="$CONFIG_ROOT"
export PYTHONUNBUFFERED=1
export NO_PROXY="*"
export no_proxy="*"
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy || true

if [[ ! -x "$VENDOR/.venv/bin/analyze-bug-jira-mcp" ]]; then
  if [[ ! -x "$UV" ]]; then
    print -u2 "未找到 uv，无法安装 analyze-bug Jira MCP。"
    exit 1
  fi
  "$UV" sync --project "$VENDOR"
fi

exec "$VENDOR/.venv/bin/analyze-bug-jira-mcp"
