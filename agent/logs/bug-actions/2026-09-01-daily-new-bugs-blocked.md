# 2026-09-01 每日新增 Bug 处理记录（证据访问阻塞）

- run_id：`bug-20260901T010320Z-044b7c7f-f6cd-4bd3-9b76-59865bb08cc2`
- 规则版本：`v1.16.0-trial.3`，manifest schema v5
- 操作者/目标负责人：吴优（`wu-you`）
- 查询条件：`assignee = you.wu AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in ("To Do",Reopened,"In Progress",Pending)`
- Jira 查询结果：28 条 Bug。
- 吴优线上 `bug` 页去重结果：396 个已登记行、395 个唯一 Key、1 个重复 Key。
- 本次新增：`ADS-44267`、`HUR-84049`、`HUR-84055`；计划行分别为 `bug!398`、`bug!399`、`bug!400`，均未写入。
- 权限状态：身份、负责人范围、Jira/Drive短期预检通过；实际运行中Google Drive connector不存在，Alchemy跳转SSO，MasterGo读取回执过期，因此按证据契约停止写表。
- 外部动作：未执行Jira评论、转派、关闭或状态变更；未修改Alchemy；未写线上清单或本地索引。

## ADS-44267 决策核验卡

- 备注因果链：C673-6 SWD.3.68中，指定时间天气查询展示天气大卡后挂R，AVM/360出现但仍被天气卡覆盖。完整评论中存在“设计如此”、AVM应优先于大卡、AVM为华为Activity且层级无法保证三种冲突说法；附件标注天气卡片优先级P2。
- 客户问题识别：是，客户问题编号`ID20260602134722264`；已检查客户用例，车型、软件版本、前置、步骤、输入、预期、实际和附件入口完整。
- 关联票：已完整读取`ADS-46283`全部9条评论。该票因客户接受生日场景行为而关闭为Invalid，不直接覆盖天气卡片与AVM仲裁场景。
- 证据画像与必查资料：选择general和visible_interaction；voice仅为触发且非争议点，map_navigation不适用。2026-09-01已读Jira、附件、全部评论、关联票及天气PRD本地正文；已执行Drive网页宽泛、精确文档名和版本族搜索，但当前无connector，不能形成`origin=connector`回执；MasterGo回执过期，未读到目标图层。
- 资料适用范围：`ads44267-jira`为C673-6/SWD.3.68的`implementation_actual + exact`；`ads44267-weather-prd`适用于C673-6，只证明指定时间天气查询与语音卡片能力，作为`context_only + exact`；`ads44267-layer-gap`是同项目AVM与天气卡片层级规则的`formal_target + gap`，属于关键缺口。
- 冲突处理：天气PRD没有定义AVM层级；研发/供应商评论只能证明当前实现和限制，不能替代正式目标。`ADS-46283`的生日场景客户结论不外推。本票在正式层级配置和MasterGo图层补齐前保持待会诊。
- 唯一结论：状态`待会诊`。结论：ADS-44267定义为跨域可见层级规则冲突，当前保持待会诊；天气PRD仅证明指定时间天气查询应展示天气卡片，尚不能证明挂R后天气卡片与AVM/360的优先级。
  依据：[ADS-44267 Jira原票·描述/附件/全部评论]；[天气PRD C673-6 v20250520·查询天气功能说明]；MasterGo当前图层与Drive connector回执不可用。
  处理：补齐C673-6生效层级配置和MasterGo目标图层，明确AVM Activity与P2天气卡片的仲裁规则后再判定修复或关闭；C673系统交互产品负责人处理。

ADS-44267 计划写入行398；因上述证据访问缺口未生成写表请求。

## HUR-84049 决策核验卡

