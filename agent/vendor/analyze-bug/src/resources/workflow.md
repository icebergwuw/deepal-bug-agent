## Trigger

- 当用户要求分析 Jira issue key（例如 `AT-29523`）或要求自动检索 Debug 日志并生成 Jira 评论时，启用本技能。
- 如果用户没有提供明确的 Jira issue key，先要求用户补充 issue key，再开始分析。

## Core Rules

1. 保持原有五阶段分析流程不变：获取与解析、日志检索、运营配置与规则判定、输出报告、汇总票回填。
2. 外部系统访问优先通过 MCP 完成：
   - Jira: `get_jira_issue`、`add_jira_comment`、`update_jira_description`
   - Debug: `fetch_debug_log_list`、`get_debug_log_detail`
   - Rules: `get_analysis_rules`、`get_module_rules`、`get_fault_priority`、`get_rules_version`
   - Ops: `list_intents`、`list_slots`、`list_slot_properties`、`list_standard_functions`、`list_functions`、`get_standard_function_detail`、`get_function_detail`、`get_function_vehicle_config`、`list_projects`、`get_project_detail`、`list_project_functions`
3. 允许调用 shell / JSON / 文本处理工具做本地辅助工作，例如时间转换、JSON 摘要、日志字段过滤、repo 静态搜索；不要用 shell 直接替代 Jira、Debug、Rules、Ops 的职责。
4. `online-dialogue` 代码是可选增强，不是前置依赖；没有本地代码时只结合 Jira + Debug + Rules + Ops 分析。
5. 若日志显示 Query 中的关键对象、目标词或功能词与 NLU 命中的 intent 明显冲突，或 intent 与已抽取 slot / property 自相矛盾，应优先归因为 `NLU`；后续 operation、TTS、车端执行仅作为连带现象，不再继续归责到 Cloud / Vehicle / TTS。
6. 运营配置链路优先于运行时规则判责；若运营配置已足以解释问题，不再强行归类到 Cloud。
7. 除 Bugfree 汇总票外，最终 Jira 评论统一使用固定四段式；只有在已能定位主因时才允许写 `【解决方案】`：

```text
【基础信息】
【诊断证据】
【问题原因】
【解决方案】责任方：xxx。balabala修复建议。
（AI Generated）
```

## Phase 1: Fetch And Parse

1. 调用 `get_jira_issue(issue_key)` 获取问题详情。
2. 从标题、描述、评论、自定义字段中提取：
   - 车辆标识：优先 VIN，其次 VID
   - 发生时间
   - 用户语音 Query
   - 用户期望和实际结果
   - `rid/requestId`
   - `metaId/functionId/projectId/fromFunctionId`
   - 评论中已有的判责线索、预期功能点、日志链接
3. 识别是否为汇总票：
   - 标题包含 `bugfree`
   - 描述中存在 Markdown 表格
4. 缺字段时按以下顺序退出：
   - 凭证/权限错误
   - Issue 不存在
   - VIN/VID 缺失
   - 时间缺失
   - 描述不清晰

### 车辆标识提取

- VIN 优先于 VID。
- VIN 识别规则：`[A-HJ-NPR-Z0-9]{11,17}`
- VID 识别规则：`VID:123456`、`vid=123456`、6-15 位纯数字。
- 若 VIN 与 VID 都缺失，调用 `add_jira_comment` 提醒报告人补充。

## Phase 2: Debug Retrieval

调用 `fetch_debug_log_list` 时忽略 `request_id` 为 `kk-` 的测试数据。

### 检索顺序

1. Online 精确匹配：`VIN/VID + Query + 时间 ±10 分钟`
2. Online 模糊匹配：`VIN/VID + query=None + 时间 ±10 分钟`
3. Offline 精确匹配
4. Offline 模糊匹配
5. 扩大时间范围到 ±30 分钟后重试
6. 只按 VIN 检索最近日志
7. 全部失败则输出“无法找到日志”报告

### 日志详情

- 找到候选日志后调用 `get_debug_log_detail`
- 如需补充 ASR 链路，可继续读取 `asr` 详情
- 若日志不完整，直接走“日志不完整”退出模板

## Phase 3: NLU Gate And Ops-First Diagnosis

