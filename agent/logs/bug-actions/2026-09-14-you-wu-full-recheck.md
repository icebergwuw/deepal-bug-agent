# 2026-09-14 吴优当前待处理 Bug 完整复查

- Run ID：`bug-20260914T1726+0800-you-wu-full-recheck`
- 操作者 / 目标负责人：吴优（`wu-you`）
- 查询范围：`project in (SD, HUR, ADS, BGS, BEO, PC, SM, SLV) AND issuetype = Bug AND status in ("To Do", Reopened, "In Progress", Pending) AND assignee in (membersOf(product-ca)) AND assignee = you.wu`
- Jira 实时结果：15 条，全部当前经办人吴优。入口：Jira REST + 操作者当前 Chrome 已登录态。
- 模式：普通二次复查（`recheck`）；新票本应追加。本轮**未写线上清单、未改本地索引、未评论/转派/关闭 Jira**。
- 阻塞：schema-v5 写表门禁要求 Google Drive `origin=connector` 检索回执。当前会话无 Drive/Sheets connector；Chrome Drive 搜索页已打开但结果不能冒充 connector 回执。因此不能生成通过 `validate_bug_evidence_gate.py` 的确定性写表请求，也不能发送 Sheets `batchUpdate`。
- 已完成：15 票完整 Jira 字段/描述/附件元数据/评论时间线；语音票 Alchemy 在线原话、标准功能、深蓝/马自达项目功能；MasterGo 深蓝项目首页已登录（未读到具体目标图层）。
- Alchemy 回执：`agent/logs/bug-actions/2026-09-14-batch-recheck/alchemy-2026-09-14.json`
- 实时清单：`SD-6421`、`SD-6404`、`SD-5515`、`PC-39375`、`PC-38942`、`PC-37759`、`PC-37473`、`HUR-84753`、`HUR-78190`、`ADS-50733`、`ADS-50732`、`ADS-50731`、`ADS-50730`、`ADS-50551`、`ADS-44267`。
- 已有行：166/167/171/373/265/71/178/113/415。新票未入索引：`HUR-84753`、`ADS-50733`、`ADS-50732`、`ADS-50731`、`ADS-50730`、`ADS-50551`。索引最大行 425，若恢复写表则新票从 426 起追加，锚点第 107 行。

## 本轮未执行动作

- 未更新吴优 `bug` 页 C/D/G/I/J 或追加新行。
- 未更新 `agent/bug-owners/wu-you/index.md`。
- 未执行任何 Jira 评论、转派、关闭或状态变更。
- 未修改 Alchemy、MasterGo。

## SD-6421 决策核验卡

- 备注因果链：Search Parking 上屏无搜索结果；聂汉维日志 `classification=chat meta_id=2820`；吴优指出语料表有 SEARCH PARKING/COFFEE；于丽美要求产品下发 Search 类新增句式。关联 SD-6991 已关闭（离线不支持导航）。2026-09-14 Alchemy：C673-G/D587-G 的 `Search Parking`/`SEARCH PARKING` 落到 `meta_id=1026` 点播歌曲；D587-G `SEARCH COFFEE` 正确落到 `meta_id=1208` 搜索/展示地址。
- 客户问题识别：否（标签客户_JIRA，无完整客户编号/用例结构）。
- 关联票：SD-6991 已读，已关闭，不能证明 Search 句式已覆盖。
- 证据画像与必查资料：选择 voice + map_navigation；排除 visible_interaction。Drive 正式定义检索因无 connector 标 unavailable。
- 资料适用范围：Jira 描述/评论/日志=implementation_actual；Alchemy 当前/标准 1097 点播歌曲与项目 24325 继承未修改=implementation_actual；1208 搜索地址证明 Search Coffee 句式已存在。缺少当前 C673 海外语料表精确条款作 formal_target。
- 冲突处理：历史“转需求”与当前 1026 音乐误召回并存；不能在无语料表正文时把 1026 直接定为唯一缺陷位置。
- 唯一结论：结论：G3G5 VR Search Parking 当前未按搜索执行，平台把 SEARCH PARKING 映射到歌曲点播 1026，而 SEARCH COFFEE 已能走 1208；在未回读现行海外语料表正文前，保持待复核，不把历史转需求直接写回。依据：SD-6421 Jira原票·描述/于丽美2026-08-07评论；Alchemy C673-G/D587-G 2026-09-14·Search Parking→1026、SEARCH COFFEE→1208。处理：回读现行 SEARCH/POI 英文语料表后，补 Search Parking 句式或修正 1026 误召回并下发；C673海外语音产品负责人处理。状态：待复核。

