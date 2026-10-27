# 2026-10-27 HUR 文言与语料 story 分流

- 操作者：Codex
- Run ID：20261027T152000+0800-hur-story-handoff
- 涉及 Jira：HUR-85390 / HUR-84627 / HUR-86245
- 操作类型：规则维护
- 读取证据：吴优 2026-10-27 口径；`get_jira_issue` 回读三张 story 的状态和经办人
- 表格位置：不适用
- 写入摘要：原 Bug 关票是一定的。转需求 story 未传递给开发且经办人仍是 `you.wu` 时复用，已传递给开发才新建。长马文言和语料共用这个判断。
- Jira 动作：未评论 Jira / 未流转 Jira / 未新建 Jira
- 回读校验：`HUR-85390` 待办，经办人 `you.wu`。`HUR-84627` Pending，经办人 `you.wu`。`HUR-86245` 待办，经办人 `you.wu`。后两张只覆盖小憩和露营。
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未评论 Jira、未流转 Jira、未更新语料表、未写变更管理表、未发飞书
- 敏感信息处理：未记录账号、密码、token 或访问口令
