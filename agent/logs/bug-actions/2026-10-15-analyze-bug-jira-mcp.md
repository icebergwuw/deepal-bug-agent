# 2026-10-15 analyze-bug Jira MCP

- 动作：把 analyze-bug 0.4.1 的 Jira MCP 接到本仓库，供后续单票读取使用。
- 入口：`.grok/config.toml` 的 `analyze_bug_jira`，命令 `agent/scripts/analyze-bug-jira-mcp.sh`。
- 读工具：`get_jira_issue`。本地补了经办人、模块、标签和关联票，原包这三个读字段没有返回。
- 写工具：`add_jira_comment`、`update_jira_description`。本次没有调用。
- 凭证：沿用项目 `.env`，不写入仓库。
- 未执行：没有评论、转派、关闭或改描述。
