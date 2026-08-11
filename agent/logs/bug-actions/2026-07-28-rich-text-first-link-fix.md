# 富文本首标签重复链接修复

- 日期：2026-07-28
- 涉及 Jira：ADS-47367（作为复盘写表校验案例）
- 操作类型：表格契约脚本修复与验证。

## 问题与修复

- `bug_sheet_contract.py` 在第一个富文本标签从单元格第 0 位开始时，同时提交默认运行段和链接运行段；Google Sheets 回读为两个相同的首链接。
- 调整为仅在首个标签前存在普通文本时才提交默认运行段，并新增 `test_first_link_at_zero_has_one_run`。
- 该修复不改变列职责、证据门槛或 Jira 外部动作权限。

## 验证与边界

- `python3 agent/scripts/test_bug_sheet_contract.py`：11 项通过；`python3 agent/scripts/validate_rule_architecture.py`：`ok: true`。
- ADS-47367 的 J138 已按修复后的脚本重写；`validate-patch --key ADS-47367 --mode review` 返回 `ok: true`，五个短标签各保留一个正确原始入口。
- 未评论 Jira、未转派、未创建需求、未改 Jira 状态；未记录敏感信息。
