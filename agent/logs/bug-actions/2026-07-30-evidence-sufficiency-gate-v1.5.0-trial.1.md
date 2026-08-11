# Bug 证据充分性硬门禁规则维护

- 日期：2026-07-30
- 操作者：Codex
- 涉及 Jira：PC-37681（失败模式与通过案例）、HUR-82492（非语音回归）、ADS-47560（客户用例回归）
- 操作类型：规则维护与本地校验
- 外部动作：未写线上 Bug 表；未评论、转派、关闭或修改 Jira 状态。

## 用户确认的改动范围

- 把同范围正式定义、实现事实、资料缺口和语音证据链改成写入确定性状态前的机器硬门禁。
- 重新处理 Bug 前，必须完整读取 Jira 评论区，并补齐当前 Jira、Drive 正式资料、语音平台和直接关联票的决定性证据。
- 本日志只记录门禁规则维护；后续批量 Bug 处理必须逐票另留证据、结论、写表和回读记录。

## 完成内容

- 每条资料增加唯一 `source_id` 和 `formal_target / implementation_actual / context_only` 角色。
- 确定性结论必须由预期行为卡引用有效目标来源，并由结论引用 `implementation_actual + exact` 来源。
- `mismatch` 一律排除；跨项目 `partial` 定义只有经 `context_only + exact` 的项目继承声明连接且标记 `verified=true` 后生效。
- `material=true` 的关键资料缺口禁止确定性状态；缺口附原因和下一步、降为待处理状态后才可通过。
- 语音类必须记录 Jira 用户原话、Alchemy 当前结果、`meta_id`、标准功能点和项目功能点；平台不可用或链路未完成时显式降级。
- 客户测试用例缺失规则从“只禁止关闭”收紧为状态固定 `待确认`。

## 回归结果

- `python3 agent/scripts/test_bug_evidence_gate.py`：14 项通过。
- `python3 agent/scripts/test_bug_sheet_contract.py`：11 项通过。
- `python3 agent/scripts/validate_rule_architecture.py`：`ok: true`。
- `git diff --check`：通过。

## 边界

- 门禁能校验来源角色、适用范围、继承链、引用关系和缺口状态，但不能自动判断文档内容是否被人为错误标成 `formal_target`；处理人仍须按证据契约完整读取原文并记录具体条款。
- `project_function.status=not_applicable` 只表示已核验后确认没有项目继承功能点，不得用于表示“没有读取”。
- 未记录密码、token、测试账号明文或平台访问口令。
