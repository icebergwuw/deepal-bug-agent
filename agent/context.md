# Context

## 身份

- 工作主体：镁佳 Megatronix 产品组，为长安深蓝汽车提供智能座舱服务。
- 当前操作者：只读取本机 `agent/config/local-profile.json` 的 `operator_owner_id`，再从 `agent/bug-owners/registry.yaml` 解析姓名和负责人范围。
- 首次运行或身份不可验证时按 `agent/onboarding.md` 引导，保持只读，不默认成吴优或其他成员。
- 同事独立使用时，本机档案是 `operator_mode=external`。姓名只能来自对方明确确认，不映射成注册表负责人，也不写入已登记 Bug 表。
- Codex 在该流程中代替已绑定操作者做产品判断，不能把结论写成“产品确认/产品定口径”。

## 固定链接

- Jira：`http://jira.i-tetris.com`
- Jira 单票读取：项目 MCP `analyze_bug_jira` 的 `get_jira_issue`。语音日志是 `analyze_bug_debug`，Alchemy 配置是 `analyze_bug_ops`，判责规则是 `analyze_bug_rules`。启动脚本是 `agent/scripts/analyze-bug-mcp.sh`，运行时在 `agent/vendor/analyze-bug`。Jira 账号放在本机 `.env`；Debug / Alchemy Cookie 由脚本从已登录 Chrome 提取。凭证写到 gitignore 的 `.analyze-bug/`，不进入仓库。
- Bug 清单总入口（Jira Dashboard 17302）：
  `http://jira.i-tetris.com/secure/Dashboard.jspa?selectPageId=17302`
- 工作说明表：
  `https://docs.google.com/spreadsheets/d/1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs/edit?gid=717876892#gid=717876892`
- 工作说明页签：`深蓝8155`
- 深蓝项目变更管理表-2026年：
  `https://docs.google.com/spreadsheets/d/1q_h3iEm4t8RAv9EEjbadm6yMFxoEFGkP9ZYqPlHdPv4/edit?gid=1443256155#gid=1443256155`
- 该链接打开的页签是 `深蓝8295平台（国内）OTA 项目`，`gid=1443256155`。新建需求按原 Bug 的项目选择对应页签，不固定写这一页。表头在第 3 行。产品填写 `功能模块` 和 `JIRA-Story`；序号、提出时间、变更内容、变更阶段、费用申报和涉及车型由 PJM 填写。旧版冻结页签不写。从该表新建需求时，只处理 B 列变更提出时间在当前日期往前一个自然月内的行。经办人按 U 列产品负责人设置：吴优 `you.wu`，李欣 `xin.li03`，冯智秀 `zhixiu.feng`。U 列无法对应已登记负责人时才用当前操作者。不改无关旧票经办人。建票回读成功后用飞书应用 `cli_aa506e13fcf8dcf5` 通知群 `oc_c3692001480b0aac7825bafab90989b3`，配置在 `agent/config/feishu-notify.json`。通知必须带依赖项：缺的 PRD/UE、跨模块依赖、表上已写明的对接人。表上没有对接人时不写死名字。群内称呼：李欣是塞林格，冯智秀是芝芝。机器人目前没有成员读取权限，不能把称呼当成已艾特。

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