### Step 0: NLU 前置校验

在进入 ops 链路前，先检查是否已经满足 NLU 归因条件。满足任一项时，直接归因 `NLU`，不要再被后续 Cloud / Vehicle / TTS 现象带偏：

1. `Query` 的关键目标对象与命中 intent 语义冲突
   - 例如 Query 明确说“远光灯”，但 intent 命中 `light_low_beam_height_adjust`
2. 已抽取 slot / property 与命中 intent 自相矛盾
   - 例如 slot `control_target=high_beam_light`，但 intent 却指向 low beam / 近光灯语义
3. 本地 `intentDomainMapping` 或 `dialogScenarioBase.json` 已存在更匹配的标准 intent / path，但日志命中了另一条旧 intent 或降级 intent
4. 后续 `operation`、`tts`、车端执行错误能够被“前置 intent 错误”完整解释

命中以上任一情况时：

- 主责直接写 `NLU`
- 关键证据优先引用 `query / asr / intent / slotMap / local config`
- `operation / tts / 车端执行` 只写成连带结果，不再写成 Cloud 主责

### Step 1: 运营配置链路诊断

分析运营配置问题时，按需参考 analyze-bug runtime 内置文档 `src/resources/config-bug-foundation.md`；这是懒加载分析文档，只在进入运营配置排查时再读取，不要在其他场景预先加载。

按下面顺序固定排查：

1. 判断实际分析目标
   - `projectId` 为空：标准功能点
   - `projectId` 非空且 `fromFunctionId` 为空：平台功能点
   - `projectId` 非空且 `fromFunctionId` 非空：回到 `fromFunctionId` 对应的标准功能点
2. 检查平台基础
   - `list_intents`
   - `list_slots`
3. 检查功能点链路
   - `list_standard_functions` / `list_functions` / `list_project_functions`
   - `get_standard_function_detail` / `get_function_detail`
   - `get_function_vehicle_config`
4. 检查表达层
   - `list_slot_properties`
   - `canonical` / `literal` / `property` / 混合写法
   - 若日志已显示云端下发了明确、稳定且语义正确的 `canonical`，后续优先以该 `canonical` 作为事实基线，不要反过来要求云端迁就下游旧枚举

### Step 2: 归因回退

- 若已命中 Step 0 的 intent / slot 冲突：归因 `NLU`
- 平台基础缺失：归因“运营配置问题”
- `nluMapping` / `slotParams` / `protocolRequest` / `operation` 缺失：归因“运营配置问题”
- `slotProperty` / `canonical` / 同义词边界错误：仅在 ops/云端侧缺失、错配、语义错误时归因“运营配置问题”
- 若云端已下发稳定、明确且语义正确的 `canonical`，但下游执行侧仍不支持该值、只支持旧枚举或错误回落：优先归因“Vehicle/车端适配问题”，不要要求云端把 `canonical` 改回下游私有枚举
- 若 ops 侧功能点、映射、接口、表达层都完整，但本地 `online-dialogue` 缺少对应 `dialogScenario` 路由或只落到 `1919` 这类兜底：归因“Cloud 问题”
- 配置链路完整后仍异常：再调用 `get_fault_priority` 和 `get_module_rules(module)` 回到原 `Acoustics -> ASR -> NLU -> Cloud -> Vehicle -> TTS` 判责链路
- 若最终不属于运营配置，也不属于 Cloud，应允许结论停在 `App/UI/产品边界`，不要强行补成 Cloud

## Phase 4: Code Evidence

### 何时结合本地代码

只有在以下两种情况下才下钻本地 `online-dialogue`：

1. 已判定为运营配置问题
   - 静态核对 repo 配置与运营平台配置是否一致
2. 已判定为 Cloud 问题
   - 前提是 ops 侧配置已经完整
   - 根据日志里的 `intent/meta/operation/query` 静态定位相关类、配置、调用链
   - 重点检查 `dialogScenarioBase.json` / `dialogScenario*.json` 是否缺少对应路由，或是否错误回落到 `1919` 兜底

### 代码仓探测顺序

1. `ONLINE_DIALOGUE_ROOT`
2. 当前工作目录就是 `online-dialogue`
3. 当前工作目录同级目录存在 `online-dialogue`
4. `~/Code/online-dialogue`

