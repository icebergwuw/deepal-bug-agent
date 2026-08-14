# 2026-08-14 每日新增 Bug 完整处理（写前阻塞）

- Run ID：`bug-20260814T010123Z-213a9634-5bcc-4e03-bf2a-b976f5bd7b04`
- Automation ID：`bug`
- 规则版本：`v1.10.1-trial.1`
- 操作者：吴优（`wu-you`）；目标负责人：吴优；目标页签：`bug`
- 查询时间：2026-08-14 09:01-09:20（Asia/Shanghai）
- JQL：`assignee = you.wu AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in ("To Do",Reopened,"In Progress",Pending) ORDER BY key ASC`
- Jira 实时命中：143 个唯一 Key。
- 吴优线上 `bug` 页实时回读：332 个非空登记、331 个唯一 Key；历史重复仅 `SLV-44272` 两次。
- 逐 Key 去重后新增：10 个。
- 未执行 Jira 评论、转派、关闭或状态变更。

## 本次新增 Key 与 Jira 完整读取结果

### ADS-48614

- Jira 已读：状态 Reopened，C673-7，描述、附件 `logcat.log.053_2026_08_07_16_52_02.gz`、4 条评论、关联票 `ADS-48552`。
- 当前实现事实：POI 卡片历史对话只有 4 个地点；用户说“第六个”后 Claw 下发 `metaId=-7` 并导航到最后一项。AIS 评论称列表中找不到第六个。
- 待补：完整读取关联票；核验 Alchemy 当前原话、标准/项目功能点；打开 POI PRD 和交互候选并定位序号越界条款。
- 当前状态：未形成可写结论。

### ADS-48732

- Jira 已读：状态 To Do，C673-7，描述、视频/日志附件、2 条评论、关联票 `ADS-48730`、`ADS-48465`。
- 当前实现事实：睡眠空间 20 秒无触摸计时到期熄屏，语音状态机进入 Idle 并终止尚未完成的 ASR；同一句正常执行时可下发 `metaId=1147` 和 `1h20m`。
- 待补：完整读取关联票；核验 Alchemy 当前原话、标准/项目功能点；打开睡眠空间 PRD/交互候选并定位熄屏与语音并发规则。
- 当前状态：未形成可写结论。

### BEO-8993

- Jira 已读：状态 To Do，D587-G EVE，描述、视频附件、1 条评论，无直接关联票。
- 当前实现事实：蓝牙电话页车模与轮毂样式和 3D/车辆设置页不一致；评论要求产品给车模原型图。
- 待补：打开 D587-G 电话/车模生效配置、视觉规范和 UE；MasterGo 当前未通过有效期内真实读取验证。
- 当前状态：未形成可写结论。

### HUR-81740

- Jira 已读：状态 To Do，J90A，描述、全部附件、12 条评论，无直接关联票。
- 当前实现事实：回拨列表页说“第一个”时云端/可见/本地 DS 仲裁存在冲突；本地生成 PHONE `callConfirm`，最终未执行。最新评论认为命中可见正确，若保留序号选择需处理能力边界。
- 待补：核验 Alchemy 当前原话、标准/项目功能点；打开蓝牙电话 PRD、J90A 可见配置和 UE，确认列表确认页序号选择目标。
- 当前状态：未形成可写结论。

### HUR-82887

- Jira 已读：状态 To Do，J90A，描述、2 个日志附件、4 条评论；日志入口关联 `HUR-82884`。
- 当前实现事实：未导航时“打电话给亚朵酒店”被云端直接解析为 PHONE `callConfirm` 并进入 5 秒自动拨号倒计时；附件中用户取消，未形成真实外呼。评论给出蓝牙电话 PRD入口并质疑测试预期。
- 待补：完整读取 `HUR-82884`；打开 `AIS_语音蓝牙电话产品需求文档_v2.7` 指定章节；核验 Alchemy 当前原话、标准/项目功能点和 POI/机构路由规则。
- 当前状态：未形成可写结论。

### HUR-83012

- Jira 已读：状态 To Do，J90-ER 0616，描述、视频/日志附件、2 条评论，无直接关联票。
- 当前实现事实：来电设置为播报后未播报“接听还是挂断”且未唤醒语音球；研发称 0616 不处理且原设计没有该句播报。
- 待补：打开蓝牙电话 PRD和来电播报配置，核验目标文案、适用分支和交互阶段。
- 当前状态：未形成可写结论。

### HUR-83099

- Jira 已读：状态 To Do，J90A，描述、视频/日志附件、1 条评论，无直接关联票。
- 当前实现事实：Jira 只写“退出儿童模式时 TTS 播报异常”，预期字段也写成“嗨字播报异常”，未描述完整预期、实际原话或可复查时间码。
- 待补：向测试收集完整复现用例、实际 TTS 原话和视频时间码；打开儿童模式 PRD/语音定义并核验 Alchemy。
- 当前状态：待确认，资料不足，未形成可写结论。

### HUR-83103

