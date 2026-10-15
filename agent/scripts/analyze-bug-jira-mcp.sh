#!/bin/zsh
# 兼容旧入口。凭证和启动逻辑在 analyze-bug-mcp.sh。
exec "$(cd "$(dirname "$0")" && pwd)/analyze-bug-mcp.sh" jira