## SD-6404 决策核验卡

- 备注因果链：C673-G 欧洲导航卡片英文道路名与下个路口信息重叠；程云要求产品和 UI 定义显示边界。历史 08-17 曾按 UE V0.6 标 3/4 转研发。本轮未读到当前 MasterGo 目标图层，Drive connector 不可用。
- 客户问题识别：否。
- 关联票：无直接关联票，checked=true。
- 证据画像与必查资料：选择 map_navigation + visible_interaction；排除 voice。UE/配置检索因无 connector 与未读目标图层标 unavailable。
- 资料适用范围：Jira 描述/视频附件=implementation_actual；历史 UE 不能替代本次图层回读。
- 冲突处理：重叠现象明确，但不能用过期 UE 快照直接定研发方案。
- 唯一结论：结论：导航卡片英文长文本重叠现象成立，但本轮未取得当前地图 UE 目标图层和层级/避让正式条款，不能维持或更新为可转研发。依据：SD-6404 Jira原票·描述/程云2026-07-23评论/视频附件。处理：打开现行 C673 地图导航 UE 对应导航卡片画板，确认道路名与下路口信息分区后，再转 Android-Map UI 研发（程云）修复；C673地图UI产品负责人处理。状态：待确认。

## SD-5515 决策核验卡

- 备注因果链：马来语 `Di manakah saya sekarang` 回复 ok；历史日志 `locations:where_am_i` 且魏新享确认 1006 下发无误；程云称高德返回中文地址无法按马来语 TTS 播报。2026-09-14 Alchemy C673-G/C673DA 同原话变为 `meta_id=2820` 拒识，不再下发 1006。标准 1089 查询当前位置、深蓝项目 24317 继承未修改仍存在。
- 客户问题识别：否。
- 关联票：描述指向 SD-5514 日志，本轮未把 SD-5514 当关闭依据。
- 证据画像与必查资料：选择 voice + map_navigation。Drive 正式马来语 TTS/地址本地化条款 unavailable。
- 资料适用范围：Jira 历史 1006 下发=implementation_actual；当前 Alchemy 2820=implementation_actual；1006 标准/项目功能点=alchemy_standard/project，不能单独证明马来语播报目标。
- 冲突处理：历史实现是 1006，当前平台拒识，与“下发无误转车机”冲突；以当前 Alchemy 为准，不沿用可转语音关闭链。
- 唯一结论：结论：马来语“我在哪”能力在标准/项目功能点仍是 1006 查询当前位置，但当前 C673-G/C673DA 在线原话已拒识到 2820，与历史 1006 下发冲突，先复核配置再谈 TTS 本地化。依据：SD-5515 Jira原票·魏新享/程云评论；Alchemy 2026-09-14 C673-G/C673DA·Di manakah saya sekarang→2820；标准功能 1089/项目 24317。处理：恢复马来语当前位置到 1006 并核验马来语地址 TTS；C673海外语音产品负责人处理。状态：待复核。

## PC-39375 决策核验卡

