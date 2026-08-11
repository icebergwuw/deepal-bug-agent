# 客户问题编号与测试用例门槛规则维护

- 日期：2026-07-29
- 操作者：Codex
- 涉及 Jira：ADS-47560
- 操作类型：复盘表格更新 / 规则维护 / 会议沉淀

## 变更

- 在 `agent/evidence-contract.md` 增加客户提报 Bug 识别与测试用例门槛，作为唯一证据口径。
- 在 Bug 流程中增加客户问题编号提取、客户测试用例检查和缺失时 `待确认` 的执行步骤；复盘流程只定义对应 G/H/I/J 更新。
- 决策核验卡新增 `客户问题识别`，机器校验要求记录 `external_id`、测试用例状态和来源；用例缺失或不完整时拒绝 `可关闭 / 非 Bug / 设计如此 / Invalid`。
- 新增两项单元测试：缺客户用例禁止关闭、缺客户用例允许待确认并要求收集动作。
- 规则版本更新为 `v1.4.0-trial.1`。

## ADS-47560 写表结果

- 已按 `review` 更新 `bug!G150,H150,I150,J150`，保留 A-F。
- G=`待确认`；H 写明客户测试用例缺口及吴优的收集动作；J 保留三个原始可点击入口。
- 写后 `validate-patch --key ADS-47560 --mode review` 通过。

## 外部动作

- 未评论、转派、关闭或修改 Jira 状态。
- 未向客户发送消息；已把索取客户测试用例记录为吴优待办。

## 验证

- `python3 agent/scripts/test_bug_evidence_gate.py`：7 项通过。
- `python3 agent/scripts/test_bug_sheet_contract.py`：11 项通过。
- `python3 agent/scripts/validate_rule_architecture.py`：`ok: true`。
- `python3 agent/scripts/validate_bug_evidence_gate.py --key ADS-47560 --log agent/logs/bug-actions/2026-07-29-ADS-47560.md`：通过。
- `git diff --check`：通过。
- 已在 Google 表格页面打开 `bug!G150:J150`：G 显示 `待确认`，H/I 完整可读，J 的三个短标签均显示为可点击链接，未发现裁切或样式破坏。
