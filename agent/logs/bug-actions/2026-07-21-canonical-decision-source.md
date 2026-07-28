# 2026-07-21 Bug 结论单一来源修复

## 问题

- 同一 Bug 的表格 D 和聊天回复此前分别自由生成，导致表格偏技术流转语言、聊天偏用户语言，结论含义相同但可读性和措辞不一致。
- D 列字数要求只会放大压缩倾向，不是根因；根因是缺少唯一标准结论和写后文本一致性校验。

## 结构修复

- 每个 Bug 先形成 `cause_text`、`decision_text`、`status`、`boundary_text`、`technical_evidence`。
- `decision_text` 只生成一次并原样写入 D；技术根因写 C，执行日志写本地日志/J。
- 完整流程的聊天回复只能复用线上回读的 D，不再二次概括。
- 复盘时 H 是 `final_decision_text`，复盘摘要和聊天回复只能复用回读的 H。
- 移除针对 ADS-47165 的术语黑名单式示例和 D 列数字字数目标，避免继续按个案叠加规则。

## 更新位置

- `agent/sheet-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`

## 外部动作

- 未修改 Jira、未评论、未转派、未变更 Jira 状态。
- 本次未修改线上 Bug 数据，只修复后续生成与交付结构。

## 回读校验

- 已确认 Bug 流程、复盘流程、表格契约和 Skill 均使用同一 `decision_text` / `final_decision_text`。
- 已确认旧的 D 列数字字数目标、ADS-47165 个案术语黑名单和复杂交互示例已从现行契约移除。
