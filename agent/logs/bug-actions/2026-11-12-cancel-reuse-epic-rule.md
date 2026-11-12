# 2026-11-12 取消不沿用原票 Epic

- 操作者：吴优
- Run ID：20261112T1123+0800-reuse-epic
- 涉及 Jira：HUR-87169
- 操作类型：规则维护 / 新建需求
- 读取证据：吴优要求取消「不沿用原票 Epic」。参考票 HUR-87038 的 Epic 是 HUR-2。HUR 没有未关闭的精确标题 `ECR_待签署`。语料表未改。未打印凭证。
- 表格位置：不适用
- 写入摘要：取消不能沿用同项目参考票 Epic 的限制。有 `ECR_待签署` 时仍优先用它。没有这张 Epic 时沿用同项目参考票 Epic。不跨项目，不改已有票 Epic。
- Jira 动作：新建 HUR-87169，故事，P1，经办人朱雪豪，模块 AI Cockpit - Voice/General，车型 J90A/EL，Epic HUR-2，修复版本无发版计划。未评论，未流转。
- 回读校验：`get_jira_issue` 回读 HUR-87169，标题、经办人、Epic 与创建一致。`python3 agent/scripts/validate_rule_architecture.py` 通过。安装副本与变更表 Skill 模板一致。
- 未执行动作：未改语料表，未发飞书，未写变更管理表，未评论 Jira
- 敏感信息处理：未记录账号、密码、token 或访问口令
