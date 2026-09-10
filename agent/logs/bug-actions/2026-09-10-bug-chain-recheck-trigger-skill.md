# Bug chain recheck trigger Skill

- 日期：2026-09-10
- 原因：新增纯感叹号/问号快捷触发器，用于重新审查当前 Bug 的完整证据与处理链路。
- 影响文件：`agent/skills/bug-chain-recheck-trigger/SKILL.md`、`agent/logs/bug-actions/2026-09-10-bug-chain-recheck-trigger-skill.md`
- 触发范围：消息去除首尾空白后，仅由 `!`、`！`、`?`、`？` 组成，可夹空格；不含 Jira、链接或普通文字。
- 权限边界：沿用普通 `recheck` 流程；不新增 Jira 外部动作授权，不绕过身份、证据门禁、写表和回读要求。
- 验证案例：`!`、`？？`、`!？！` 触发；`! 看一下`、`HUR-12345!`、Jira 链接不触发。
- 回滚口径：删除新增 Skill 与本日志；不删除 Bug 证据或历史判断。