- 备注因果链：标记日志“几点退潮”在闲聊与天气间漂移。吴优 08-18 口径应稳定进 1975。张凯迪 09-10 称标准 1400 查询天气现象不含退潮。2026-09-14 Alchemy BIGSUR 同原话稳定 `meta_id=1975` weather:query:check，slot=weather_condition literal=退潮。深蓝项目 26750 继承未修改(1400) 已锁定。
- 客户问题识别：否。关联 ST-63391 为外部指令匹配，已读标题，不改变本票天气边界。
- 关联票：ST-63391 已读，外部匹配票，不替代本票天气现象范围。
- 证据画像与必查资料：选择 voice。天气 PRD/现象词表 Drive 检索 unavailable。
- 资料适用范围：Alchemy 1975 当前结果=implementation_actual；标准 1400/项目 26750=alchemy_standard/project；缺天气现象 canonical 词表作 formal_target。
- 冲突处理：平台已能走到 1975，但 1400 是否覆盖“退潮”无正式词表，不能判可转语音或非问题。
- 唯一结论：结论：“几点退潮”当前稳定命中 1975 查询天气现象，但标准 1400 是否包含退潮/涨潮未在正式词表回读，不能把付费潮汐或闲聊冲突一次定责。依据：PC-39375 Jira原票·吴优08-18/张凯迪09-10评论；Alchemy BIGSUR 2026-09-14·几点退潮→1975；标准1400/项目26750。处理：回读天气现象词表后决定保留 1975、补退潮 canonical，或剔除误召回；深蓝语音天气配置负责人处理。状态：待复核。

## PC-38942 决策核验卡

- 备注因果链：收藏西湖山水后说“第一个”，列表有时收起。程云区分“第一个”会关列表、“选择第一个”为二次交互，要求产品统一关闭规则。Alchemy：收藏句 `meta_id=1021` 收藏 POI；无列表上下文的“第一个”落到 `meta_id=3116` 通用收藏+list_offset=1，不是可见列表选择。
- 客户问题识别：否。
- 关联票：无直接关联票。
- 证据画像与必查资料：选择 voice + visible_interaction。POI 二次交互 UE/PRD Drive 检索 unavailable。
- 资料适用范围：Jira 步骤/程云评论=implementation_actual；Alchemy 1021/3116=implementation_actual；缺 POI 列表可见节点优先级正式定义。
- 冲突处理：可见优先要求列表在前时“第一个”应选列表项；当前无列表上下文测试不能代替车端可见节点，规则空白仍在。
- 唯一结论：结论：收藏 POI 后“第一个”的列表关闭/选择规则仍未正式定义；当前无列表上下文时“第一个”会落到通用收藏 3116，不能直接当语音缺陷关闭。依据：PC-38942 Jira原票·程云2026-08-04评论；Alchemy BIGSUR 2026-09-14·我要收藏西湖山水→1021、第一个→3116。处理：补齐 POI 列表上“第一个/选择第N个/收藏/导航/途经点”的关闭与选择规则并下发；POI/VUI产品负责人处理。状态：待确认。

## PC-37759 决策核验卡

- 备注因果链：蓝牙已连接、测试预期“未授权不能打 10086”，实际可打出。雷磊要求产品确认非点击触发的隐私授权。历史曾按数字直拨不依赖通讯录授权判非 Bug。本轮未回读现行电话/隐私 PRD 条款。Alchemy `拨打电话`→1059 仅表达打电话意图。
- 客户问题识别：否。
- 关联票：无。
- 证据画像与必查资料：选择 voice + visible_interaction。电话隐私正式定义 Drive 检索 unavailable。
- 资料适用范围：Jira 步骤=implementation_actual；1059=implementation_actual；缺隐私授权对象（通讯录 vs 麦克风 vs 数字直拨）formal_target。
- 冲突处理：测试预期与历史产品口径冲突，无当前正式条款不能维持非 Bug。
- 唯一结论：结论：蓝牙已连接时语音拨 10086 能打出，是否绕过隐私授权取决于授权对象是通讯录还是数字直拨；本轮未回读现行电话隐私条款，不能关闭。依据：PC-37759 Jira原票·描述/雷磊2026-07-10评论；Alchemy BIGSUR·拨打电话→1059。处理：回读现行蓝牙电话隐私授权定义，明确数字直拨与联系人检索的授权边界后关闭或转研发；吴优（电话产品）处理。状态：待确认。

## PC-37473 决策核验卡

