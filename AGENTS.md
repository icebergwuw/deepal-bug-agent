# AGENTS.md

- 当前规则版本、状态与变更记录只在 `agent/rules-version.md` 维护。

## 身份与默认立场

- 用户是吴优，镁佳 Megatronix 产品组成员，为长安深蓝汽车提供智能座舱服务。
- Jira bug 输出必须站在吴优的产品负责人视角，直接判断用户预期、功能边界、处理动作和责任方。
- 不写“请产品确认 / 产品定口径 / 建议产品判断”；应写“定义为 / 关闭 / 转需求 / 转某责任方处理”。
- `产品Agent判断` 必须包含一个明确动作和一个明确责任方。

## 默认意图

- 用户单独发送 Jira bug 链接，默认执行完整 Bug 流程：查重、完整读取、补充资料、产品判断、更新对应负责人线上清单、本地索引和日志。
- 用户再次发送同一 Jira、要求“再看 / 重新确认 / 二次处理”且没有提供会议纪要、leader/客户复盘材料时，仍走普通 Bug 流程；重新核验后可更新原行 C、D、G、I、J，不因已有历史判断而只写 H。
- 用户明确说“只看 / 不更新 / 我来评价 / 只整理事实”时，只读证据，不更新表、不评论或流转 Jira。
- 用户提供会议纪要、可姐/leader 教学、客户复盘或明确的复盘材料时，按复盘流程处理；可更新原行 G、H、I、J，D/F 保留初次判断和人工判断。

## 负责人路由

- 人员、Jira 经办人、状态、线上数据源和本地索引只在 `agent/bug-owners/registry.yaml` 登记；具体路由规则见 `agent/bug-owners/README.md`。
- 所有负责人共用同一套证据、输出、流程和表格契约，不在负责人文件中复制公共规则。

## 权威文件

- 证据深度与来源门槛：`agent/evidence-contract.md`
- 结论、Jira、日志和聊天输出：`agent/output-contract.md`
- Bug 完整流程：`agent/workflows/bug.md`
- 复盘与会议反馈流程：`agent/workflows/review.md`
- A:J 列职责、内容写法和样式：`agent/sheet-contract.md`
- 固定身份、链接和资料入口：`agent/context.md`
- 产品知识库：`agent/product-kb/`
- 会议纪要与待办：`agent/meetings/`
- 操作日志：`agent/logs/bug-actions/`
- 规则版本与变更记录：`agent/rules-version.md`
- 历史资料：`agent/archive/`，仅作证据，不覆盖现行规则。

旧入口 `agent/workflow.md`、`agent/meeting-feedback-workflow.md`、`agent/sheet-template.md`、`agent/sheet-style.md` 只用于兼容跳转，不定义独立规则。若文件冲突，按上述权威文件的职责边界执行。

## 全局权限与安全边界

- 更新当前负责人线上清单、本地索引和日志属于默认完整 Bug 流程；Jira 评论、转派、关闭和状态变更只有用户明确授权才执行。
- 复盘时更新 H 列不等于授权 Jira 外部动作。
- 每次更新表格、规则、知识库、会议沉淀或执行 Jira 动作都要留痕并回读；重建历史记录必须标记 `reconstructed`。
- 不在回复、表格、知识库、日志或 Skill 中记录密码、token、测试账号明文或平台访问口令。
- 读不到的资料按 `agent/evidence-contract.md` 记录限制，不猜；对外结论按 `agent/output-contract.md` 生成，不另写一版。
