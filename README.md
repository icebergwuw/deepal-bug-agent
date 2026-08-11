# Megatronix Bug Product Agent

深蓝智能座舱 Bug 的产品分析工作区。新 session 先读根目录 `AGENTS.md`，再按任务类型进入对应文件。

首次克隆到新电脑时，先执行 [团队首次运行与权限引导](agent/onboarding.md)。未绑定本机身份并通过写前预检前，项目保持只读。

## 当前入口

- 身份、默认意图、负责人路由、权限边界：`AGENTS.md`
- 首次运行、身份绑定、权限检查和迁移：`agent/onboarding.md`
- 证据深度、来源优先级和关闭门槛：`agent/evidence-contract.md`
- 结论、Jira、日志和聊天输出：`agent/output-contract.md`
- Bug 调查和更新流程：`agent/workflows/bug.md`
- 复盘、会议反馈和待办流程：`agent/workflows/review.md`
- 线上 Bug 表 A:J 契约：`agent/sheet-contract.md`
- 已有行更新模式白名单：`agent/config/sheet-update-modes.json`
- 可组合证据画像、必查动作和来源类型：`agent/config/evidence-requirements.json`
- 固定链接和背景资料：`agent/context.md`
- 负责人注册表、状态和索引：`agent/bug-owners/registry.yaml`、`agent/bug-owners/`
- 产品知识库：`agent/product-kb/`
- 会议纪要和待办：`agent/meetings/`
- 操作日志：`agent/logs/bug-actions/`
- 机械写表与校验脚本：`agent/scripts/`（仅保留架构校验登记的可复用脚本；写表请求必须绑定已通过的同 Jira manifest）
- Git 内 Skill 唯一模板：`agent/skills/deepal-product-bug-handler/SKILL.md`
- 历史快照和培训材料：`agent/archive/`

## 数据边界

- 线上负责人页是 Bug 当前主数据源，本地负责人索引用于快速查重和定位行号。
- 仓库包含公司内部 Bug 信息和资料入口，只允许上传到访问受控的私有仓库；不得公开发布。
- Git 不保存任何 Token、密码、Cookie、连接器授权或本机身份文件；各电脑必须独立完成平台登录与权限验证。
- 同一 Jira 可以因负责人流转出现在多个负责人页；只检查同一页内重复。
- 历史快照、会议原稿和培训材料不能替代当前 Jira、正式资料或现行规则。
- 历史一次性批量构建脚本只保存在 `agent/archive/scripts/` 供审计，不得用于当前 Bug 处理或绕过现行门禁。
- 旧入口文件仍保留用于兼容，但只跳转到当前权威文件。
- 每个 Bug 的完成条件包括逐 Jira 日志；只写批量范围、不列 Jira key 的任务不算完成。
- 新建或普通复查 Bug 在形成确定性结论前，须完成关联票核验，并在日志留存决策核验卡；核验字段和门槛以 `agent/evidence-contract.md` 为准。

## 文件职责

- 证据语义、来源优先级和结论门槛只在 `agent/evidence-contract.md` 维护。
- 证据画像、必查动作和来源类型枚举只在 `agent/config/evidence-requirements.json` 维护。
- 结论和各渠道输出规则只在 `agent/output-contract.md` 维护。
- 执行顺序只在 `agent/workflows/` 维护。
- 列职责和写表校验只在 `agent/sheet-contract.md` 维护。
- 更新模式的允许列和保护列只在 `agent/config/sheet-update-modes.json` 维护。
- 已安装 Skill 必须与 `agent/skills/deepal-product-bug-handler/SKILL.md` 完全一致。
- 人员和线上数据源只在 `agent/bug-owners/registry.yaml` 维护。
- 其他文件只能引用这些权威入口，不复制一套规则。