- 备注因果链：POI 列表上说打开行车记录仪，DVR 打开但 POI 弹窗仍在。吴优目标是关 POI；谭威称语音只触发打开 DVR，应由地图侧统一互斥。Alchemy `打开行车记录仪`→1305 app:ctrl open driving_recorder，语义正确。关联 PC-37201 已按另一组窗口“当前层级显示，非问题”关闭，不能外推。
- 客户问题识别：否。
- 关联票：PC-37201 已读、已关闭、不同窗口组合。
- 证据画像与必查资料：选择 voice + visible_interaction + map_navigation。DVR/地图互斥正式定义 Drive 检索 unavailable。
- 资料适用范围：Jira 评论链=implementation_actual；1305/项目 24542=implementation_actual；缺 DVR 全屏与 POI 卡片互斥 formal_target。
- 冲突处理：语音打开动作正确，缺页面互斥规则，不能转语音缺陷。
- 唯一结论：结论：打开行车记录仪的语音执行正确，POI 弹窗是否关闭属于跨应用互斥规则空白，不能归语音缺陷。依据：PC-37473 Jira原票·谭威2026-08-24评论；Alchemy BIGSUR·打开行车记录仪→1305；PC-37201 关闭结论不可外推。处理：定义任一入口打开 DVR 时关闭地图 POI 搜索卡片，并同步地图与 DVR 交互；地图与行车记录仪产品负责人处理。状态：待确认。

## HUR-84753 决策核验卡

- 客户问题识别：是，外部编号 `BG20260911000677`。客户用例有步骤和预期，但缺完整版本前置、权限对象对照表和可复现日志结构，status=incomplete。
- 备注因果链：J90A SWD.050 麦克风权限列表无蓝牙电话，关麦克风开关后蓝牙电话麦克风仍可用。吴优已引用马自达 J90A EU 隐私授权 v1.0 认为国内同规则、是问题。本轮未回读该 PDF 正文条款，也未读到当前车端权限清单实现。
- 关联票：无。
- 证据画像与必查资料：选择 visible_interaction。隐私 UE/权限清单 Drive+目标图层 incomplete。
- 资料适用范围：Jira 描述/吴优评论=implementation_actual 与线索；客户用例不完整强制降级。
- 冲突处理：产品已倾向是问题，但客户用例和权限对象证据未闭环，禁止关闭或转研发。
- 唯一结论：结论：麦克风权限未覆盖蓝牙电话且关闭后仍可用，客户用例不完整，先补齐测试用例和权限对象对照，不能转研发或关闭。依据：HUR-84753 Jira原票·描述/吴优2026-09-14评论；客户编号 BG20260911000677。处理：向客户补齐版本前置、权限开关对象和日志，并回读 J90A 隐私授权麦克风/蓝牙电话条款后定责；吴优处理。状态：待确认。

## HUR-78190 决策核验卡

- 备注因果链：离线“退出全程预览”回复“好的，这就打开导航全览”。常荣日志：NLU 已下发 1018 op=close，归责车端后台分支。张齐财称前后台写死后台，并问项目功能 26006。2026-09-14 Alchemy HUR 同原话仍是 1018 navi:map:journey:view op=close；马自达项目 26006 已下发、继承未修改(1445)。
- 客户问题识别：否。
- 关联票：无。
- 证据画像与必查资料：选择 voice + map_navigation。TTS/前后台执行策略正式条款 Drive 检索 unavailable。
- 资料适用范围：Jira 日志 1018 close=implementation_actual；当前 Alchemy 同样 close=implementation_actual；TTS 打开文案与车端后台分支责任未在正式配置回读。
- 冲突处理：NLU 正确，执行/TTS 错误；不能在未拆清项目 TTS 与车端状态机前单独转语音或转研发。
- 唯一结论：结论：退出全程预览的 NLU 已正确下发 1018 close，车端却打开并播打开 TTS，需会诊项目 TTS/前后台策略与地图执行状态机，不能单转语音。依据：HUR-78190 Jira原票·常荣/刘洪星/张齐财评论；Alchemy HUR 2026-09-14·退出全程预览→1018 close；马自达项目 26006 已下发。处理：核对 26006 关闭 TTS 与地图前后台判断，拆开语音配置与车端执行责任后分别提单；吴优会同地图执行研发处理。状态：待会诊。

## ADS-50733 决策核验卡

