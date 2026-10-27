# Review And Meeting Workflow

这是会议纪要、可姐/leader 教学、Bug 复盘和客户后续反馈的唯一流程文件。

## 执行权限

- 首先按 `agent/onboarding.md` 和 `agent/scripts/bug_project_preflight.py` 核验本机身份、目标负责人写入范围及 Jira/Google Drive 权限；未通过时只整理复盘事实和权限引导，不写表。
- 先提炼结论更新、当前操作者待办、Agent 准确率和可沉淀规则。
- 用户给出会议纪要、可姐/leader 教学、客户复盘或明确复盘材料时，可按 `agent/config/sheet-update-modes.json` 的 `review` 模式更新对应负责人原行，并同步会议文件、待办和必要知识库。吴优 `result_output=jira_comment_only` 时不回填吴优 bug 表；复盘结论在 `agent/scripts/authorize_jira_comment.py` 通过后，以当前 H 原文评论到该票。
- Jira 外部动作遵守 `AGENTS.md` 的全局权限边界；写 H 列不代表已执行 Jira 动作。

## 标准输出

1. `结论更新`：逐个 Jira 写最终产品结论、责任方、与旧判断的差异。
2. `当前操作者待办`：写可直接执行的评论、转派、建需求、拉群或补资料动作。
3. `准确率标注`：Agent 旧判断为对、错或待定，并说明关键原因；E 列仍由人工勾选。
4. `规则沉淀`：只沉淀可复用、证据明确的方法。
5. `待补信息`：列出仍会改变判断的未知项。

每个 Bug 的证据复核按 `agent/evidence-contract.md`；复盘同样形成当前要求的 `schema_version=5` manifest，使用 `agent/config/evidence-requirements.json` 完成全部画像和必查资料，并在写 H 或评论 H 前通过 `agent/scripts/validate_bug_evidence_gate.py`。评论 H 前还要通过 `agent/scripts/authorize_jira_comment.py`。标准结论、Jira 草稿和聊天复用按 `agent/output-contract.md`。

## Bug 表更新

- `result_output=jira_comment_only` 跳过本节表格写入。复盘仍形成当前 H 原文，经 `authorize_jira_comment.py` 和 `validate_bug_run.py --phase comment` 后评论到该票。不改 G/H 单元格。
- 先按 Jira 和负责人定位原行，不新增重复行。
- 后续反馈会改变原判断时，按证据契约重新读取当前 Jira 和决定性正式资料，重新判断全部证据画像并完成必查资料；不能仅凭一句研发或客户转述覆盖原结论。
- 复盘 manifest 的 `decision.text` 使用本轮 `final_decision_text`，确定性和待定状态均须通过同一证据门禁后才能写 G/H；客户或 leader 的明确最终结论可作为 `customer_final_decision`，但不能替代与结论有关的当前实现事实。
- 保留 D 列原始 Agent 判断和 F 列人工判断，最终处理写 H 列。
- H 写入 `agent/output-contract.md` 定义的 `final_decision_text`。
- 客户接受现有方案时，H 写“接受现状/结束跟进”，不能写成“已修复”。
- G 按复盘后的实际下一步更新为对应短状态；修改表格 G 不等于修改 Jira 状态，E 仍由人工勾选。
- H 列内容和链接按 `agent/sheet-contract.md` 写入并回读。
- I 写复盘后仍存在的唯一风险或门槛；J 汇总支撑 H 的原始可访问入口。C/D 保留普通处理阶段记录，详细复盘过程留在会议文件和操作日志。
- 复盘指出此前漏识别客户问题编号或漏收客户测试用例时，按证据契约将 G 改为 `待确认`，H 写向客户收集完整用例后复核；保留原 D/F 作为初次判断记录。

## 会议文件

- 每次会议在 `agent/meetings/` 新建 `YYYY-MM-DD-主题.md`。
- 同步更新 `agent/meetings/action-items.md`，待办必须有来源、负责人、状态和下一步。
- 原始长文本、旧表结构和历史颜色说明放 `agent/archive/`；现行证据、输出、流程和表格规则分别以对应权威契约为准。
- 规则变化更新对应权威文件或 `agent/product-kb/`，同时写操作日志。

## 会议纪要结构

