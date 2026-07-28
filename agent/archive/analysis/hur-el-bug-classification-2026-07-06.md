# HUR EL Bug Classification - 2026-07-06

Source JQL:

`project = HUR AND issuetype = Bug AND status in ("To Do", Reopened, "In Progress", Pending) AND assignee in (membersOf(product-ca)) AND assignee = you.wu`

## Scope

True EL / Israel / Arabic configuration bugs found in the JQL:

- `HUR-81528`
- `HUR-81030`
- `HUR-80609`
- `HUR-80518`
- `HUR-80515`
- `HUR-80396`
- `HUR-80390`
- `HUR-80125`

The linked issue `HUR-81582` is `ER`, not `EL`, but is included separately because the user pasted that ticket URL.

## Classification

| Jira | Category | Product conclusion | Next action |
| --- | --- | --- | --- |
| HUR-81528 | Arabic localization / BTPhone contact label | First confirm with 一星 whether the displayed value is read from phone/system data. If yes, accept current behavior and close; if not, route BTPhone/system-contact localization. | Ask 一星, then close as accepted current behavior or transfer localization based on answer. |
| HUR-81030 | Phone-number display rule | Keep phone numbers as canonical dial string `10086`; do not convert phone numbers into localized Arabic-script digits/words for display. | Close as non-issue / update test expectation. |
| HUR-80609 | Arabic toast localization | Exit camping-mode toast should be Arabic. Zhou Junyan has registered it and is waiting for a new version. | Keep Pending, verify in returned version. |
| HUR-80518 | Arabic copy / vision text localization | Thermostatic-cabin low-performance-mode Arabic text is wrong. Registered by Zhou Junyan. | Keep Pending, verify in returned version. |
| HUR-80515 | Arabic copy / scene-mode translation | Camping mode is translated as comfort mode. Registered by Zhou Junyan. | Keep Pending, verify in returned version. |
| HUR-80396 | Voice TTS configuration | First network pre-hint issue was fixed, but verification found wrong TTS because the third TTS for `1039` should not exist. | Transfer voice/platform config; remove wrong TTS variant and verify with HUR-79577. |
| HUR-80390 | POI tag localization, voice-map boundary | UI should not display Chinese `餐厅` in English/EL locale. Voice should not pass Chinese literal as display text; map/voice need a localized display strategy based on tag/canonical. | Pull voice + map to align. Short-term: voice/platform provides localized display text or map maps `restaurant` to locale string. |
| HUR-80125 | Test condition / online capability boundary | `go to airport` is online navigation POI search. Current Arabic config is offline-only/no online switch, so expecting online navigation execution is not valid. | Close as non-issue or transfer test to update case; if customer wants offline airport POI, create new requirement. |
| HUR-81582 | ER, privacy precondition, not EL | In wash mode, privacy mode should not be closable by voice. Existing voice demand lacks this precondition. | ER ticket: bug-to-demand / voice document task, add precondition for wash mode. |

## Buckets

### Can close / update test

- `HUR-81030`: phone number should display canonical digits `10086`.
- `HUR-80125`: offline Arabic config cannot be expected to execute online POI search.

### Pending version verification

- `HUR-80609`
- `HUR-80518`
- `HUR-80515`

These are already registered by Zhou Junyan; wait for new build and verify.

2026-07-06 可姐复盘确认：这三条 Agent 判断均为对，处理方向保持 Pending 等新版本验证。

### Transfer to implementation / config

- `HUR-81528`: ask 一星 whether it is phone/system-returned data; close if yes, otherwise transfer BTPhone / system contact localization.
- `HUR-80396`: voice/platform TTS config.
- `HUR-80390`: voice + map localization alignment.

### Separate non-EL ticket

- `HUR-81582`: ER wash-mode privacy precondition, should go to bug-to-demand / voice documentation task.

## Jira Comment Drafts

`HUR-81030`:

> 产品结论：电话号码属于拨号标识，显示应保持 canonical 数字串，如 `10086`，不转换为阿拉伯语数字/文字。当前表现符合预期，建议关闭并同步测试修改预期。

`HUR-80125`:

> 产品结论：`go to airport` 属于在线导航 POI 搜索能力；当前阿拉伯配置为离线场景且无在线切换能力，按现有能力不应要求执行在线搜索。建议关闭当前 bug，若客户要求离线支持机场 POI 搜索，另走需求。

`HUR-80390`:

> 产品结论：EL/英文场景下地址弹窗不应展示中文 `餐厅`。该问题应按本地化展示处理，语音侧不要将中文 literal 作为 UI 展示文案；建议语音与地图对齐，由语音提供本地化 display text 或地图基于 `restaurant` 做本地化映射。

`HUR-80396`:

> 产品结论：离线查询家的地址不应播报“页面已打开，现在你可以手动操作”。该问题与 `HUR-79577` 同类，需删除/修正 1039 下错误 TTS 配置后回归。

`HUR-81528`:

> 产品结论：先确认该字段是否为手机/系统数据返回。若一星确认读取手机系统数据，当前表现可接受，建议关闭非问题；若不是系统返回，再转 BTPhone/系统联系人本地化处理。

`HUR-81582`:

> 产品结论：洗车模式中隐私模式应保持受控，不能通过语音关闭。现有语音需求缺少洗车模式前置条件，建议走语音文档 task/bug 转需求补充该限制。