- 客户问题识别：是，VIN `LS6C3E2T3TF812038`，标签客户_JIRA。用例只有时间点和现象，缺完整步骤、query 原文、预期层级定义，status=incomplete。
- 备注因果链：场景积木卡片生成后语音打开车辆设置，积木卡片消失且车辆设置层级低于语音卡片。常荣/谭威指向卡片层级。Alchemy `打开车辆设置`→1305 car_settings；`打开场景积木`→1305 sceneblock。
- 关联票：与 ADS-50732 同类层级，未互为关闭依据。
- 证据画像与必查资料：选择 voice + visible_interaction。卡片层级正式配置 unavailable；客户用例不完整。
- 资料适用范围：Jira 现象=implementation_actual；1305=implementation_actual；缺场景积木/车辆设置/语音卡片层级 formal_target。
- 冲突处理：客户用例不完整，固定待确认。
- 唯一结论：结论：场景积木卡片与语音打开车辆设置后的消失/层级问题需先补客户完整测试用例和层级仲裁定义，不能转研发。依据：ADS-50733 Jira原票·描述/常荣谭威评论；Alchemy BIGSUR·打开车辆设置/打开场景积木→1305。处理：补齐客户步骤、query、预期层级，并回读 8295/C385-5 卡片层级配置；C385系统交互产品负责人处理。状态：待确认。

## ADS-50732 决策核验卡

- 客户问题识别：是，VIN `LS6C3E2T3TF812038`，客户用例 incomplete。
- 备注因果链：出行助手卡片生成后语音打开车辆设置，出行卡片消失且车辆设置低于语音卡片。谭威称语音卡片层级本身较高，要产品确认。
- 关联票：与 ADS-50733 同类，已读标题，不合并关闭。
- 证据画像与必查资料：voice + visible_interaction；客户用例不完整。
- 资料适用范围：Jira 现象=implementation_actual；缺出行助手/车辆设置/语音卡片层级 formal_target。
- 冲突处理：客户用例不完整，固定待确认。
- 唯一结论：结论：出行助手卡片在语音打开车辆设置后消失且层级低于语音卡片，客户用例不完整，先补用例和层级定义。依据：ADS-50732 Jira原票·描述/谭威2026-09-14评论。处理：补齐客户测试用例并定义出行卡片与车辆设置/语音卡片互斥层级；C385系统交互产品负责人处理。状态：待确认。

## ADS-50731 决策核验卡

- 客户问题识别：是，VIN `LS6C3E2T3TF812038`，客户用例 incomplete。
- 备注因果链：深蓝管家 query 播报期间挂 R，播报内容在 360 上层。谭威称大模型相关都有此问题。Alchemy `打开深蓝管家`→1305，target 无 canonical。
- 关联票：与 ADS-44267/ADS-50551/ADS-50730 同类跨域层级，已读，不互相关闭。
- 证据画像与必查资料：voice + visible_interaction；客户用例不完整。
- 资料适用范围：Jira 现象=implementation_actual；缺 AVM Activity 与语音/管家卡片层级 formal_target。
- 冲突处理：客户用例不完整，固定待确认。
- 唯一结论：结论：深蓝管家播报期间挂 R 后内容压在 360 上，客户用例不完整，且与天气卡/大模型卡片跨域层级同一未决规则。依据：ADS-50731 Jira原票·描述/谭威评论；Alchemy BIGSUR·打开深蓝管家→1305。处理：补客户用例，并与 ADS-44267 一并定义 AVM 与语音/大模型卡片仲裁；C385系统交互产品负责人处理。状态：待确认。

## ADS-50730 决策核验卡

- 客户问题识别：是，VIN `LS6C3E2T3TF812038`，客户用例 incomplete。
- 备注因果链：场景积木 query 播报期间挂 R，播报内容在 360 上层。Alchemy 打开场景积木→1305 sceneblock。
- 关联票：与 ADS-50731/ADS-50551/ADS-44267 同类，已读。
- 证据画像与必查资料：voice + visible_interaction；客户用例不完整。
- 资料适用范围：Jira 现象=implementation_actual；缺 AVM 与场景积木播报层 formal_target。
- 冲突处理：客户用例不完整，固定待确认。
- 唯一结论：结论：场景积木播报期间挂 R 后内容压在 360 上，客户用例不完整，不能转研发或设计如此。依据：ADS-50730 Jira原票·描述/常荣评论；Alchemy BIGSUR·打开场景积木→1305。处理：补客户用例并定义场景积木播报层与 AVM 仲裁；C385系统交互产品负责人处理。状态：待确认。

