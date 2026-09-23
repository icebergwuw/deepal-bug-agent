# 2026-09-17 Drive 检索入口门禁

- 操作者：吴优 / `wu-you`
- Run ID：`rules-20260917-origin-chrome`
- 涉及 Jira：PC-40393
- 操作类型：规则维护
- 记录状态：reconstructed。版本说明已引用本日志，但原文件当时未落地，本次按版本说明补记，不改当时证据内容。
- 读取证据：v1.18.0-trial.1 版本说明
- 表格位置：不适用
- 写入摘要：取消写表门禁对 Drive 检索回执 `origin=connector` 的强制要求。回执记录实际入口，优先 `chrome`。
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：`python3 agent/scripts/test_bug_evidence_gate.py` 覆盖 `origin=chrome`、`origin=in_app_browser` 和拒绝 `origin=manual`
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未改线上 Bug 行
- 敏感信息处理：未记录账号、密码、token 或访问口令
