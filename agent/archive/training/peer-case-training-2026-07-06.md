# Peer Case Training Notes - 2026-07-06

> Historical calibration material. It preserves prior examples only; current workflow and sheet schema are defined by `agent/workflows/bug.md` and `agent/sheet-contract.md`.

## Sources

- 罗稚钦工作说明：
  - `https://docs.google.com/spreadsheets/d/1VPXk6D0yPRZpMb9_dlLWd2RfHcPqp0Yz/edit?gid=2017792747#gid=2017792747`
  - This file is an Office-backed spreadsheet, so Google Sheets API metadata is unavailable. Drive text extraction was readable.
- 李欣的工作说明（深蓝&马自达）：
  - `https://docs.google.com/spreadsheets/d/1dkVWO52bgDbD-RqNqA0Up3r3sWfneeoIX5-K_qvd2QU/edit?gid=674412372#gid=674412372`
  - Target tab: `bug处理`.

## How To Use These Cases

Use these as product-side calibration examples before writing any new Jira bug judgment. They are not source of truth by themselves. For a new bug, still read the Jira page, project docs, Alchemy result, and available UE/PRD first.

When a new bug resembles one of these patterns, write a direct product conclusion:

- close as non-issue
- accept current behavior
- transfer to NLU / voice platform
- transfer to app or map R&D
- convert to requirement
- keep one representative ticket and close duplicates

Do not write `产品确认` as the final action.

## Reusable Judgment Rules

### 1. Close As Non-Issue When The Expectation Is Not In Scope

Use `非问题 / Resolve Invalid` when:

- the requirement document or UE does not define the requested behavior;
- the current behavior matches PRD/UE;
- the test case assumes behavior that product never promised;
- the issue is only a wording misunderstanding and the functional result is correct;
- the customer or project has explicitly accepted the existing behavior.

Useful wording:

- `按现有需求关闭，当前无此功能定义。`
- `当前行为符合需求/交互，按非问题关闭。`
- `测试用例预期不成立，转测试修改用例。`

Examples seen:

- `BEO-7467 / BEO-7468`: P-gear expectation did not apply; judged by vehicle speed instead.
- `SD-4665`: no navigation search bar switch in display settings.
- `HUR-81049 / HUR-81050`: `设置` is not equal to `打开`.
- `ADS-44488`: screen brightness auto adjustment comes from light sensor, not vehicle light setting.
- `BEO-6045`: factory-reset defaults followed document definition; test expectation was wrong.

### 2. Accept Current Behavior When Fix Value Is Low Or Interaction Is Tolerable

Use `接受现状 / 保持现状` when behavior is understandable, low impact, or costly to optimize without clear user value.

Useful wording:

- `用户感知可接受，维持现状。`
- `收益较小，不作为 bug 修改。`
- `按当前交互关闭，后续客户坚持再转需求。`

Examples seen:

- `ADS-40706`: delete on wallpaper page accepted as current behavior.
- `ADS-43242`: split-screen flash before navigation full-screen accepted / moved to demand only if needed.
- `BEO-4065`: air-condition mini-window transition inconsistency accepted due low benefit.
- `HUR-79956 / HUR-77377`: repeated Bluetooth connection-failed popup accepted in this condition.

### 3. Existing Function But Missing Utterance Or Mapping Goes To Voice/NLU

If Alchemy/standard function already supports the capability but the query is missing, wrong, or not inherited by the project, do not create a new product requirement first. Transfer to voice/NLU or voice platform to add泛化, mapping, project inheritance, or slot value.

Useful wording:

- `能力已存在，转语音/NLU补泛化和项目继承。`
- `标准功能支持，缺口在语料/槽位/项目配置。`
- `按 meta_id 对应功能点补 query 或取值。`

Examples seen:

- `ADS-41372`: "不走收费路" handled as泛化.
- `ADS-41356`: should route to `1570` for mobile data query.
- `BEO-3899`: navigation broadcast setting should execute according to operation-platform dispatch.
- `ADS-42892`: skin/wallpaper settings need泛化 under existing function.
- `ADS-43468`: CLTC/WLTC difference handled as whether this wording should be supported.

### 4. Missing Slot, New Value, Or Unsupported Edge Behavior Becomes Requirement

Convert to requirement when:

