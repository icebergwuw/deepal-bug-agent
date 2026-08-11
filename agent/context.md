# Context

## 身份

- 工作主体：镁佳 Megatronix 产品组，为长安深蓝汽车提供智能座舱服务。
- 当前操作者：只读取本机 `agent/config/local-profile.json` 的 `operator_owner_id`，再从 `agent/bug-owners/registry.yaml` 解析姓名和负责人范围。
- 首次运行或身份不可验证时按 `agent/onboarding.md` 引导，保持只读，不默认成吴优或其他成员。
- Codex 在该流程中代替已绑定操作者做产品判断，不能把结论写成“产品确认/产品定口径”。

## 固定链接

- Jira：`http://jira.i-tetris.com`
- Bug 清单总入口（Jira Dashboard 17302）：
  `http://jira.i-tetris.com/secure/Dashboard.jspa?selectPageId=17302`
- 工作说明表：
  `https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=717876892#gid=717876892`
- 工作说明页签：`深蓝8155`
- 语音平台功能分类：
  `https://alchemy.i-tetris.com/#/functional/classify`
- 语音平台在线对话测试：
  `https://alchemy.i-tetris.com/#/conversation/testing?id=27475f07-6fc5-47dc-bd3a-af07750b1683&env=`

所有负责人的状态、线上页、Jira 账号和本地索引统一从 `agent/bug-owners/registry.yaml` 进入，不在本文件复制人员或表格配置。

## 当前边界

- 主数据源、负责人路由和索引边界见 `agent/bug-owners/registry.yaml` 与 `agent/bug-owners/README.md`。
- 证据时效、Alchemy、MasterGo 和专项资料核验见 `agent/evidence-contract.md`。
- 可复用资料入口、日期基线和历史检索结果见 `agent/product-kb/sources.md`；它们只作线索，不是当前 Bug 的默认结论。
- 结论和用户回复格式见 `agent/output-contract.md`。