- Jira 已读：状态 To Do，J90A-EL 阿拉伯语，描述、图片及 LanguageList 附件、2 条评论，无直接关联票。
- 当前实现事实：Android Auto 切换蓝牙弹窗的阿拉伯语文言缺失；评论未提供 TextID/Key，只确认所有语言文言表缺失。
- 待补：从附件和当前生效 `J90A_海外LanguageList内部版V1.0_260806` 定位 TextID/Key、阿拉伯语行号和弹窗 UE。
- 当前状态：待确认，缺 TextID/Key，未形成可写结论。

### HUR-83119

- Jira 已读：状态 To Do，J90A-EL 英语，描述、图片及 LanguageList 附件、2 条评论，无直接关联票。
- 当前实现事实：Android Auto 切换蓝牙弹窗的英语文言缺失；评论未提供 TextID/Key，只确认所有语言文言表缺失。
- 待补：从附件和当前生效 `J90A_海外LanguageList内部版V1.0_260806` 定位 TextID/Key、英语行号和弹窗 UE。
- 当前状态：待确认，缺 TextID/Key，未形成可写结论。

### SLV-44574

- Jira 已读：状态 To Do，C673，描述、图片/视频附件、2 条评论；日志指向 `SLV-44564`。
- 当前实现事实：蓝牙电话通话记录数据未同步态的“同步”按钮，query“同步”未执行可见；评论称未定义该可见语言。
- 待补：完整读取 `SLV-44564`；核验 Alchemy 当前原话、标准/项目功能点；打开深蓝8295可见配置和 UE，定位按钮节点与语料；MasterGo 当前未通过有效期内真实读取验证。
- 当前状态：未形成可写结论。

## Drive 检索与候选审计状态

- 已在当前登录的 Google Drive 执行真实检索。检索 `第六个 选择超出范围 POI` 返回 0；扩大为 `POI` 后实际命中多个强候选，包括：
  - `长安深蓝_8295平台_大模型产品需求文档_POI推荐_v0.8`（Drive id `1JajU_yrr2lTthOThyHuqexPP4PO5MOGmVNVMHNsxjmc`）
  - `mega claw 导航agent 花瓣地图不支持能力清单`（Drive id `1WspNNtgcMJnnrOjRMp5H1X6ADDQxOB4BATYbyvxvyrw`）
  - `AIS_语音蓝牙电话产品需求文档_v2.7`（Drive id `1V3TC1qm3IqLN1qABKereetThkKPbdOqgkrUxzeSYsDc`）
  - `J90A_海外LanguageList内部版V1.0_260806`（Drive id `1ASnEMB3HSNClw2MRbsA1tGDaB9Y5Vi_dXL9hZzz7gC4`）
  - `深蓝8295可见新表—非3DV1.0`（Drive id `1igZUJg_CV2Jb7kCTSz0zZvxtrojbLXTBdzs2ee92X2Q`）
- 扩大检索还返回工作说明、备份 LanguageList、产品分工、记忆空间等非本票强候选；候选尚未逐项打开/排除，不能写 `results_count=0`，也未生成 schema v4 `search_receipts`。

## 阻塞与未执行动作

- 当前运行环境没有 Google Drive/Sheets 结构化连接器或 Google Sheets API 凭据；可用浏览器只能读取可见值。
- 线上清单可以通过 gviz 实时回读 Key，但无法用该入口校验公式、富文本链接、BOOLEAN、保护列、格式、筛选范围和原始 A:J。
- 按 `agent/sheet-contract.md` 与 Skill 的 fail-closed 要求，不用浏览器 UI 粘贴代替契约写入，不伪造原始 A:J 回读、`readback_sha256` 或 final run bundle。
- 因写入/回读能力缺失，且 Drive 候选、Alchemy、MasterGo及关联票尚未全部完成，本次未进入 schema v4 证据门禁、prewrite run bundle校验或线上写表。
- 为确认阻塞状态，已对 planned bundle 执行一次 prewrite 校验；校验拒绝空 `items`，错误为“有写入计划的 run 必须包含 items”。该失败如实保留，不把 planned bundle伪装为已通过的 prewrite/final bundle。
- 未更新 `agent/bug-owners/wu-you/index.md`，避免本地索引先于线上主数据。
- 未执行任何 Jira 评论、转派、关闭或状态变更。

## 本地校验

- `validate_rule_architecture.py`：通过。
- `test_bug_evidence_gate.py`：28 项通过。
- `test_bug_run.py`：3 项通过。
- `test_bug_sheet_contract.py`：16 项通过。
- `test_bug_project_preflight.py`：7 项通过。
- JSON 语法、`git diff --check` 和新增内容敏感字段扫描：通过。
- `validate_bug_run.py --phase prewrite`：未通过，唯一错误为 planned bundle 无 items；原因和影响见上文。

## 恢复条件

- 在自动化运行环境启用可结构化调用的 Google Drive/Sheets 连接器，至少支持 Drive search/open、Sheets get_cells/get_metadata/batchUpdate 和原始 A:J 回读。
- 恢复后继续使用本 Run ID 或明确建立新的补跑 Run ID，逐票完成候选审计、Alchemy/MasterGo/关联票核验、schema v4 manifest、prewrite/final bundle、写表和回读；不得把本日志视为已处理完成。
