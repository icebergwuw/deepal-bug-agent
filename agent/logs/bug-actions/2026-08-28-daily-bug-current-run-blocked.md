# Daily Bug current run - evidence blocked

- run_id: `bug-20260828T073812Z-2b6b56f6-4b77-4c9c-9650-7a8aab6c6f55`
- operator: `wu-you`
- JQL: `assignee = you.wu AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in (To Do, Reopened, In Progress, Pending) ORDER BY created DESC`
- Jira visible result count: `39`
- Existing registered keys: the previously recorded ten rows remain registered at `bug!399:408` and are not duplicated.
- New unregistered keys: `ADS-49702`, `HUR-83830`, `SD-7244`, `HUR-82934`, `ADS-44267`.

## ADS-49702

- Current Jira read: customer issue `ID20260826172022268`; C673-7; CDC SWD.2.52; To Do; P2; Android - General; complete structured test case; video/RAR/screenshot attachments.
- Actual: charge current 8/10/16/32A produces TTS “掉到”; expected adjustment/set wording; 2/10. Comment identifies “调到/掉到” homophone concern.
- Drive search receipt observed in authenticated UI: query `充电电流 TTS 调整 设置 C673`; candidates included `C673_功能定义_车辆设置功能定义V6.1`, `长安C673 交互设计文档_车辆设置_EV&EVE_v6.1_20250828.pdf`, `长安C673 交互设计文档_车辆设置_EV&EVE_v7.2.pdf`, C673 function lists.
- Blocker: exact current C673-7 TTS/function row and Alchemy standard/project function-point evidence not yet opened and recorded.
- Provisional state: `待复核`; owner route: C673 voice/vehicle-control product owner.

## HUR-83830

- Current Jira read: J90A All; Reopened; P2; Android - SceneMode; OS ending `SWD.05.0-20260823233210`; four image attachments.
- Actual: English low-power door-open prompt truncated; verification on OS ending `20260828042814` still failed 10/10 and showed 10% versus Chinese 20%.
- Implementation evidence: Gerrit review `1131228` for “修复恒温座舱开门提示英文文言显示不全” is `MERGED` on the release branch.
- Drive search receipt observed: query `J90A 恒温座舱 低功耗 开门提示 英文`; candidates included `OTA节点_J90A-标准语料_V0.6.xlsx`, J90A language lists, `J90A_EL接收测试报告_SWB.00.9.xlsx`, and `马自达J90A_情景模式_需求文档_V2.4.pdf`.
- Blocker: exact current language row, applicable version family, release readback and formal target citation not yet completed.
- Provisional state: `待复核`; owner route: J90A SceneMode product owner.

## SD-7244

- Current Jira read: customer issue `ID20260820144228069`; C673-G3G5; SWA.3.64; To Do; P2; Android - Music; 5/5; VIN and SMB log locations present.
- Actual: after normal nap mode, lock/power down, local music starts but speakers are silent; preliminary analysis says amplifier offline.
- Drive search receipt observed: query `C673 恒温座舱 下电 音乐 功放`; candidates included `C673-G3、G5座舱全功清单_V1.7_20260730.xlsx`, `座舱全功清单_20260729173842.xlsx`, C673 vehicle-setting definitions and CDC inspection documents.
- Blocker: exact power-state/audio target and same-version amplifier down-state evidence not yet opened and reconciled.
- Provisional state: `待确认`; owner route: C673 audio/SceneMode product owner.

## HUR-82934

- Current Jira read: J90A EU PI; To Do; AI Cockpit - Voice/General; Swedish camping-mode duration reduction corpus; customer-originated Longma request.
- Actual: Swedish translations do not match the Chinese commands; comments say modified corpus and translation are inconsistent and request product handling.
- Drive search receipt observed: query `J90A 瑞典语 露营模式 时长 减少`; candidates included `OTA节点_J90A-标准语料_V0.6.xlsx`, J90A V0.5/V0.5.5 language files, `J90A_海外LanguageList内部版V1.0_260806`, and EU-PI external language list.
- Blocker: exact Swedish row, customer acceptance, current language-list version and Alchemy standard/project/downlink evidence not yet completed.
- Provisional state: `待确认`; owner route: J90A language/voice product owner.

## ADS-44267

- Current Jira read: customer issue `ID20260602134722264`; C673-6; SWD.3.68; In Progress; P2; Android - General; weather card plus AVM/360 evidence.
- Actual: after weather query and shifting to R, weather card remains above 360; expected AVM/360 highest layer.
- Conflict: historical comments say “设计如此/关闭”; current product comment says AVM should outrank a large card; supplier says AVM is an Activity and layer cannot be guaranteed. Related `ADS-46283` was read.
- Drive search receipt observed: query `天气卡片 360 AVM 层级 C673`; candidates included `Megatronix_地图导航产品需求文档_C385&C673_V6.1`, `长安C673&C385-Components.xlsx`, C673 function lists and 2026 change-management sheet.
- Blocker: current C673-6/C673-7 AVM layer definition and conflict resolution are not yet established.
- Provisional state: `待会诊`; owner route: C673 AVM/visible-layer product owner.

## Write gate

- No online sheet write, index update, Jira comment, assignment, closure or status change was performed.
- No deterministic conclusion is claimed. Exact document opening, per-result real search receipts, version-family enumeration, Alchemy standard/project function points and MasterGo current-layer evidence remain required.
