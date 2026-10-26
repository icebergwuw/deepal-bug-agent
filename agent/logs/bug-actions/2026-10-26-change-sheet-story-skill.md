# 2026-10-26 变更表建票 skill

- 操作者：吴优
- Run ID：20261026T100000+0800-change-sheet-skill
- 涉及 Jira：无新票
- 操作类型：规则维护
- 读取证据：吴优要求把变更表建票、按 U 列设经办人、回写 D 列、带依赖项通知飞书的流程沉淀成 skill。
- 表格位置：不适用
- 写入摘要：新增 `deepal-change-sheet-story`。仓库模板与本机安装副本保持一致。普通 Bug skill 改为指向它，不再在 Bug 流程里临时改写建票步骤。
- Jira 动作：未评论 Jira / 未流转 Jira / 未建票
- 回读校验：Skill 结构校验通过。规则架构校验通过。已安装变更表 skill 与仓库模板一致，Bug skill 安装副本也已同步。
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未新建 Jira，未另发飞书消息，未改已有票，未写 Alchemy
- 敏感信息处理：未记录 App Secret、密码、token 或访问口令
