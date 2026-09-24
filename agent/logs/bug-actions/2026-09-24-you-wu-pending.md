# 2026-09-24 吴优名下未关闭 Bug 批量 Pending

- 操作者：Codex
- Run ID：20260924T101800+0800-you-wu-pending
- 涉及 Jira：ADS-46438、ADS-50547、ADS-50563、HUR-80638、HUR-85062、HUR-85064、PC-36610、SD-5515、SD-6404、SD-6421、SD-7800
- 操作类型：流转 Jira
- 读取证据：用户给出的 JQL 实查 11 张；逐票读取当前状态和可用流转。工作流里待办、重新打开不能直接 Pending，处理中可以。
- 表格位置：未改线上表
- 写入摘要：未写表。按用户明确授权，把经办人 you.wu、状态为待办/处理中/重新打开的 11 张 Bug 流转到 Pending。
- Jira 动作：未评论，未改经办人。待办先走「开始进行」到处理中，再走 Pending；重新打开先走 Start Progress 到处理中，再走 Pending；处理中直接 Pending。11 张 HTTP 204。
- 回读校验：流转后用同一批 key 重新查询，11 张状态均为 Pending，经办人均为 you.wu。
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未评论 Jira，未改经办人，未更新负责人表或本地索引，未做产品结论。
- 敏感信息处理：未记录账号、密码、token 或访问口令

## 流转结果

| Key | 流转前 | 流转后 | 路径 |
| --- | --- | --- | --- |
| ADS-46438 | 待办 | Pending | 开始进行 → Pending |
| ADS-50547 | 待办 | Pending | 开始进行 → Pending |
| ADS-50563 | 处理中 | Pending | Pending |
| HUR-80638 | 重新打开 | Pending | Start Progress → Pending |
| HUR-85062 | 待办 | Pending | 开始进行 → Pending |
| HUR-85064 | 重新打开 | Pending | Start Progress → Pending |
| PC-36610 | 处理中 | Pending | Pending |
| SD-5515 | 待办 | Pending | 开始进行 → Pending |
| SD-6404 | 待办 | Pending | 开始进行 → Pending |
| SD-6421 | 处理中 | Pending | Pending |
| SD-7800 | 处理中 | Pending | Pending |
