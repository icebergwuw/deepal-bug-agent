# Daily Bug Recheck - 2026-08-28

## Run

- run_id: `bug-20260828T072800Z-new-current`
- operator: `wu-you`
- Jira JQL: `assignee = you.wu AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in (To Do, Reopened, In Progress, Pending) ORDER BY created DESC`
- Jira current result count: 39 (visible pagination: 1 of 39)
- Online Wu You sheet/index dedupe: five current keys are not present in the local index: `ADS-49702`, `HUR-83830`, `SD-7244`, `HUR-82934`, `ADS-44267`. Existing ten keys remain registered at rows 399-408 and are recheck candidates.
- External Jira actions: none. Sheet writes: none. Alchemy writes: none.

## New Keys

### ADS-49702

- Jira current: customer issue `ID20260826172022268`; C673-7; CDC SWD.2.52; Android - General; status To Do; priority P2; customer label; attachment video, RAR and screenshot.
- Complete Jira description read: ON/P gear; query charge current 8/10/16/32A; expected adjustment/set wording; actual TTS says “掉到”; reproducibility 2/10.
- Current comment: “调到” homophone “掉到”, asking whether wording needs change.
- Drive real search queries: `充电电流 TTS 调整 设置 C673`.
- Candidate titles observed: `C673_功能定义_车辆设置功能定义V6.1`, `长安C673 交互设计文档_车辆设置_EV&EVE_v6.1_20250828.pdf`, `长安C673 交互设计文档_车辆设置_EV&EVE_v7.2.pdf`, `座舱全功清单_C673-7_华为车型_20251205.xlsx` and other C673 vehicle-setting/function-list files.
- Gate: blocked pending opening the selected current C673-7 candidate and locating exact TTS/function-point row plus current Alchemy standard/project function evidence.

### HUR-83830

- Jira current: J90A All; OS `j90a-cdc-release_huron_hqx.1.2.1_20250526...SWD.05.0-20260823233210`; Android - SceneMode; status Reopened; priority P2; four image attachments.
- Complete Jira description read: English mode, low-power mode, door-open prompt; expected complete copy; actual prompt truncated; verification 10/10 on `...20260828042814`, translation showed 10% while Chinese showed 20%. Gerrit review `1131228` is MERGED for fixing English prompt truncation.
- Drive real search queries: `J90A 恒温座舱 低功耗 开门提示 英文`.
- Candidate titles observed: `J90A-(EU+ER)车机文言_(4+23种语言)_V0.5...`, `OTA节点_J90A-标准语料_V0.6.xlsx`, `J90A_EL接收测试报告_SWB.00.9.xlsx`, `J90A_EU-PI_LanguageList外发版...`, `马自达J90A_情景模式_需求文档_V2.4.pdf`.
- Gate: blocked pending exact current-language row/section, version-family selection and release readback.

### SD-7244

- Jira current: customer issue `ID20260820144228069`; C673-G3G5; SWA.3.64; Android - Music; status To Do; priority P2; 5/5; VIN present; customer asks product-side review.
- Complete Jira description read: normal nap mode, lock/power down, play local music; expected playback; actual speakers silent; preliminary note says amplifier offline.
- Drive real search queries: `C673 恒温座舱 下电 音乐 功放`.
- Candidate titles observed: `C673-G3、G5座舱全功清单_V1.7_20260730.xlsx`, `座舱全功清单_20260729173842.xlsx`, `C673_功能定义_车辆设置功能定义V6.1`, `C673-5 项目CDC_电检文档V1.6 20241209.xlsx`.
- Gate: blocked pending exact power-state/audio target and same-version amplifier down-state evidence; customer test case is complete enough to continue but no deterministic conclusion yet.

### HUR-82934

- Jira current: J90A EU PI; OS `j90a_eu_pi-cdc-release_huron_hqx.1.2.1_20260109...SWD.00.3-20260806235852`; AI Cockpit - Voice/General; status To Do; customer-originated Swedish language request.
- Complete Jira description read: Swedish mode; camping-mode duration reduction commands; expected Chinese/Swedish consistency; actual mismatch. Comments say modified corpus and translation do not match and identify it as customer-provided Longma request.
- Drive real search queries: `J90A 瑞典语 露营模式 时长 减少`.
- Candidate titles observed: `OTA节点_J90A-标准语料_V0.6.xlsx`, `J90A-(EU+ER)车机文言_(4+23种语言)_V0.5.5...`, `J90A_海外LanguageList内部版V1.0_260806`, `J90A_EU-PI_LanguageList外发版 Google 表格`.
- Gate: blocked pending exact Swedish row, customer request acceptance, current language-list version and Alchemy project-function/downlink evidence.

### ADS-44267

- Jira current: customer issue `ID20260602134722264`; C673-6; SWD.3.68; Android - General; status In Progress; priority P2; customer label; weather card plus AVM/360 attachment evidence.
- Complete Jira description read: query weather, then shift to R; expected 360/AVM highest layer; actual weather card remains above 360. Comments conflict: prior “design as is/close” versus current product statement that AVM should outrank a large card; supplier says AVM is an Activity and cannot guarantee layer.
- Related issue read: `ADS-46283` and its intentToExit/weather-card behavior were read from the current comments.
- Drive real search queries: `天气卡片 360 AVM 层级 C673`.
- Candidate titles observed: `Megatronix_地图导航产品需求文档_C385&C673_V6.1`, `长安C673&C385-Components.xlsx`, `座舱全功清单_C385-5_C673-7大激光_20260731.xlsx`, `深蓝项目变更管理表-2026年`.
- Gate: blocked pending current C673-6/C673-7 AVM layer definition and conflict resolution; status must remain 待会诊.

## Conclusion

This run has real Jira and Drive search observations for five new keys, but no ticket has passed the schema-v5 evidence gate. No online sheet/index patch was generated. Exact candidate opening, per-result receipts, version-family enumeration, Alchemy standard/project function-point evidence, and MasterGo/current layer evidence remain required before any write.
