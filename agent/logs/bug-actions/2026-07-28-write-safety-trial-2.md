# 2026-07-28 写表安全闭环 trial.2

## 范围

- 用户批准修复严格链接校验、追加顺序、行号与写前新鲜回读、Git 内唯一配置和 Skill 模板。
- 本次没有处理具体 Jira Key，没有修改线上 Bug 表，也没有执行 Jira 评论、转派或状态动作。

## 修改

- 更新模式允许列/保护列迁移到 `agent/config/sheet-update-modes.json`。
- `agent/skills/deepal-product-bug-handler/SKILL.md` 成为 Git 内唯一模板；安装副本必须逐字一致。
- 新增 `sync_bug_skill.py`，默认只检查，`--install` 时才同步安装副本。
- 新增行请求改为复制格式、设置 E 列校验、写入值和富文本链接、自动行高、扩展筛选。
- C、D、H、J 在生成阶段拒绝显示长 URL，链接目标必须是完整 `http(s)` 地址。
- `validate-append` 逐格核验 A:J，并对 C、D、H、J 的所有链接目标做精确对比。
- 已有行 patch 使用 1-based `row-number`；batchUpdate 前必须用当前完整 A:J 与预览 fingerprint 比较。

## 验证

- `python3 agent/scripts/test_bug_sheet_contract.py`：10 项测试通过。
- `patch --help` 仅暴露 1-based `--row-number`，并要求 `--preview-fingerprint`。
- `validate-append --help`：子命令加载成功。
- `python3 agent/scripts/validate_rule_architecture.py`：`ok: true`。
- `python3 agent/scripts/sync_bug_skill.py`：Git 内模板与安装副本完全一致。
- `git diff --check`：通过。