- current platform truly lacks the value/slot/rule;
- existing docs do not cover the requested scenario but the user expectation is reasonable;
- implementation requires a new front-end/app behavior or project configuration;
- privacy/safety/auth restriction needs a new前置条件 across entry points.

Useful wording:

- `转需求：补充 xxx 场景/槽位/前置条件。`
- `bug 转需求，需求描述写清 query、期望行为、功能点链接。`
- `先关 bug，关联需求票推进。`

Examples seen:

- `PC-37128`: opening charge port cover required new utterance / demand path.
- `PC-36843`: wiper voice multi-action should remove wheel-switch logic; convert to requirement.
- `ADS-43611`: delayed scene execution must stop when privacy authorization is withdrawn; add pre-check requirement.
- `ADS-43785`: super power-saving behavior drifted from operation-platform demand; create a new bug-to-demand ticket.
- `BEO-4489`: factory reset restriction under low battery/charging/discharging had document support, so supplement demand.

### 5. Privacy And Authorization Must Be Checked Across Entry Points

When privacy authorization is not agreed, do not only check the app page. Voice, widgets, flexible cards, and background refresh must be included if they expose data or execute protected operations.

Useful wording:

- `隐私授权前置条件需要覆盖该入口，转对应模块补限制。`
- `语音入口也要受蓝牙电话隐私授权控制。`
- `widget/卡片不得绕过隐私协议刷新数据。`

Examples seen:

- `ADS-43268`: Bluetooth phone privacy not agreed, voice can directly dial; add a前置条件.
- `ADS-43267`: Bluetooth phone card state inconsistent before privacy authorization; add restriction.
- `ADS-43438`: flexible desktop Bluetooth card can refresh call records before authorization; tie to previous demand.
- `HUR-80003`: Bluetooth phone permission/page disabled state and dialog state inconsistent; complete authorization logic.

### 6. Duplicate Or Same Root Cause: Keep One Representative Ticket

If several tickets are the same root cause, keep the clearest representative one, link or comment the others, and close duplicates or transfer to the same owner.

Useful wording:

- `与 xxx 同根因，保留 xxx，当前票按重复问题关闭。`
- `同一类语言/同一根因，只留一个代表票推进。`

Examples seen:

- `ADS-44160` duplicates `ADS-43148`.
- `HUR-80119 / HUR-80113 / HUR-80114 / HUR-80115 / HUR-80108 / HUR-80107` follow the same multilingual navigation issue group.
- `BEO-4532` related to `SD-3528` because wording was corrected but execution direction was wrong.

### 7. Multilingual Voice Bugs Need Translation/Language-Channel Judgment

For foreign-language voice bugs, first decide whether the issue is:

- translation text wrong;
- language model/intent mapping missing;
- meta_id/action placeholder impossible to configure for that language;
- same root cause across multiple languages.

Useful wording:

- `转语音配置/翻译修正。`
- `多语言同根因，保留代表票，其他关闭。`
- `当前多语言能力不支持该占位符，删除语料或按不支持处理。`

Examples seen:

- `BEO-5202`: French instruction should map to relative adjustment `meta_id 1385`; cloud language model optimization.
- `HUR-80095`: multilingual `ACTION$` placeholder difficult to configure; direct translation or remove utterance.
- `HUR-79583 / BEO-6169`: company/home location queries under multilingual navigation require platform configuration or demand.
- `SD-3528`: translation caused wrong expected behavior.

### 8. Navigation/POI Bugs: Separate Voice Dispatch From Map Result

For navigation bugs:

- if Alchemy dispatches wrong meta_id or missing slot, transfer to voice/NLU;
- if Alchemy dispatches correct `poi_name` or action but map/vehicle picks wrong result, transfer to map/vehicle R&D;
- if current POI search behavior is obviously unacceptable compared with normal map products, do not close as non-issue just because a rule exists;
- compare with phone map behavior when needed.

Useful wording:

- `语音下发正确，转地图/车端处理搜索或排序。`
- `语音落域错误，转NLU修正 meta_id/slot。`
- `搜索结果不符合用户预期，拉地图与语音会诊。`

Examples seen:

- `PC-36286`: client matched by `poi_name` without considering `around`; app/client should add around parameter.
- `ADS-43297`: `导航到单位` should route to `1207`.
- `HUR-80319`: deleting waypoint should route to `1205`, not current wrong meta.
- `HUR-80355`: route too long caused map calculation delay; close if accepted as map limitation.