- 备注因果链：J90A瑞典语用例将`Förläng med 1 timme och 15 minuter`标为露营时长减少，但原话表示延长1小时15分钟，实际执行也是增加。标准语料V0.7第485行`mode_08_05`又将中文“减少x分钟”与瑞典语`Öka varaktigheten med 1 timme 15 minuter`配对，存在同方向错配。
- 客户问题识别：否；Jira未发现标题/描述前置客户问题编号。
- 关联票：已核验无直接关联票。
- 证据画像与必查资料：选择voice；general由voice专项覆盖，map_navigation和visible_interaction不适用。2026-09-01已读Jira、附件、全部评论、J90A情景模式资料及标准语料；Drive网页搜索已执行但当前无connector，不能生成合规回执。Alchemy打开后跳转SSO，原话测试、`meta_id`、标准/项目功能点和发布下发均不可用。
- 资料适用范围：`hur84049-jira`是J90A EU瑞典语本票的`implementation_actual + exact`；`hur84049-corpus`是J90A标准语料V0.7第485行的`context_only + exact`，与本票同语义方向但不是逐字相同query；`hur84049-alchemy-gap`是当前Alchemy链路关键缺口。
- 冲突处理：Jira中文标签要求减少，瑞典语原话和实际执行均为增加；语料第485行支持存在标注错配风险，但不能代替本票当前Alchemy映射。平台恢复前不关闭为测试预期错误，也不确定性定责配置或研发。
- 唯一结论：状态`待复核`。结论：HUR-84049定义为瑞典语露营时长方向性标注疑似错误，当前保持待复核；“Förläng med 1 timme och 15 minuter”表示延长1小时15分钟，与用例中的“减少”标签相反，实际增加方向与原话一致。
  依据：[HUR-84049 Jira原票·描述/附件/全部评论]；[J90A标准语料V0.7·8_瑞典语第485行 mode_08_05]；Alchemy当前配置因SSO不可访问。
  处理：核对并修正本票中文语义标签、瑞典语音频/query与slot/canonical的同向映射，完成Alchemy标准/项目功能点及下发后回归；J90A海外语音语料产品负责人处理。

HUR-84049 计划写入行399；因上述证据访问缺口未生成写表请求。

## HUR-84055 决策核验卡

- 备注因果链：J90A瑞典语用例将`Förläng lite`标为露营时长减少一点，但原话表示延长一点，实际执行也是增加。标准语料V0.7第486行`mode_08_08`又将中文“减少一点时长”与瑞典语`Öka varaktigheten en aning`配对，存在同方向错配。
- 客户问题识别：否；Jira未发现标题/描述前置客户问题编号。
- 关联票：已核验无直接关联票。
- 证据画像与必查资料：选择voice；general由voice专项覆盖，map_navigation和visible_interaction不适用。2026-09-01已读Jira、附件、全部评论、J90A情景模式资料及标准语料；Drive网页搜索已执行但当前无connector，不能生成合规回执。Alchemy打开后跳转SSO，原话测试、`meta_id`、标准/项目功能点和发布下发均不可用。
- 资料适用范围：`hur84055-jira`是J90A EU瑞典语本票的`implementation_actual + exact`；`hur84055-corpus`是J90A标准语料V0.7第486行的`context_only + exact`，与本票同语义方向但不是逐字相同query；`hur84055-alchemy-gap`是当前Alchemy链路关键缺口。
- 冲突处理：Jira中文标签要求减少一点，瑞典语原话和实际执行均为增加一点；语料第486行支持存在标注错配风险，但不能代替本票当前Alchemy映射。平台恢复前不关闭为测试预期错误，也不确定性定责配置或研发。
- 唯一结论：状态`待复核`。结论：HUR-84055定义为瑞典语露营时长方向性标注疑似错误，当前保持待复核；“Förläng lite”表示延长一点，与用例中的“减少一点”标签相反，实际增加方向与原话一致。
  依据：[HUR-84055 Jira原票·描述/附件/全部评论]；[J90A标准语料V0.7·8_瑞典语第486行 mode_08_08]；Alchemy当前配置因SSO不可访问。
  处理：核对并修正本票中文语义标签、瑞典语音频/query与slot/canonical的同向映射，确认模糊步长10分钟，完成Alchemy标准/项目功能点及下发后回归；J90A海外语音语料产品负责人处理。

HUR-84055 计划写入行400；因上述证据访问缺口未生成写表请求。

## 运行收口

- 三条schema v5 manifest均保存真实已读来源和不可用限制；`search_receipts`为空，未伪造connector回执或`results_count=0`。
- 三条manifest、三张逐Key核验卡和整批prewrite bundle的结构校验均通过；原始结果保存于`bug-20260901T010320Z-044b7c7f-f6cd-4bd3-9b76-59865bb08cc2-prewrite-validation.json`。该结果只证明blocked记录结构合规，不解除平台访问门槛。
- 未生成Sheet build/patch请求；`bug!398:400`未写入，因此不存在A:J回读、校验JSON或`readback_sha256`。
- 未修改`agent/bug-owners/wu-you/index.md`；该文件已有的工作树修改属于其他运行。
- 本次run保持`planned/blocked`，待Google Drive connector、Alchemy登录和MasterGo当前图层访问恢复后继续同一run或以新run重新去重处理。
