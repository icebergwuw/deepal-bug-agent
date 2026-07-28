# 2026-07-28 已有 Bug 行更新模式与列级写入

## 触发

- 用户纠正：普通二次查看同一 Bug 时可以修改原处理列；只有会议纪要等复盘输入才更新 G、H、I、J。
- 本次为规则和工具改造，没有处理具体 Jira Key，没有读取或修改线上 Bug 表，也没有执行 Jira 评论、转派或状态动作。

## 规则结果

- 普通二次复查：可按需更新 C、D、G、I、J；保留 A、B、E、F、H。
- 会议/复盘：可按需更新 G、H、I、J；保留 A、B、C、D、E、F。
- 普通二次复查继续使用 `decision_text` 并更新 D；会议/复盘形成 `final_decision_text` 并更新 H。

## 工具结果

- `agent/scripts/bug_sheet_contract.py` 新增 `snapshot`、`patch` 和 `validate-patch`。
- `patch` 要求完整 A:J 写前回读和 fingerprint，只生成允许列的独立 `updateCells` 请求。
- C、D、H、J 请求明确包含 `userEnteredValue,textFormatRuns`；G、I 只更新 `userEnteredValue`。
- manifest 显示每个目标列的修改前、修改后和链接目标；写后校验确认所有未声明列保持不变。

## 验证

- `python3 agent/scripts/test_bug_sheet_contract.py`：7 项测试通过。
- `snapshot`、`patch`、`validate-patch` 三个 CLI 子命令加载成功。
- `python3 agent/scripts/validate_rule_architecture.py`：`ok: true`。
- `git diff --check`：通过。
