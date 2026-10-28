# 2026-10-28 Drive 读取默认走 Google API

- 操作者：吴优
- Run ID：bug-20261028T110800+0800-google-api-default
- 涉及 Jira：无
- 操作类型：规则维护
- 读取证据：吴优确认用已配置的 Google API 优化读取链路
- 写入摘要：预检探测本机 token。成功时 Drive entry 为 google_api；失败时退回 Chrome。写表通道未改
- Jira 动作：未评论、未转派、未关闭
- 回读校验：预检 google_drive.entry 为 google_api，api_ok 为 true。结果不含 token
- 未执行动作：未改写表通道，未把 token 写入仓库
- 敏感信息处理：未记录账号、密码、token 或访问口令
