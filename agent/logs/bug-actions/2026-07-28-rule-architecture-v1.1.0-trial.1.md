# Bug 规则架构 v1.1.0-trial.1

- 日期：2026-07-28
- 操作类型：规则维护 / Skill 更新 / 机械脚本修复
- 涉及 Jira：无；ADS-47367 仅作为既有 C/D/J 富文本与 D 原文结构的回归参考
- Jira 动作：未评论、未转派、未关闭、未修改状态
- 线上表格动作：未读取、未写入

## 架构变更

1. 新增 `agent/evidence-contract.md`，成为证据分类、来源优先级、专项资料、Alchemy、MasterGo 和结论门槛的唯一权威文件。
2. 新增 `agent/output-contract.md`，成为 `decision_text`、`final_decision_text`、D/H、Jira、日志和用户回复格式的唯一权威文件。
3. 精简 `AGENTS.md`：只保留身份、默认意图、负责人入口、权威文件导航和全局权限/安全边界。
4. 精简 `agent/workflows/bug.md` 与 `agent/workflows/review.md`：只保留各自执行顺序，证据和输出改为引用契约。
5. 精简 `agent/sheet-contract.md`：只保留 A:J 字段、富文本链接、样式和写后回读，不再定义聊天格式。
6. 精简 `agent/context.md`：移除与负责人注册表重复的 Bug 表配置，把日期模块基线迁移到 `agent/product-kb/sources.md`。
7. 四份负责人索引移除重复路由段落，只保留数据与统一入口引用。
8. 精简 `/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`：Skill 只加载项目权威规则和适配工具，不复制业务规则。
9. 版本升级为 `v1.1.0-trial.1`；具体当前版本只在 `agent/rules-version.md` 维护。

## 写表脚本修复

- `agent/scripts/bug_sheet_contract.py` 不再生成多个 `HYPERLINK(...)` 拼接。
- J 列改为每行一个短标签、每个标签独立富文本链接。
- 新增 `info_links`、`judgment_links`、`review_links`，支持 C/D/H 原位可点击证据。
- 富文本 `startIndex` 按 Google Sheets 使用的 UTF-16 code unit 计算，并加入非 BMP 字符回归。
- build 明确只用于追加新行；更新已有 Bug 必须做列级定向写入，避免覆盖 F/H。
- validate 新增旧多 HYPERLINK 拼接和 C/D/H/J 可见长 URL 拒绝。
- 新增 `agent/scripts/test_bug_sheet_contract.py` 和 `agent/scripts/validate_rule_architecture.py`。

## 验证与回读

- `PYTHONDONTWRITEBYTECODE=1 python3 agent/scripts/test_bug_sheet_contract.py`：3 项测试通过。
- `PYTHONDONTWRITEBYTECODE=1 python3 agent/scripts/validate_rule_architecture.py`：`ok: true`，0 错误。
- Skill 官方 `quick_validate.py` 因当前 Python 环境缺少 PyYAML 未能直接运行；未安装新依赖。已按其源码执行等价 YAML/frontmatter 校验，结果 `Skill is valid!`。
- 当前规则版本检索只命中 `agent/rules-version.md`。
- 当前权威文件的本地路径引用校验通过。
- 六个旧入口均保持 5 行兼容跳转，没有独立业务规则。
- 未生成 `__pycache__`。

## 回滚边界

- 若新职责拆分导致执行遗漏，恢复 `v1.0.0-trial.3` 的工作流与表格规则内容，并保留本日志。
- 不恢复脚本的多 HYPERLINK 拼接；必要时停用 build，继续使用经过回读的定向富文本写入。