### 9. TTS Or Reply Text: Check Execution First

If execution is correct but TTS is awkward, route to voice platform / TTS wording. If TTS is correct but execution fails, route to app/R&D. If current state already matches command, no repeated execution may be acceptable.

Useful wording:

- `执行正确，仅回复文案需调整。`
- `TTS正确但车端未执行，转对应应用研发。`
- `当前已是目标状态，无需重复执行。`

Examples seen:

- `ADS-43208`: wiper TTS had a defined new reply; debug / update wording.
- `ADS-43844`: voice visible names and wording inconsistent; modify platform copy and R&D behavior.
- `ADS-43561`: current state already主驾小憩; no need to repeat播报.
- `ADS-44656`: unsupported function reply should align with operation-platform common reply.

### 10. Project Or Customer Confirmation Is A Step, Not The Final Product Wording

When the peer sheets say "与客户确认" or "项目确认", use it as a gating action. In our output, still give the interim product stance and next owner.

Useful wording:

- `当前按现有需求关闭；若客户要求变更，再转需求。`
- `当前按项目配置保持现状；由项目经理确认客户是否新增需求。`
- `有文档支持，先按 bug 转研发；若客户要求不同，另走需求变更。`

Examples seen:

- `ADS-4072223635`: app P-gear corner tag requires customer confirmation because previous scope was video/game.
- `SD-3566`: Bluetooth contact search button follows current interaction; customer change requires demand input.
- `PRD/UE inconsistent` cases should be handled by choosing the latest effective document or owner, then recording gap.

## Status Vocabulary To Reuse

- `可关闭`
- `接受现状`
- `转语音/NLU`
- `转语音平台/运营平台`
- `转地图研发`
- `转BTPhone`
- `转项目`
- `转测试修改用例`
- `转需求`
- `重复问题关闭`
- `待会诊`

## Product Sheet Writing Defaults

For 吴优's `bug` sheet, keep output short:

- `收集到的信息`: one sentence combining Jira fact and evidence.
- `预期处理方式`: one sentence with conclusion and owner.
- `状态`: one short status.
- `备注`: only key caveat, duplicate link, or next gating action.

Prefer:

- `按现有需求关闭，吴优评论“当前无此需求”。`
- `能力已存在，转语音/NLU补泛化。`
- `语音下发正确，转地图研发处理搜索结果。`
- `隐私授权前置条件应覆盖语音入口，转BTPhone补限制。`

Avoid:

- `产品确认`
- `建议产品判断`
- `研发看下`
- long technical root-cause paragraphs in the main sheet cell

## Peer Style Analysis

### 罗稚钦 Style

罗稚钦有多年工作经验，所以她的表是偏“资深产品快速定性”的工作台。很多行不是缺少判断，而是把判断压缩到一句可执行结论里；重点是快速把 bug 分到 `非问题 / debug / 转需求 / 转项目 / 修改用例 / 转回测试`，不在表里展开完整推理过程。

#### Writing Pattern

- `收集到的信息` 常常是一句判断依据，不追求完整背景。
- `预期处理方式` 直接给处置类型，例如 `非问题`、`debug`、`转需求`、`转项目`。
- 语气更像内部备忘，不像对外说明。
- 很多结论用“没有这个需求”“测试没有用例来源”“设置≠打开”“翻译有问题”这类短句。
- 对证据要求是“够判断即可”，不会每条都贴长文档。
- 她默认读表的人能理解上下文，所以不会解释每一步为什么成立。

#### Judgment Bias

罗稚钦更敢关闭 bug，尤其是以下场景：

- 测试预期没有需求来源；
- 当前文档/UE没有定义；
- 功能语义被测试理解错；
- 同类问题已有客户或项目接受口径；
- 操作本身不是产品承诺的能力。

Examples:

- `BEO-7467 / BEO-7468`: 非 P 档不是判断条件，实际要看车速，因此非问题。
- `SD-4665`: 车辆设置-显示没有导航搜索栏开关，修改用例。
- `HUR-81049 / HUR-81050`: `设置` 不等于 `打开`，所以不按执行失败处理。
- `HUR-80343 / HUR-80342 / HUR-80341`: 没有双指同时点击需求，非问题关闭。
- `HUR-80262 / HUR-80222`: 数字显示中文/阿拉伯数字属于测试期望问题，非问题。