## ADS-50551 决策核验卡

- 客户问题识别：是，VIN `LS6C3E2T3TF812038`，客户用例 incomplete。
- 备注因果链：语音“前面是什么小区”播报期间可挂 R，播报在 360 上层。谭威称与生日卡片类似。Alchemy 同原话 `meta_id=1356` 车外识别 geo_match，标准 1412/项目 26067 已锁定继承未修改。
- 关联票：谭威指向生日卡片（ADS-46283 已关闭客户接受无大卡片），不能证明接受本票大模型播报压 AVM。
- 证据画像与必查资料：voice + visible_interaction；客户用例不完整。
- 资料适用范围：Jira 现象=implementation_actual；1356=implementation_actual；ADS-46283 关闭范围不覆盖本票。
- 冲突处理：客户用例不完整，固定待确认。
- 唯一结论：结论：“前面是什么小区”属 1356 车外识别，播报期间挂 R 压在 360 上；客户用例不完整，且生日卡片关闭范围不能外推到本票。依据：ADS-50551 Jira原票·描述/谭威评论；Alchemy BIGSUR·前面是什么小区→1356；ADS-46283 已读不可外推。处理：补客户用例，定义车外识别播报层与 AVM 仲裁；C385系统交互产品负责人处理。状态：待确认。

## ADS-44267 决策核验卡

- 客户问题识别：是，外部编号 `ID20260602134722264`。原票步骤较完整，但本轮未回读视频时间码对应的现行层级配置，客户用例对“天气大卡片 vs 打字机小弹窗 vs AVM Activity”的目标仍不完整，status=incomplete。
- 备注因果链：语音查天气后挂 R，天气弹窗高于 360。谭威称设计如此、等播报完退出；吴优 08-27 明确不接受大卡片压 AVM；谭威 08-28 称 AVM 是华为 Activity 无法保证层级。Alchemy `今天天气如何`→1249 查询天气。
- 关联票：谭威引用 ADS-46283，已读，关闭范围是庆生无大卡片，不能证明接受天气大卡片压 AVM。
- 证据画像与必查资料：voice + visible_interaction。C673-6 层级配置/MasterGo 目标图层本轮未读到。
- 资料适用范围：Jira 描述/吴优谭威评论冲突=implementation_actual + 冲突；1249=implementation_actual；缺 AVM 与 P2 天气卡片仲裁 formal_target。
- 冲突处理：研发“设计如此”不能单独关闭；客户最终结论未覆盖大卡片；保持待会诊。
- 唯一结论：结论：天气卡覆盖倒车 AVM 仍是跨域层级规则冲突，客户未接受大卡片压 AVM，华为 AVM Activity 也无法单独当正式目标，保持待会诊。依据：ADS-44267 Jira原票·描述/吴优2026-08-27/谭威2026-08-28评论；Alchemy BIGSUR·今天天气如何→1249；ADS-46283 已读不可外推。处理：补齐 C673-6 天气卡与 AVM 层级仲裁并会诊系统交互与华为 AVM 责任；C673系统交互产品负责人处理。状态：待会诊。

## 恢复写表条件

1. 恢复可结构化调用的 Google Drive/Sheets connector（`search_drive_files` + `get_cells`/`batchUpdate`），按票补 origin=connector 检索回执、精确文档名和版本族审计。
2. 对需要 UE 的票读取 MasterGo `fileId+layerId` 目标图层，不只停留在项目首页。
3. 客户票补齐测试用例后再把 G 从待确认上修。
4. 通过 schema-v5 gate、写前预检、列级 patch/append、线上回读和 `validate_bug_run.py --phase final` 后才能声称已更新清单。
