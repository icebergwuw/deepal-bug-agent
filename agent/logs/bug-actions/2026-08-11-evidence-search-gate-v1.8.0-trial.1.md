# 证据检索门禁 v1.8.0-trial.1

- 日期：2026-08-11
- 类型：规则与工具整改
- 范围：本地 Bug 项目规则、证据门禁、写表请求生成和脚本目录治理
- 外部动作：未修改线上 Bug 表，未评论、转派或变更 Jira 状态

## 问题复核

- schema v2 只要求 `queries` 非空，无法识别只有 Jira key、标题片段或无语义字符串的低质量检索记录。
- Drive/UE/PRD 检索命中候选后，没有机器字段强制逐项读取或排除，导致已存在的正式资料仍可被记为 `not_found`。
- 写表请求生成未绑定已通过的本票 manifest，一次性批量脚本可以自行拼装行数据和预览信息，形成门禁旁路。

## 已实施

- manifest 升级到 schema v3，query 改为 `{kind, text}` 并按必查动作校验所需语义维度。
- 对正式资料类 `not_found` 增加 `candidate_audit`；候选必须逐项标记 `read / excluded / unavailable`，已读候选禁止隐藏为 `not_found`。
- `bug_sheet_contract.py build / patch` 强制传入每票已通过且 Jira key 一致的 manifest。
- `agent/scripts/` 采用显式允许清单；四个一次性构建脚本移至 `agent/archive/scripts/`，仅供历史审计。

## 验证与回读

- `test_bug_evidence_gate.py`：26 项通过。
- `test_bug_sheet_contract.py`：15 项通过。
- `validate_rule_architecture.py`：`ok: true`。
- 本日志已回读；本次未产生线上表格或 Jira 写入，无外部回读项。