1. 会议信息
2. 一句话结论
3. 结论更新
4. 当前操作者待办
5. Jira 注释草稿
6. 准确率标注
7. 规则沉淀
8. 待补信息

## 转需求记录

判断和建票分开。先按 `agent/evidence-contract.md` 证明当前正式定义没有覆盖目标行为，才能标 `转需求` 或 `转需求评估`。平台已有能力但说法、槽位或项目继承缺失时转语音或 NLU，不新建需求。现有功能点应支持但映射错误时按缺陷处理。低频或不符真实使用流程时，不转需求；缺正式边界或客户用例时保持 `待确认`，不直接关闭。

建票前用 Jira 搜索同类 Bug 和已有需求。已有需求覆盖时不新建，评论引用该需求链接。没有覆盖时按下面四步，不把原 Bug 改成需求：

1. 新建需求。标题与原 Bug 对齐，按系统责任边界拆票。背景写 `bug转需求`。描述写功能点、query、当前行为和目标行为。语音类同时写 `meta_id` 和 Alchemy 功能点链接。
2. 原 Bug 与新需求建立关联。多张需求票互相链接。
3. 原 Bug 按 workaround / bug转需求关闭。只关闭这一条已判定转需求的原 Bug，不改经办人。
4. 原 Bug 评论仍用当前 D 或 H。处理句写明转需求原因、新需求链接和关闭口径，不另写一套评论格式。

新建需求先登记到 `agent/context.md` 的深蓝项目变更管理表-2026年，按原 Bug 项目选择页签，不固定写 `gid=1443256155`。只填产品负责的 `功能模块` 和 `JIRA-Story`；PJM 列不代填。旧版冻结页签不写。从变更管理表新建需求时，只处理 B 列「变更提出时间」落在当前日期往前一个自然月内的行。未写年份时按工作簿年份解析；解析后晚于今天则减一年。无法解析日期、已有 Jira key、已完成、废弃、重复、待报价或内部 bug 的行不新建。
这类新建需求的经办人按变更表 U 列产品负责人设置，创建时显式指定，不留空让组件默认经办人接管。吴优对应 `you.wu`，李欣对应 `xin.li03`，冯智秀对应 `zhixiu.feng`。U 列无法对应已登记负责人时才用当前操作者。这不授权修改无关旧票经办人；用户明确纠正刚建出的票时，可以改那张票的经办人。
修复版本、合同或 AP Link、评审计划没有当前项目规则时停止建 Jira，不沿用东风样例。2026-10-23 吴优已授权这四步；Jira MCP 没有建票和流转接口，用同一 Jira 凭证走 REST，完成后回读需求票、关联、原 Bug 状态和变更表对应行。回读成功后用 `agent/scripts/notify_feishu_ticket.py` 向 `agent/config/feishu-notify.json` 记录的飞书群发一条，内容含票号、标题、链接、经办人、变更表序号和依赖项。依赖项写缺的 PRD/UE、跨模块依赖，以及变更表上已经写明的对接人。表上没有对接人时不写死名字，只写待指定。没有 open_id 时不得声称已艾特。应用 ID 是 `cli_aa506e13fcf8dcf5`，群 ID 是 `oc_c3692001480b0aac7825bafab90989b3`。App Secret 只放 gitignore 的 `agent/config/feishu-bot.local.json`，不写入规则、日志或仓库。发送失败不得声称已通知。

## HUR 文言与语料

已判定的长马文言和语料分开处理关票和转需求 story，规则见 `agent/product-kb/rules/hur-translation-parent.md`。关票是一定的：原 Bug 评论后按 Workaround / bug转需求关闭，不改经办人。转需求 story 未传递给开发、经办人仍是 `you.wu` 时复用，不新建；已传递给开发才新建。长马文言和语料都这样判断。不因为经办人是吴优就关闭或新建全部票。

文言当前总票只从 `agent/context.md` 读取。执行前回读它仍未完成且经办人仍是 `you.wu`。总票已交给开发或不再收翻译问题时，先新建并改 context，不得把历史总票号写死。语料复用仍在 `you.wu` 名下、覆盖同一问题的 story，不把历史语料票写成永久总票。

不写变更管理表，不发飞书建票通知，不回填吴优 bug 表。语音执行、TTS 截断和故事票不走这条。分类不确定时不关闭。
