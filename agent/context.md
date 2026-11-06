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
- 该链接打开的页签是 `深蓝8295平台（国内）OTA 项目`，`gid=1443256155`。新建需求按原 Bug 的项目选择对应页签，不固定写这一页。表头在第 3 行。产品填写 `功能模块` 和 `JIRA-Story`；序号、提出时间、变更内容、变更阶段、费用申报和涉及车型由 PJM 填写。旧版冻结页签不写。从该表新建需求时，只处理 B 列变更提出时间在当前日期往前三个自然月内的行。经办人按 U 列产品负责人设置：吴优 `you.wu`，李欣 `xin.li03`，冯智秀 `zhixiu.feng`。U 列无法对应已登记负责人时才用当前操作者。不改无关旧票经办人。建票回读成功后用飞书应用 `cli_aa506e13fcf8dcf5` 通知群 `oc_c3692001480b0aac7825bafab90989b3`，配置在 `agent/config/feishu-notify.json`。通知必须带依赖项：缺的 PRD/UE、跨模块依赖、表上已写明的对接人。表上没有对接人时不写死名字。群内称呼：李欣是塞林格，冯智秀是芝芝。机器人目前没有成员读取权限，不能把称呼当成已艾特。
- 2026-11-05 起，用户说绑 UI Task 时复制原票：标题加 `-UI`，类型改为任务，字段沿用原票，Relates 关联原票，不改原票。UE 新增、替换或内容变更时先提醒建 UI Task，未要求前不自动建。
- `深蓝8155平台（海外）G3/G5/G6 项目` 是 `gid=508121302`。这一页表头在第 2 行，Story 回写 G 列，产品负责人在 H 列。2026-11-02 回读本页已发变更票 `SD-8172`：Epic 是 `SD-11`（ECR_待签署），未发布修复版本只有 `C673-G5_OTA1_20261230`，车型 `C673`。国家字段只能单选，该票和 Epic 都是欧洲；表上多地区勾选为是时，描述必须写明范围不因此收窄。不要套 `ADS-7`，也不要另造 G3/G6 版本。用户当次明确放宽时间窗口时，才可以超出三个月。回写 `StoryID/TaskID` 必须是超链接，显示票号，指向 `http://jira.i-tetris.com/browse/<KEY>`，不能写纯文本。8295 国内 OTA 页的 D 列同样写超链接。

- 长马标准语料只有一张在线表：`OTA节点_J90A-标准语料_V1.0`，`https://docs.google.com/spreadsheets/d/1ny5OwV4Jrnjl1xFKxV-O16YiAWuv8L--/edit?gid=1437153171#gid=1437153171`。HUR 语料问题先查这张表的对应语种页，不另找第二份语料。2026-10-23 用 Chrome 已登录态导出核对，小憩和露营时长在 `1_英语`。
- 深蓝语料表是 `【正式版】长安系_海外各国语料清单汇总`，`https://docs.google.com/spreadsheets/d/159bd_jBCou9dmXZNEH8y_cQQiMKmUj7rJoVHMl2d1SI/edit?gid=1845215852#gid=1845215852`。2026-11-02 吴优指定这张表，Google API 读到的标题是 `V0.3.2.17`，指定页签是 `深蓝-删减版`。深蓝语料问题先查这张表，不把长马语料表拿来代替。版本会更新，不把 `V0.3.2.17` 写成永久版本。表格标题可以落后于「版本记录」，当前版本只看「版本记录」最后一版。
- 2026-11-06 起，新增深蓝海外语料按 SD-8240 的做法。只追加「深蓝-删减版」最后一个非空行之后，不写「深蓝」全量页，除非用户当次明确要求。同一工作簿「版本记录」按一句一行追加。版本号接最后一版递增，日期用操作当天，修订人写吴优，Jira 列写原票链接。第一行「修订内容」写本次新增摘要。中文一行一句。先查语音专业语料；专业文档已有的说法用专业文档，不用票面概括句代替。专业文档没有的关闭句或页面，按当次票面补，并在版本记录备注写明缺口。车型点只打当次项目对应列：SD 的 C673-G3/G5/G6 只打 `C673-G`，`一代` 和 `D587-G` 写 `-`。页面类模块用 `页面打开`，子模块用 `页面`。没有已审校的其他语种译文时，按表内同类打开/关闭句式补齐，并写明不是另一份已审校译文。不改表格标题。不评论、不转派、不改 Jira，不发飞书。

- 海外 LanguageList / Text ID 查当前 Key、中文、模块和译文时只看 `01`–`21`，不看 `All Key`。`All Key` 有而 `01`–`21` 没有，按当前 Text ID 未收录。2026-11-06 吴优确认。这不替代另一本 `J90A_AllKey_静态补齐多语言` 工作簿。
- 当前 HUR 翻译总票：`HUR-85390`。2026-10-27 回读仍是待办，经办人 `you.wu`，标题是 `[翻译][BUG转需求]Text ID V1.3将提交翻译问题0923`，尚未传递给开发。执行前必须再回读它仍未完成且经办人仍是 `you.wu`。用户给出新总票，或这张已关闭、已解决、不再收翻译问题，或经办人不再是 `you.wu`，都视为已传递给开发，先改这一行再关联，不得沿用旧票号。处理规则见 `agent/product-kb/rules/hur-translation-parent.md`。国内文言不进这张总票，也不进海外 TextID 清单。修复版本含「国内」即排除，已见 `J90A国内26年OTA版本发布`。
- 长马语料没有永久总票。2026-10-27 回读时，`HUR-84627` 和 `HUR-86245` 仍由 `you.wu` 持有，只覆盖小憩和露营，不是所有语料的承接票。同一问题先复用经办人仍是 `you.wu` 的 story；已传递给开发才新建，新建后改这里的当次票号。

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
