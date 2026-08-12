# 2026-08-12 GitHub持续交付规则

- 操作者：Codex（本机绑定 wu-you）
- 涉及 Jira：无
- 操作类型：规则维护 / Git交付
- 写入摘要：将用户“本次上传且以后更新都上传”的授权固化到AGENTS、onboarding和Bug workflow；同步修正Bug与复盘流程残留的schema v3文字和表格校验序号；规则版本更新为v1.10.1-trial.1。
- Git动作：提交前执行规则测试、run最终校验、敏感信息检查和diff检查；推送后核对远端main提交。
- Jira动作：未评论 Jira / 未转派 Jira / 未关闭 Jira / 未变更状态
- 敏感信息处理：不提交local-profile、Cookie、Token、连接器授权、定时任务或访问口令。
