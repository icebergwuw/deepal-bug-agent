# 2026-10-23 建票后飞书通知

- 操作者：吴优
- Run ID：20261023T120500+0800-feishu-notify
- 涉及 Jira：无新票
- 操作类型：规则维护
- 读取证据：吴优指定飞书应用和群，要求建完票后通知。密钥只写入本机 gitignore 文件，不进入本次读取摘要。
- 表格位置：不适用
- 写入摘要：登记飞书群 `oc_c3692001480b0aac7825bafab90989b3` 和应用 ID `cli_aa506e13fcf8dcf5`。变更表新建需求回读成功后调用 `agent/scripts/notify_feishu_ticket.py`。
- Jira 动作：未评论 Jira / 未流转 Jira / 未建票
- 回读校验：规则架构校验通过。已安装 Skill 与仓库模板一致。
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未另发飞书消息。ADS-52385 已在该群通知。未写吴优 bug 表，未写 Alchemy
- 敏感信息处理：未记录 App Secret、密码、token 或访问口令
