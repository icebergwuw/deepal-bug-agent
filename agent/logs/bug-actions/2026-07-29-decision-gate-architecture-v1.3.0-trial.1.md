# 2026-07-29 决策核验关口架构补强

- 操作者：Codex
- 涉及 Jira：HUR-82492（验证案例）；未批量处理其他 Jira。
- 操作类型：规则维护、日志回填与本地校验；未写线上 Bug 表，未执行 Jira 外部动作。

## 用户确认的改动范围

- 保持现有“契约 / 工作流 / 知识库 / 日志 / 脚本”层级，不新建 `agent/decisions/` 或第二套规则目录。
- 在现有证据契约中增加决策关口，在日志中增加可审计决策核验卡，在流程中增加关联票必读和写表前校验。
- 研发评论知识库退回检索信号职责；评论权重、来源取舍与结论门槛仅由证据契约定义。

## 完成内容

- 新增五项决策核验卡和 `validate_bug_evidence_gate.py`：备注因果链、关联票、资料适用范围、冲突处理、唯一结论。
- Bug 流程把问题链接、同根因/同日志/重复/预期冲突关联票列为必读条件，并明确共享日志不能替代产品目标核验。
- HUR-82492 操作日志已按同一格式回填，专项 J90A 资料标记为 `exact`，共通资料标记为 `mismatch`。
- 架构校验新增对决策关口、流程入口、日志字段和评论信号库去重的检查；新增独立单元测试。

## 回读与未执行动作

- 已回读：`python3 agent/scripts/test_bug_evidence_gate.py` 4 项通过；`python3 agent/scripts/test_bug_sheet_contract.py` 11 项通过；`python3 agent/scripts/validate_rule_architecture.py` 与 HUR-82492 日志核验均返回 `ok: true`；`git diff --check` 无输出。
- 未评论 Jira、未改状态、未转派、未关闭 Jira；未写线上 Bug 表。
- 敏感信息处理：未记录账号、密码、token、测试账号明文或平台访问口令。
