# 2026-08-14 UE 语音覆盖 Skill 仓库拆分

- 操作者：Codex（本机绑定 wu-you）
- 涉及 Jira：无
- 操作类型：Skill 管理 / 规则维护 / Git 交付
- 写入摘要：将 `audit-ue-voice-coverage` 拆分为独立私有仓库，Skill 版本重置为 `v1.0.0`；Bug 仓库改为锁定外部依赖，不再复制 Skill 源码。
- Skill 仓库：`https://github.com/icebergwuw/audit-ue-voice-coverage`（private）
- Skill 提交：`7fd08f9ca4f3d553d37ac24e9fc48011849fb21d`
- Skill 标签：`v1.0.0`
- 保留范围：原语音覆盖审核 manifest、表格回读结果和历史操作日志仍在 Bug 项目保留。
- 凭据边界：未提交本机身份、密码、Token、Cookie、浏览器会话或 SSH 私钥。
- Jira 动作：未评论 Jira / 未转派 Jira / 未关闭 Jira / 未变更状态
