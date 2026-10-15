# 2026-10-15 analyze-bug MCP 全套

- 动作：在已有 `analyze_bug_jira` 之外，登记 `analyze_bug_debug`、`analyze_bug_rules`、`analyze_bug_ops`。
- 入口：`.grok/config.toml`，命令 `agent/scripts/analyze-bug-mcp.sh`。
- Ops：无 Cookie 可启动；请求带 `Referer: https://alchemy.i-tetris.com/`，不走系统代理。
- 凭证：Jira 仍用项目 `.env`。Debug / Alchemy Cookie 从本机已登录 Chrome 提取到 `.analyze-bug/`，不进入仓库，不写入本日志。
- 未执行：没有评论、改描述、转派、关闭，也没有写入 Alchemy。
