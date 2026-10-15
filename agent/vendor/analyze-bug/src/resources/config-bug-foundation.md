# 配置型 Bug 归因基础

## 1. 文档目标

这份文档用于给后续 Codex / Gemini 的自动 bug 分析能力提供“需求与配置链路”归因基础。

它解决的不是 ASR / NLU / Cloud / Vehicle / TTS 的通用运行时分析，而是下面这类问题：

- 需求票或标注规范已经变更，但平台/功能点配置没有跟上
- 新增 `intent`、`slot`、泛化说法、property 后，日志表现像拒识、无操作、执行错
- 平台功能点与标准功能点继承关系处理错误，导致分析对象找错
- `nluMapping`、`slotParams`、`protocolRequest` / `operation`、`slotProperty` 之间链路不完整

维护约定：

- 当前事实基线来自 `voice-requirement-delivery` 的 `SKILL.template.md` 和 `references/`
- 本文档只负责抽象、重组和压缩成 bug 归因语言
- 不在这里维护一套与需求交付技能平行的独立规则

## 2. 需求与配置事实提取

当 Jira 描述、关联需求或日志现象指向配置链路时，先建立这些事实：

- 主需求票：功能点、需求目标、是否只改平台、是否要求 repo 同步
- 标注规范票：`intent`、`slot`、拆分规则、泛化词、property 边界
- 测试票 / AIS 票：验证口径、边界词、预期行为
- 实际功能点详情：`projectId`、`fromFunctionId`、`nluMapping`、`slotParams`、`protocolRequest` / `operation`

优先提取这些字段：

- 入口功能点 ID
- `projectId`
- `fromFunctionId`
- 规范中的 `intent`
- 涉及的 `slot`
- 是否是全新需求或新增配置链路
- 是否只是新增泛化词 / 同义词 / property 映射

## 3. 配置链路判定树

建议按下面顺序排查，不要跳步：

1. 先锁定实际修改目标
   - `projectId` 为空：标准功能点，目标就是当前功能点
   - `projectId` 非空且 `fromFunctionId` 为空：平台独有功能点，目标是当前平台功能点
   - `projectId` 非空且 `fromFunctionId` 非空：继承标准功能点，目标是 `fromFunctionId` 对应的标准功能点
2. 再看平台基础是否齐备
   - 规范给了 `intent` 时，先查 `intentList`
   - 规范依赖新增或变更 `slot` 时，检查 `slotList` 是否存在对应 slot
3. 再看功能点映射是否齐备
   - `nluMapping`
   - `slotParams`
   - `protocolRequest` / `operation`
4. 最后看表达层配置
   - `slotProperty`
   - 字面值写法
   - property / 字面值 / 混合写法是否与规范一致

最小归因规则：

- 平台基础没就绪：优先归因“需求/平台基础配置缺失”
- 平台基础已就绪但功能点链路没挂上：优先归因“功能点配置缺失”
- 若云端已下发明确、稳定且语义正确的 `canonical/property`，问题出在下游执行侧不支持该值：优先归因“Vehicle/车端适配问题”，不要要求云端回退到下游旧枚举
- ops 配置链路完整，但 `online-dialogue` 的 `dialogScenarioBase.json` 或 `dialogScenario*.json` 缺少对应路由、只落到 `1919` 这类兜底、或 repo 配置与 ops 不一致：归因“Cloud/代码问题”
- 配置链路完整且 repo 路由也完整后仍异常：再回到 ASR -> NLU -> Cloud -> Vehicle -> TTS 主链路

## 4. 高频配置故障模式

### 4.1 `nluMapping` 为空，规范无明确 `intent`

现象：

- 新需求未生效
- 日志可能表现为拒识或无操作

首查事实：

- 标注规范是否明确给出 `intent`

配置责任：

- 归因“需求/规范缺失”

排除项：

- 不要直接归因 NLU 模型
- 不要继续补 `slotParams` 或 `operation`

### 4.2 规范有 `intent`，但 `intentList` 无该值

现象：

- 规范已明确描述能力，但功能点无法建立正确匹配链路

首查事实：

- `list_intents` 中是否存在规范 `intent`

配置责任：

- 归因“平台基础配置缺失”

排除项：

- 不要先归因 ASR / NLU 运行时故障

### 4.3 `intentList` 有值，但功能点未挂 `nluMapping`

现象：

- 规范能力已存在于平台基础层，但具体功能点仍无法命中

首查事实：

- 实际修改目标的 `nluMapping` 是否为空或缺对应 intent

配置责任：

- 归因“功能点配置缺失”

排除项：

- 不要把这类问题直接当成分类模型错误

### 4.4 `slotList` 缺失规范依赖的 slot

现象：

- 需求新增 slot 后仍无法正确抽取或链路无法建立

首查事实：

- 规范要求的 slot 是否已进入 `slotList`

配置责任：

- 优先归因“平台基础配置未就绪”

排除项：

