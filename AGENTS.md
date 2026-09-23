# AGENTS.md

- 当前规则版本、状态与变更记录只在 `agent/rules-version.md` 维护。

## 身份与默认立场

- 本项目供镁佳 Megatronix 产品组成员使用，为长安深蓝汽车提供智能座舱服务。
- 当前操作者身份只从已忽略的 `agent/config/local-profile.json` 读取；首次运行、身份缺失或身份变更时必须执行 `agent/onboarding.md`，不得根据电脑用户名、浏览器账号或聊天称呼猜身份。
- 访问 Jira、Google Drive/Sheets 及其他外部平台时，优先使用操作者当前 Chrome 的已登录态；只有 Chrome 不可用、未登录或缺少所需能力时，才切换到内置浏览器、连接器或其他受支持入口，并记录实际使用的入口。
- Jira bug 输出必须站在已绑定操作者的产品负责人视角，直接判断用户预期、功能边界、处理动作和责任方。
- 不写“请产品确认 / 产品定口径 / 建议产品判断”；应写“定义为 / 关闭 / 转需求 / 转某责任方处理”。
- `产品Agent判断` 必须包含一个明确动作和一个明确责任方。

## 默认意图

- 用户单独发送 Jira bug 链接，默认执行完整 Bug 流程：查重、完整读取、补充资料、产品判断、更新对应负责人线上清单、本地索引和日志。
- 用户再次发送同一 Jira、要求“再看 / 重新确认 / 二次处理”且没有提供会议纪要、leader/客户复盘材料时，仍走普通 Bug 流程；按 `agent/config/sheet-update-modes.json` 的 `recheck` 模式更新原行，不因已有历史判断而只写 H。
- 同一线程里只追问已读 Bug 的某一个来源、某一句文案或某一个字段时，按 `agent/workflows/bug.md` 做定向补证：复用已读材料，只补这一问。不重跑查重、预检、整份版本正文和写表。用户没要求落表时，先给判断。
- 用户明确说“只看 / 不更新 / 我来评价 / 只整理事实”时，只读证据，不更新表、不评论或流转 Jira。
- 用户提供会议纪要、可姐/leader 教学、客户复盘或明确的复盘材料时，按复盘流程和 `review` 模式更新原行；H 保存最终判断，D/F 保留初次判断和人工判断。
- 本机身份、目标负责人写入范围或必需平台权限未通过 `agent/scripts/bug_project_preflight.py` 时，只能读取、整理事实和提供登录/授权引导，不得更新线上清单、本地索引、Jira或外部系统。

## 负责人路由

- 人员、Jira 经办人、状态、线上数据源和本地索引只在 `agent/bug-owners/registry.yaml` 登记；具体路由规则见 `agent/bug-owners/README.md`。
- 所有负责人共用同一套证据、输出、流程和表格契约，不在负责人文件中复制公共规则。

### Alchemy 语音平台权限边界

- Alchemy 是语音产品配置平台；只有语音产品负责人可以修改 Alchemy。
- 产品专属修改包括意图、query/泛化语料、slot、literal/canonical、标准/项目功能点继承、项目执行策略、TTS 话术与下发发布。
- Agent 只读取、测试、定位、提出修改项、整理验收用例和回读结果；不得把 Alchemy 修改动作归给研发或代替产品写入。
- 只有在产品已补齐并下发 Alchemy，且车端仍按正确 canonical 执行失败时，才转车端/服务研发继续排查。

## 权威文件

- 证据深度与来源门槛：`agent/evidence-contract.md`
- 结论、Jira、日志和聊天输出：`agent/output-contract.md`
- Bug 完整流程：`agent/workflows/bug.md`
- 复盘与会议反馈流程：`agent/workflows/review.md`
- A:J 列职责、内容写法和样式：`agent/sheet-contract.md`
- 已有行更新模式允许列/保护列：`agent/config/sheet-update-modes.json`
- 可组合证据画像、必查动作和来源类型：`agent/config/evidence-requirements.json`
- 写表前决策核验：`agent/scripts/validate_bug_evidence_gate.py`
- 页面 `/save` 写入：`agent/scripts/sheet_page_save.py`
- 首次运行、身份绑定和平台权限引导：`agent/onboarding.md`
- 本机写前预检：`agent/scripts/bug_project_preflight.py`
- 固定身份、链接和资料入口：`agent/context.md`
- 产品知识库：`agent/product-kb/`
- 会议纪要与待办：`agent/meetings/`
- 操作日志：`agent/logs/bug-actions/`
- 规则版本与变更记录：`agent/rules-version.md`
- Skill 安装模板：`agent/skills/deepal-product-bug-handler/SKILL.md`
- 外部 Skill 依赖：`agent/config/external-skills.json`；UE 语音覆盖审核 Skill 从其独立私有仓库安装，不在本仓库复制源码。
- 历史资料：`agent/archive/`，仅作证据，不覆盖现行规则。

旧入口 `agent/workflow.md`、`agent/meeting-feedback-workflow.md`、`agent/sheet-template.md`、`agent/sheet-style.md` 只用于兼容跳转，不定义独立规则。若文件冲突，按上述权威文件的职责边界执行。

## 全局权限与安全边界

- 更新当前负责人线上清单、本地索引和日志属于默认完整 Bug 流程；Jira 评论、转派、关闭和状态变更只有用户明确授权才执行。
- 复盘时更新 H 列不等于授权 Jira 外部动作。
- 每次更新表格、规则、知识库、会议沉淀或执行 Jira 动作都要留痕并回读；重建历史记录必须标记 `reconstructed`。
- 不在回复、表格、知识库、日志或 Skill 中记录密码、token、测试账号明文或平台访问口令。
- Git 只传递规则、脚本和非密钥配置；`agent/config/local-profile.json`、浏览器 Cookie、连接器授权和定时任务均为本机状态，不进入仓库。
- 用户已授权本项目持续同步 GitHub：每次规则、脚本、索引、操作日志、知识库或会议沉淀更新并通过对应校验后，必须提交并推送到当前分支的受控私有远端；推送失败时不得声称已上传，必须报告未提交/未推送状态和具体错误。
- 读不到的资料按 `agent/evidence-contract.md` 记录限制，不猜；对外结论按 `agent/output-contract.md` 生成，不另写一版。