#### Handling Of Requirements

罗稚钦转需求的触发条件比较清楚：

- 确实新增语料或新增平台能力；
- 现有逻辑不覆盖用户合理预期；
- 当前能力需要补规则而不是修 bug；
- 隐私、场景、语音等链路需要新增前置判断。

Examples:

- `PC-37128`: 充电口盖新增语料但研发未收到需求，转需求。
- `PC-36843`: 雨刮语音多动作当前轮切逻辑不合理，转需求。
- `ADS-43611`: 撤回隐私协议后延时场景未终止，需要增加执行前授权判断，转需求。
- `ADS-41755`: 空调关闭状态下风量调小/调大回复逻辑需要重新定义，转需求。

#### Strengths To Learn

- 快速抓住“测试预期是否成立”。
- 对没有需求定义的 bug 不犹豫，敢关。
- 对“设置/打开”“调高/调到”等语义差异敏感。
- 善于把翻译、多语言、语料问题单独拆出来，不混成产品需求。
- 表格语言短，适合批量推进。
- 能把复杂背景压成一个产品动作，这是资深产品的高价值能力。

#### Weaknesses / Not To Copy Blindly

- 证据链有时太短；这对资深同事自己够用，但对新人/Agent复盘不够。
- “debug” 使用过宽，有时看不出是转语音、转研发还是转平台。
- “与客户确认”有时停在动作，没有写当前产品立场。
- 对复杂语音链路没有总是写 `meta_id` 或平台详情，复用性不够。

### 李欣 Style

李欣是应届生，所以她的表更像“学习型/推进型 bug 台账”。她会把研发/项目/客户/平台反馈放进 `收集到的信息`，再用 `预计方案` 写下一步。相比罗稚钦，她更倾向保留过程、责任人和待办，这对追溯很有用，但产品定性有时没有完全收口。

#### Writing Pattern

- 常用 `【预计方案】` 开头，便于一眼区分结论。
- `收集到的信息` 往往保留研发原话或平台现象。
- `状态` 用 `done / 解决 / 已转 / 可姐验证 / 保持现状 / bug转需求` 这类推进状态。
- `备注` 常放真实下一步，例如 `转给智秀`、`问雷雷`、`贴图给研发`、`和客户再确认`。
- 她更倾向把“已有票、重复票、需求票、相关文档”串起来。
- 她把很多中间过程留在表里，说明仍在用表格辅助自己完成判断闭环。

#### Judgment Bias

李欣更关注“这条 bug 该流向哪里”，而不是只判断对错。

她的常见路径：

- 能力已有但泛化/语料缺：转语音/NLU/运营平台。
- 车端逻辑或接口未处理：转对应研发。
- 交互无定义但用户预期合理：bug 转需求。
- 客户或项目已接受：接受现状/保持现状。
- 多条同根因：保留代表票，其余关闭或关联。
- 需要验证的：写清找谁，而不是笼统写“确认”。

Examples:

- `ADS-42892`: 皮肤/壁纸设置走现有 1305 能力，补泛化需求。
- `ADS-41356`: 平台当前下发 1919，但应走 1570 查询移动数据。
- `ADS-43268 / ADS-43267`: 蓝牙电话隐私未授权，语音和 widget 入口也需要加前置条件。
- `PC-36286`: 客户端只按 `poi_name` 匹配，没有考虑 `around` 参数，转开发加参数。
- `HUR-80319`: 删除途经点当前走 1091，应该走 1205。
- `ADS-44160`: 与 `ADS-43148` 同根因，重复问题保留一个。

#### Handling Of Voice Bugs

李欣处理语音 bug 的风格很适合我们学习：

- 先看平台下发到哪个功能点 / meta_id。
- 再判断是“语音落域错”还是“车端执行错”。
- 如果平台能力已有，倾向补泛化或配置，不直接转新需求。
- 如果平台没有能力或项目未继承，才转需求或转运营平台。
- 对 TTS 问题先拆成“执行对不对”和“回复文案对不对”。

Examples:

