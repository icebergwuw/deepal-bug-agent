# 2026-08-06 证据画像门禁 v1.7.0-trial.1

- 操作者：Codex
- 涉及 Jira：PC-38036、PC-37808（仅作为规则验证案例）
- 操作类型：规则维护
- 读取证据：现行 `AGENTS.md`、证据/输出/表格契约、普通与复盘工作流、证据门禁脚本及测试、PC-38036/PC-37808 既有处理产物。
- 表格位置：未更新线上表。
- 写入摘要：新增机器可读证据画像与必查动作配置，manifest 升级为 v2，统一普通与复盘门禁，并增加批量日志逐 Jira 卡校验。
- Jira 动作：未评论 Jira / 未流转 Jira。
- 回读校验：已回读规则、配置、脚本和本日志；完整校验均通过，结果见下方。
- 未执行动作：未更新 Jira、线上表、本地负责人索引或既有 Bug 结论。
- 敏感信息处理：未记录账号、密码、token、测试账号明文或访问口令。

## 修改原因

旧门禁能够确认“manifest 中已列出的资料是否够用”，却不能确认“按问题类型本来必须查的 Drive PRD、专项定义、配置或 UE 是否实际查过”。因此 PC-38036 和 PC-37808 型案例即使漏掉对应资料检索，也可能通过结构校验。问题在机器规则缺少必查动作闭环，而不只是提示文字不够醒目。

## 新规则

- 所有 manifest 使用 `schema_version=2`，逐项评估 `general`、`voice`、`map_navigation`、`visible_interaction` 画像，可组合命中，不允许静默跳过。
- 每个命中画像展开 `required_evidence_checks`，记录检索日期、入口、关键词、状态、来源引用或精确限制；未找到和不可访问也必须留轨迹。
- 每条 `scope_checks` 登记 `source_type`。Alchemy 当前输出、Jira 和日志不能作为正式目标；Alchemy 标准/项目定义不能成为唯一的产品正式交互目标。
- 普通流程写 D 和复盘流程写 H 走同一门禁；批量日志按 Jira key 分别提供完整七项决策核验卡。

## 历史记录边界

`2026-08-06-you-wu-recheck-131-135-manifests.json` 是 v1.7 生效前生成的 `schema_version=1` 历史证据，不自动迁移，也不据此声称已补查 Drive 或 UE。131–135 行如需按 v1.7 形成新结论，必须重新读取实时 Jira 和对应资料并生成 v2 manifest。

## 验证与回读

- `python3 agent/scripts/test_bug_evidence_gate.py`：22 项通过。
- `python3 agent/scripts/test_bug_sheet_contract.py`：12 项通过。
- `python3 agent/scripts/validate_rule_architecture.py`：通过，`ok=true`。
- `python3 agent/scripts/sync_bug_skill.py`：通过，Git 内模板与安装副本一致。
- `python3 -m py_compile agent/scripts/validate_bug_evidence_gate.py agent/scripts/validate_rule_architecture.py`：通过。
- `jq empty agent/config/evidence-requirements.json`：通过。
- `git diff --check`：通过。