- 在 slot 基础都不存在时，不先归因 NER/模型抽取错误

### 4.5 `protocolRequest` / `operation` 为空

现象：

- 意图能命中，但无真实下发
- 日志可能表现为无操作、空操作或执行链路中断

首查事实：

- `nluMapping` 是否已存在
- `slotParams` 是否已正确映射
- `protocolRequest` / `operation` 是否为空

配置责任：

- 归因“接口配置缺失”或“配置链路不完整”

排除项：

- 不要把 `operation` 为空直接归因 Cloud 运行时异常
- 不要把 `protocolRequest` 为空直接归因 Vehicle 执行失败

### 4.6 Property / 字面值 / 混合写法误配

现象：

- 新增说法后部分命中、部分不命中
- 一个 property 覆盖过宽或过窄

首查事实：

- 当前 `slotProperty` 是否存在
- 需求词面是否应该保留字面值
- 是否应采用混合写法

配置责任：

- 归因“配置表达错误”或“property 边界错误”

排除项：

- 不要只因看到 property 存在，就把全部字面值强行替换

### 4.7 云端已有归一值，但执行侧不支持

现象：

- 日志中 `canonical` 已明确且语义正确
- 上游 `intent/slot/operation` 正常
- 下游执行侧因为只识别旧枚举、旧 property 或私有值而走错分支

首查事实：

- 云端下发的 `canonical/property` 是否稳定且与 query 语义一致
- 失败点是否发生在执行侧枚举匹配、协议适配或端侧分支判断

归因要求：

- 优先归因“Vehicle/车端适配问题”
- 解决方案应写“车端补兼容/补映射”，不要写成“云端改回旧 canonical”

排除项：

- 不要仅因执行侧不支持，就把稳定的云端 `canonical` 反判成运营配置问题
- 不要要求云端为单车型或单端侧实现回退公共归一值

## 5. 特殊场景

### 5.1 平台功能点继承标准功能点

关键规则：

- 入口平台功能点不一定是实际分析目标
- `projectId` 只决定“平台/标准”
- `fromFunctionId` 决定平台功能点是否继承标准功能点

归因要求：

- 若 `fromFunctionId` 有值，优先检查标准功能点配置
- 不要只看入口平台功能点就下结论

### 5.2 `setting_item` 字面值补泛化

当现有 `nluMapping.slots` 中出现：

```json
{"name":"setting_item","value":"原值"}
```

且本次只是给原值补泛化说法时，按下面顺序判断：

1. 先查同 slot、同 `term=原值` 的 property 是否已存在
2. 若已有 property：
   - 优先把 `nluMapping.value` 切成该 property
   - 同步把新增泛化词补进该 property
3. 若没有 property：
   - 保留字面值形式
   - 将 `nluMapping.value` 改成 `新泛化说法|原值`

典型例子：

- 有 property：不保留 `晕车|晕车舒缓`，直接切 property 并补词
- 无 property：保留 `晕车|晕车舒缓`

### 5.3 配置链路完整后的回退原则

如果下面这些都已经成立：

- 实际修改目标判断正确
- `intentList` / `slotList` 基础存在
- `nluMapping`、`slotParams`、`protocolRequest` / `operation` 链路完整
- property / 字面值表达符合规范

则先补一层 repo 核对：

- 若 `dialogScenarioBase.json` / `dialogScenario*.json` 缺少对应意图路由或错误回落到 `1919` 兜底：优先归因 `Cloud/代码问题`
- 若 repo 与 ops 配置一致且都完整：再回到运行时主链路

运行时主链路仍按：

- ASR
- NLU
- Cloud
- Vehicle
- TTS

## 6. 自动分析输出模板

### 6.1 需求/规范缺失

可直接使用：

`根据关联需求与标注规范核对，当前问题不属于运行时模型故障，根因是需求/规范侧未给出可落地的配置事实（如明确 intent），因此当前无法继续建立功能点配置链路。`

### 6.2 平台基础配置缺失

可直接使用：

`根据标注规范与平台基础配置核对，规范要求的 intent/slot 尚未进入平台基础列表（如 intentList/slotList），当前问题优先归因平台基础配置缺失，而不是运行时 ASR/NLU/Cloud 故障。`

### 6.3 功能点配置缺失

可直接使用：

`根据功能点详情核对，平台基础能力已存在，但实际功能点未挂载对应 nluMapping / slotParams / protocolRequest / operation，当前问题优先归因功能点配置缺失。`

### 6.4 Property / 泛化表达错误

可直接使用：

`根据标注规范与平台 property/字面值配置核对，当前问题根因是配置表达不一致（property、字面值或混合写法错误），导致说法覆盖范围与需求预期不一致。`

### 6.5 非配置问题，继续主链路

可直接使用：

`需求与配置链路核对后未发现直接阻塞项，当前问题不优先归因配置缺失，应继续按照 ASR -> NLU -> Cloud -> Vehicle -> TTS 主链路分析运行时故障。`
