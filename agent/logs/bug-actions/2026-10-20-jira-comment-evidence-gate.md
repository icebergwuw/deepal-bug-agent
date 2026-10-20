# 2026-10-20 Jira 评论接入证据门禁

- 操作者：吴优
- Run ID：20261020T170000+0800-comment-gate
- 涉及 Jira：无
- 操作类型：规则维护
- 读取证据：`agent/workflows/bug.md`、`agent/evidence-contract.md`、`agent/scripts/validate_bug_evidence_gate.py`、`agent/scripts/bug_sheet_contract.py`、2026-10-20 评论日志
- 表格位置：不适用
- 写入摘要：新增 `authorize_jira_comment.py`。评论前必须通过证据门禁；`jira_comment_only` 不再绕过 Drive 正式定义、客户用例和版本族核验。
- Jira 动作：未评论 Jira / 未流转 Jira
- 回读校验：规则架构校验和评论授权测试在本次提交前执行
- run bundle：不适用
- readback_sha256：不适用
- 未执行动作：未修改已发出的 Jira 评论，未转派，未关闭，未改状态，未写吴优 bug 表，未写 Alchemy
- 敏感信息处理：未记录账号、密码、token 或访问口令
