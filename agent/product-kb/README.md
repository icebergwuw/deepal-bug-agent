# Product Knowledge Base

本目录用于沉淀深蓝 / Megatronix 的资料入口、判断方法和历史案例。它不是当前 Bug 的权威事实源，不能代替当前 Jira、生效正式资料或平台实时结果。

## 使用顺序

1. 当前 Bug 的证据深度和来源顺序统一执行 `agent/evidence-contract.md`；本目录不另定义调查流程。
2. 从当前 Jira 提取车型、平台、模块、query、页面、`meta_id` 和责任边界关键词。
3. 用 `rg` 检索本目录补充资料入口、责任边界和相似案例：
   - 模块和负责人：`org/`、`modules/`
   - 处理规则：`rules/`
   - 历史 bug 方法：`bug-methods/`
4. 命中相似案例时只复用检索方法和已确认边界；最终结论仍以当前证据契约要求的实时来源为准。
5. 形成稳定且可回读的结论后，补充到对应模块或案例文件。

## 条目状态

- 新建或实质修改的案例按 `case-template.md` 写元数据：`status`、`last_verified`、`applies_to`、`sources`、`responsible_boundary`、`supersedes`。
- `status` 只用 `draft`、`verified`、`deprecated`、`historical`。
- 旧文件缺少元数据时，默认视为 `historical / 未重新核验`，只能提供检索线索；复用前必须用当前 Jira 和正式资料校正。
- 只有来源可回读、适用范围明确且责任边界清楚的条目才能标为 `verified`。

## 安全规则

- 不在知识库里记录账号、密码、token、测试账号明文。
- 读到包含敏感信息的表格，只沉淀模块、负责人、规则、文档入口，不复述敏感字段。
- MasterGo、Office-backed 表或其他不可直接读的材料，必须标明读取方式和限制。

## 目录

- `sources.md`：外部来源登记。
- `org/`：组织架构、项目经理、模块负责人、组件分流。
- `modules/`：产品模块知识。
- `rules/`：跨模块处理规则。
- `bug-methods/`：历史 bug 判断方法和案例。
- `case-template.md`：新案例元数据和内容模板。