### 代码分析约束

- 只做静态定位，不编译、不启动、不复现
- 优先读取：
  - `online-dialogue/AGENTS.md`
  - `online-dialogue/ai-doc/req-skill/requirement-delivery-workflow.md`
  - `dialogue-common/src/main/resources/config/dialogScenarioBase.json`
  - `dialogue-common/src/main/resources/config/slotPropertyDict.properties`
- 无本地代码时，明确写“本地代码缺失，本次仅基于运营系统与日志分析”

## Phase 5: Report

分析完成后调用 `add_jira_comment` 发布中文报告。不要使用 Emoji。
评论正文末尾必须显式包含 `（AI Generated）` 标识，用于区分 AI 分析评论。
`jira-analyzer` 服务端也会尝试追加同样的标识，并会把旧的 `(AI Generated Response)` / `(AI Generated)` 统一规范成 `（AI Generated）`，因此正文里仍然不要省略这行。

### 非 Bugfree 票固定格式

```text
【基础信息】
- 车辆标识: {VIN 或 VID}
- 发生时间: {TIME}
- 用户语音: {QUERY}
- reqId: {RID}

【诊断证据】
1. {证据1}
2. {证据2}

【问题原因】
{一句话写清直接原因；若能判断到根因，继续补充根因；若无法定位则写“未能定位问题”}

【解决方案】责任方：{RESPONSIBILITY}。{可执行修复建议}

（AI Generated）
```

约束：

- `【基础信息】` 保留最关键的上下文，不写冗余字段
- `【诊断证据】` 至少两条，优先使用日志证据、运营配置证据、代码证据
- `【问题原因】` 只写一个主责结论，但必须用一句完整中文说明“什么直接导致了问题”
- `【问题原因】` 禁止只写模块名或单个标签，例如不能只写 `NLU`、`Cloud`、`运营配置问题`
- 若能判断到根因，优先写成“直接原因 + 根因”合并的一句话
- 若最终归因是云端或运营配置问题，`【解决方案】` 必须给出可执行改动建议
- 若最终归因是 `Vehicle/车端适配问题`，`【解决方案】` 应明确要求车端按云端既有 `canonical` 做兼容或映射，不要把建议写成“云端回退 canonical”
- 若最终归因是其他模块，`【解决方案】` 可以给基于原因的简要建议
- 若未能定位问题，`【问题原因】` 固定写“未能定位问题”，并且不要写 `【解决方案】`
- Bugfree 汇总票不使用上述四段式，继续按表格回填和单独汇总评论执行

### 退出模板

- 问题描述不清晰：提醒补充 Query、期望结果、实际结果
- 时间缺失：提醒补充精确到分钟的发生时间
- 日志不完整：列出已获取字段、缺失字段、可能原因
- 证据不足：列出已排除模块、存疑点、人工介入建议
- 日志缺失：列出已尝试检索策略与建议
- 运营系统不可用：说明已按降级路径仅基于 Jira + Debug + Rules 分析

## Bugfree 汇总票

1. 逐行解析 Markdown 表格。
2. 每完成一行分析就调用 `update_jira_description` 实时回填。
3. 回填必须严格保持原表格结构，不新增列、不破坏对齐、不插入额外空行。
4. 仅在存在合适列时回填：
   - `req_id/Rid/request_id`
   - `模块/责任方/责任判定`
   - `备注/分析结果/分析结论`
5. 全部完成后再发布一条汇总评论，统计总条目数与各模块故障分布。

## Error Handling

- `CREDENTIAL_MISSING`: 提示运行 `analyze-bug-admin configure-jira`
- `COOKIE_MISSING`: 提示运行 `analyze-bug-admin configure-debug`
- `COOKIE_EXPIRED`: 提示更新 Cookie
- `NOT_FOUND`: 提示检查 Issue Key
- `UNAUTHORIZED`: 提示检查 Jira 用户名密码
- `FORBIDDEN`: 提示确认权限
- `TIMEOUT` / `NETWORK_ERROR`: 重试一次，仍失败则报告稍后重试
- 运营系统缺凭证：提示运行 `analyze-bug-admin configure-ops`