- `ADS-42560`: “关闭音量”拆成点击音量、选择音量、全通道静音，不是简单判失败。
- `ADS-43386`: 均衡器非自定义模式下，预期回复应是当前不处于自定义模式。
- `ADS-43844`: 播报音名称和音乐搜索混淆，需要运营平台改文案，也要给研发处理。
- `BEO-7754`: 后排屏角度 TTS 取决于展开/收起 meta_id，需确认是否整合。

#### Handling Of Privacy / Authorization

李欣会把隐私授权拆到多个入口，而不是只看页面：

- 页面入口；
- 语音入口；
- widget / 柔性桌面卡片；
- 卡片后台刷新；
- 电话权限和蓝牙电话隐私协议之间的关系。

Examples:

- `ADS-43438`: 未授权蓝牙电话隐私，柔性桌面蓝牙卡片仍刷新通话记录。
- `ADS-43268`: 未同意蓝牙电话隐私，语音仍可拨打电话。
- `ADS-43267`: 未授权时 widget 卡片显示状态和系统不一致。
- `ADS-43266`: 与 43268 同逻辑，按无效或重复处理。

#### Strengths To Learn

- 善于定位责任方，不停在“产品确认”。
- 善于把现象拆成“平台下发 / 车端执行 / TTS文案 / 项目配置 / 可见表”。
- 对重复票和同根因票处理更系统。
- 会保留研发原话，便于追溯。
- 对隐私授权、多语言、可见即可说这类链路型问题更敏感。
- 对新人来说，她的过程记录更适合作为 Agent 学习样本，因为能看到“为什么转给谁”。

#### Weaknesses / Not To Copy Blindly

- 表格里有不少半成品短语，例如 `问雷雷`、`看看交互`、`和客户确认`，这是新人推进过程记录，直接给可姐看不够完整。
- `状态` 字段有时混用 `done / 解决 / bug转需求 / 保持现状`，不够规范。
- 有些 `预计方案` 仍是过程动作，不是最终产品口径。
- 长期复用时需要我们把她的推进语翻译成更标准的产品结论。

## Combined Style We Should Use For 吴优

吴优这边不应该完全照搬任何一个人，而是合并两种风格：

Seniority interpretation:

- 罗稚钦的表适合学习“资深产品如何压缩判断、快速收口”。
- 李欣的表适合学习“新人如何记录链路、责任方和推进过程”。
- Agent 应该用李欣的链路记录方式补足证据，再输出成罗稚钦式的短结论。

### Use 罗稚钦's decisiveness

- 没需求就关。
- 测试预期错就转测试或关闭。
- 语义不成立就直接写非问题。
- 不要为了“稳”什么都转需求。

### Use 李欣's routing precision

- 语音问题必须拆平台、NLU、车端、TTS、可见配置。
- 隐私授权要查所有入口。
- 地图问题要拆语音下发和地图搜索结果。
- 重复票要保留代表票。
- 结论里写清责任方和下一步动作。

### Our Target Output Style

For 吴优's `bug` sheet, ideal output should look like this:

- `收集到的信息`: `Jira现象 + 关键证据 + 是否已有功能/需求`
- `预期处理方式`: `当前产品结论 + 责任方 + Jira动作`
- `状态`: `可关闭 / 转语音 / 转研发 / 转需求 / 待会诊`
- `备注`: `meta_id / 相关票 / 需要问的人 / 复盘风险`

Examples:

- `当前无此需求，按非问题关闭；吴优评论“深蓝无此需求”。`
- `能力已存在，转语音/NLU补泛化和项目继承；Jira评论预期一致。`
- `语音下发正确，转地图研发处理POI排序；必要时拉地图和语音会诊。`
- `隐私授权应覆盖语音和卡片入口，转BTPhone补前置条件。`
- `与 xxx 同根因，保留 xxx，当前票按重复关闭。`

### What This Means For Future Agent Judgments

When judging a new bug, first classify it into one of these buckets:

1. `测试预期不成立`
2. `需求未定义`
3. `已有能力但泛化/配置缺失`
4. `平台下发正确，车端/地图执行错误`
5. `隐私授权入口缺失`
6. `TTS文案问题`
7. `多语言/翻译问题`
8. `同根因重复问题`
9. `合理用户预期但现能力没有，转需求`
10. `影响小或客户接受，维持现状`

Then write the product conclusion directly. Do not write `产品确认` as the destination.
