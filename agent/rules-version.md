# Bug 处理规则版本

- 当前版本：`v1.14.0-trial.1`
- 状态：`trial`
- 生效日期：`2026-08-17`
- 适用范围：`.gitignore`、`AGENTS.md`、`README.md`、`agent/onboarding.md`、`agent/evidence-contract.md`、`agent/output-contract.md`、`agent/workflows/bug.md`、`agent/workflows/review.md`、`agent/sheet-contract.md`、`agent/config/evidence-requirements.json`、`agent/config/external-skills.json`、`agent/config/sheet-update-modes.json`、`agent/config/local-profile.example.json`、`agent/context.md`、`agent/bug-owners/registry.yaml`、`agent/product-kb/rules/jira-comment-signals.md`、`agent/logs/bug-actions/README.md`、`agent/skills/deepal-product-bug-handler/SKILL.md`、`agent/scripts/bug_project_preflight.py`、`agent/scripts/bug_sheet_contract.py`、`agent/scripts/validate_bug_evidence_gate.py`、`agent/scripts/validate_bug_run.py`、`agent/scripts/sync_bug_skill.py`、`agent/scripts/test_bug_project_preflight.py`、`agent/scripts/test_bug_evidence_gate.py`、`agent/scripts/test_bug_run.py`、`agent/scripts/test_bug_sheet_contract.py`、`agent/scripts/validate_rule_architecture.py`、`agent/archive/scripts/README.md`
- Skill 管理：Bug 流程使用本仓库 `agent/skills/deepal-product-bug-handler/SKILL.md`；UE 语音覆盖审核是 `agent/config/external-skills.json` 登记的独立私有 Skill。外部 Skill 从自己的 `VERSION` 读取版本，不使用本文件的 Bug 规则版本。
- 说明：当前目录从 `v1.1.0-trial.3` 起使用本地 Git `main` 分支管理；本文件继续记录业务规则版本、试行状态、验证案例和回滚口径。更早版本没有 Git 提交，不追溯伪造。

## 版本规则

- `MAJOR`：列职责、默认授权边界或完整流程发生不兼容变化。
- `MINOR`：新增证据门槛、写表契约或核验步骤。
- `PATCH`：不改变职责边界的文字澄清和缺陷修正。
- `trial.N`：试行次数；用户确认转正后移除 trial 标记。
- 每次修改必须记录日期、原因、影响文件、验证案例和回滚口径，并在 `agent/logs/bug-actions/` 留痕。

## v1.14.0-trial.1 — 2026-08-17

### 试行内容

- manifest 升级为 `schema_version=5`。每个 Drive 候选必须显式登记正文引用；引用文档必须按完整名称追搜并绑定 `exact_document_name` 回执。
- 标题含版本号的候选必须登记版本族，绑定 `version_family` 枚举回执，选择一个已读候选并确认已检查更新版本。
- 新增 `search_completion` 闭环门禁；引用链未追完、版本族未枚举、精确名称回执缺失或选中版本未读时，禁止生成写表请求。
- 多份检索回执改为合并覆盖必查动作的声明查询，支持宽泛检索、精确文档名追查和版本族枚举分别留痕。

### 修改原因

- HUR-81975 的首次复查虽然通过 v4 候选审计，但只停留在功能清单和宽泛 Drive 搜索，没有按清单中的系统设置定义全名继续追查，也没有枚举同系列 V2.1、V2.2、V2.3，导致“未找到定义”的错误结论通过门禁。
- 原规则已有“命中索引后追原文”的文字要求，但脚本无法识别引用链和版本选择是否完成，需要把要求变成结构化、可失败的机器校验。

### 影响文件

- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/config/evidence-requirements.json`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-17-drive-search-completion-gate-v1.14.0-trial.1.md`

### 验证案例

- 候选正文声明系统设置功能定义，但未登记引用追查时，门禁必须拒绝。
- 引用追查只绑定宽泛查询、没有 `exact_document_name` 回执时，门禁必须拒绝。
- 版本化候选未登记版本族，或没有 `version_family` 回执、已读选中版本和更新版本确认时，门禁必须拒绝。
- 精确文档名回执与版本族回执齐全、最新适用候选审计为 `read` 时，门禁通过。
- 全套 Bug 证据、run bundle、表格契约、预检与规则架构测试必须通过。

### 回滚口径

- 通过新提交恢复 `v1.13.1-trial.1` 的 schema v4 门禁，不使用 `git reset --hard`。
- 回滚不改写已有 v5 manifest 或本次规则维护日志；它们保留为历史证据，后续重新处理时明确选择当前生效 schema。

## v1.13.1-trial.1 — 2026-08-14

### 试行内容

- 将 `audit-ue-voice-coverage` 从 Bug 规则仓库拆分到独立私有 GitHub 仓库，以 `v1.0.0` 和精确提交号独立管理。
- Bug 仓库只保留外部 Skill 依赖声明、审核 manifest 和操作日志，不再保留第二份 Skill 源码。
- 架构校验新增外部 Skill 的私有性、语义版本和精确提交锁定检查。

### 修改原因

- UE 语音覆盖审核流程与 Bug 处理规则是两个不同产品；共用 `v1.13` 会让同事误以为 Skill 版本等于 Bug 处理规则版本。
- 单一源仓库可以让同事直接安装和升级 Skill，避免 Bug 仓库中的复制源码漂移。

### 影响文件

- `AGENTS.md`
- `agent/config/external-skills.json`
- `agent/rules-version.md`
- `agent/scripts/validate_rule_architecture.py`
- `agent/logs/bug-actions/2026-08-14-audit-skill-repository-split.md`
- 删除当前源码中的 `agent/skills/audit-ue-voice-coverage/`，历史记录中的原路径保留不变。

### 验证案例

- 独立 Skill 结构校验、团队来源校验和三份已有语音覆盖 manifest 校验全部通过。
- Bug 项目架构校验必须识别外部 Skill 的私有仓库、`v1.0.0` 和 40 位提交号。
- 删除 Bug 仓库中的 Skill 副本后，现有 Bug 单元测试和审核 manifest 校验仍必须通过。

### 回滚口径

- 通过新提交恢复 `v1.13.0-trial.1`，不使用 `git reset --hard`。
- 回滚 Bug 仓库引用不删除已创建的独立私有 Skill 仓库、标签或历史审核记录。

## v1.13.0-trial.1 — 2026-08-14

### 试行内容

- UE 语音覆盖 Skill 增加独立操作者绑定门槛：首次使用必须询问姓名，不得从系统用户名、浏览器账号、Git 作者或聊天称呼推断身份；确认前只允许只读发现。
- 预载吴优、冯智秀、罗稚钦、李欣四人的工作模块来源，按各自真实页签与 module/UE 列映射读取，不再假设同一工作簿结构。
- 非预载人员必须在授权 Drive 检索其工作说明或工作模块表，打开候选并让操作者确认精确文件与页签后才能本地绑定。
- 新增 `validate_team_sources.py`，阻止负责人、显示名、页签映射、列名或模块列表重复/缺失。

### 修改原因

- 团队成员使用不同工作簿、不同页签和不同列保存负责模块；只预载 URL 的默认 gid 会落到问题或 Bug 页，无法稳定找到模块和 UE。
- 用户要求 Skill 首次使用确认操作者，名单外人员必须通过 Drive 查找并引导确认，且需要把流程上传 GitHub 供同事使用。

### 影响文件

- `.gitignore`
- `agent/rules-version.md`
- `agent/skills/audit-ue-voice-coverage/SKILL.md`
- `agent/skills/audit-ue-voice-coverage/references/team-module-sources.json`
- `agent/skills/audit-ue-voice-coverage/scripts/validate_team_sources.py`
- `agent/logs/bug-actions/2026-08-14-charge-discharge-voice-coverage.md`
- `agent/logs/bug-actions/2026-08-14-charge-discharge-voice-coverage-audit.json`

### 验证案例

- 四位预载负责人均有唯一 owner id、显示名、工作簿与至少一个模块页签；冯智秀使用 A/D 列、罗稚钦使用 B/F 列、李欣使用 A/G 列、吴优使用 B/F 列。
- 充放电审核记录 35 组控件、72 条精确 Alchemy 指令；21 组通过，14 组失败写入线上表格 `A57:I70` 并逐字回读一致。
- 将负责人显示名、页签映射或模块名改为重复值时，团队来源校验器必须拒绝。
- 本地审核身份文件保持 Git 忽略，Skill 来源文件不包含密码、Cookie、Token 或浏览器会话。

### 回滚口径

- 通过新提交恢复 v1.12.0-trial.1，不使用 `git reset --hard`。
- 回滚不得删除本次线上充放电审核结果、审核日志或 manifest；团队来源映射作为历史证据保留。

## v1.12.0-trial.1 — 2026-08-14

### 试行内容

- UE 语音覆盖审核新增操作语境门槛：配置触发条件、前置条件、执行动作、自动化或内容对象时，必须核对 operation 是否修改指定父对象；立即执行底层车控不算配置成功。
- manifest 新增 `expected_effect`、`operation_check.context_match` 和可选 `tested_queries`。`configure` 与 `content_operation` 必须提供布尔型 `context_match`，通过项必须为 `true`。
- 大型 UE 允许按独立可实现能力点聚合写表；相同控件的席位、模式和数值可合并，但触发条件、前置条件和执行动作等不同语义上下文必须分开，并在 `tested_queries` 保留全部精确实测。

### 修改原因

- 场景积木 V1.0 真实审核中，多条指令返回了目标、动作和值均正确的即时车控，但没有把该动作写入场景积木配置。原三项 operation check 无法机器区分该类假通过。
- 执行动作页包含大量重复位置与数值，逐口令写表会产生不可实现的重复行，需要固定可追溯的聚合粒度。

### 影响文件

- `agent/rules-version.md`
- `agent/skills/audit-ue-voice-coverage/SKILL.md`
- `agent/skills/audit-ue-voice-coverage/references/audit-contract.md`
- `agent/skills/audit-ue-voice-coverage/scripts/validate_audit.py`
- `agent/logs/bug-actions/2026-08-14-scene-block-voice-coverage.md`
- `agent/logs/bug-actions/2026-08-14-scene-block-voice-coverage-audit.json`

### 验证案例

- 场景积木 manifest 包含 11 个页面状态、42 个汇总控件、121 条精确查询；41 个失败项写入线上表格，1 个通过项不申报。
- `把场景积木的执行动作设置为四门车窗开度50%` 返回即时开窗 operation，`context_match=false`，按 `misrouted` 申报。
- 负向用例将 `expected_effect=configure`、`verdict=pass` 与 `context_match=false` 组合时，校验器必须拒绝。
- 线上表格 `A16:I56` 写后逐字回读一致，原有 `A1:I15` 未修改。

### 回滚口径

- 通过新提交恢复 v1.11.0-trial.1，不使用 `git reset --hard`。
- 回滚规则不得删除本次线上场景积木审核结果；审核日志和 manifest 作为历史证据保留。

## v1.11.0-trial.1 — 2026-08-14

### 试行内容

- 新增 `audit-ue-voice-coverage` Skill，用于从负责模块和 UE 链接出发，逐项核验 MasterGo/Drive 当前有效控件与 Alchemy 实际语音执行结果，并更新语音覆盖走查表。
- 增加页面状态硬门槛：MasterGo MCP 能读取到节点不代表需求仍有效；标记为删除、搁置、废弃、草稿、备份或历史版本的页面禁止测试和申报，结构读取必须结合当前画布视觉状态。
- 增加 Alchemy 正确性门槛：`classification=task` 不代表通过；必须核对目标、动作及必要值。误映射、空 canonical、仅聊天文本、场景阻断和 GUI-only 均按失败分类。
- 新增 `validate_audit.py` 和审核 manifest，机器阻止非 active 页面控件进入申报，并要求通过项的目标、动作和值全部匹配。

### 修改原因

- 首次情景模式走查只按可抽取控件判断，未识别 V1.9 第 3、4 页恒温座舱的删除区域和“离车不下电模式（搁置）”状态，导致搁置功能被误写入申报表。
- 用户明确要求只保留“UE 中存在且未删除、语音平台无法正确执行”的能力，并要求把审核流程固化为 Skill。

### 影响文件

- `AGENTS.md`
- `agent/rules-version.md`
- `agent/skills/audit-ue-voice-coverage/SKILL.md`
- `agent/skills/audit-ue-voice-coverage/agents/openai.yaml`
- `agent/skills/audit-ue-voice-coverage/references/audit-contract.md`
- `agent/skills/audit-ue-voice-coverage/scripts/validate_audit.py`
- `agent/logs/bug-actions/2026-08-14-scenario-voice-coverage.md`
- `agent/logs/bug-actions/2026-08-14-scenario-voice-coverage-audit.json`

### 验证案例

- 情景模式审核 manifest 校验通过；将控件绑定到 `deleted` 页面时校验器拒绝通过。
- Skill `quick_validate.py` 结构校验通过。
- 线上表格将“离车不下电模式大灯设置”替换为“睡眠空间座椅设置入口”，回读 `A2:I15` 与最终 13 项一致。

### 回滚口径

- 通过新提交恢复 v1.10.1-trial.1，不使用 `git reset --hard`。
- 回滚不得恢复已确认属于搁置页面的“离车不下电模式大灯设置”申报项；本次审核日志和 manifest 作为历史证据保留。

## v1.10.1-trial.1 — 2026-08-12

### 试行内容

- 固化用户授权：项目规则、脚本、索引、操作日志、知识库或会议沉淀更新通过校验和敏感信息检查后，必须提交并推送当前分支的受控私有GitHub远端。
- 只有远端确认包含新提交后才能报告“已上传”；无变化不创建空提交，远端不可达、权限失败或私有性无法确认时停止并报告具体状态。
- 修正Bug与复盘流程中遗留的`schema_version=3`文字为当前schema v4，并修正表格写后校验序号。

### 修改原因

- 用户明确要求本次上传且以后所有项目更新均上传GitHub；此前v1.10修复仅在本地，未提交和推送。
- 当前Bug与复盘流程残留schema v3文字，可能误导后续执行生成旧manifest。

### 影响文件

- `AGENTS.md`
- `agent/onboarding.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-12-github-delivery-policy-v1.10.1-trial.1.md`

### 验证案例

- 架构、证据门禁、run bundle、表格契约和preflight测试全部通过；全仓敏感信息检查和`git diff --check`通过。
- 本次提交推送后，用`git ls-remote origin refs/heads/main`核对远端main指向新提交。

### 回滚口径

- 通过新提交恢复v1.10.0-trial.1，不使用`git reset --hard`；用户持续上传授权如需撤销，必须由用户明确提出。

## v1.10.0-trial.1 — 2026-08-12

### 试行内容

- manifest 升级为 `schema_version=4`：Drive 类必查动作在 `read / not_found` 时都必须绑定真实检索回执，候选数量和 id 必须与回执逐项一致，禁止用人工 `results_count=0` 隐藏命中项。
- 新增 `run_context`、唯一 `run_id` 和 run bundle；每票 manifest、操作者、目标负责人、页签、行号及逐 Key 决策卡必须在写前一致。
- 新增 `validate_bug_run.py`：写后必须保存原始 A:J 回读、校验 JSON 和 `readback_sha256`，最终校验通过后才可报告完成。
- 自动化无新增时也必须保存查询范围、计数、去重结果、明确“本次无新增”的日志及 `status=no_changes` run bundle。

### 修改原因

- 2026-08-12 首次每日新增批次虽完成 11 行写入和在线回读，但 manifest 将实际命中的 Drive 强候选统一记为 `results_count=0`，现有门禁仍通过；批量日志也缺逐 Key 七项卡、run_id 和落盘回读证据。
- 现行文字规则已经要求打开候选和完整留痕，问题位于执行层缺少可校验的来源回执与运行闭环，因此本次只加硬门禁，不改变产品判断口径。

### 影响文件

- `agent/config/evidence-requirements.json`
- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/sheet-contract.md`
- `agent/logs/bug-actions/README.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/validate_bug_run.py`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/test_bug_run.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/archive/scripts/README.md`
- `agent/archive/scripts/rebuild_2026_08_12_run_closure.py`
- `agent/archive/scripts/build_2026_08_12_recheck_patches.py`
- `agent/archive/scripts/validate_2026_08_12_recheck.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-12-run-evidence-log-closure-v1.10.0-trial.1.md`

### 验证案例

- Drive 回执存在结果而候选审计写 0、回执缺失或候选 id 不匹配时，证据门禁拒绝通过。
- 写表前 run bundle 缺任一 manifest、逐 Key 决策卡、负责人、页签或行号时拒绝；写后缺回读、校验文件或 sha256 不一致时拒绝完成。
- 无新增运行仍需有操作日志和 no_changes bundle；缺“本次无新增”时拒绝完成。

### 回滚口径

- 通过新的 Git 提交恢复 v1.9.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得删除本次操作日志、检索回执、run bundle 或回读证据；schema v4 作为历史证据保留，不改写为旧版本。

## v1.9.0-trial.1 — 2026-08-11

### 试行内容

- 将固定“吴优”身份改为本机显式绑定身份：首次克隆必须从 `registry.yaml` 选择负责人并生成已忽略的 `agent/config/local-profile.json`；不得根据电脑用户名、Git作者或浏览器账号猜身份。
- 新增 `agent/onboarding.md` 与 `bug_project_preflight.py`：默认只允许写绑定操作者自己的负责人页；代处理其他负责人时必须显式扩展本机范围。
- Jira、Google Drive/Sheets为完整流程基础权限；Alchemy和MasterGo按证据画像要求。平台必须先完成真实读取，再记录24小时短期回执；预检失败时强制只读并输出逐项登录/授权引导。
- Skill模板和安装脚本去除吴优电脑绝对路径，改为从仓库根目录、`$CODEX_HOME` 或当前用户目录动态定位。
- 明确Git只传递规则和脚本，不传递身份、Token、Cookie、连接器授权、浏览器会话或定时任务；仓库只能使用访问受控的私有远端。
- 本地 `.env` 除必须保持 Git 忽略外，还必须使用仅当前用户可读写的权限；权限过宽时预检拒绝写入并给出修复指引。

### 修改原因

- 当前仓库克隆到组员电脑后仍默认“用户是吴优”，存在错误产品视角和误写负责人页风险。
- `sync_bug_skill.py` 写死 `/Users/you.wu`，在其他电脑无法安装；Jira、Drive、Alchemy、MasterGo缺少首次登录与权限核验入口。
- 仅依靠“访问失败后降级”不足以完成团队交接，需要在任何写入前机器化校验本机身份、负责人范围和必需平台。

### 影响文件

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `agent/onboarding.md`
- `agent/context.md`
- `agent/output-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/config/local-profile.example.json`
- `agent/skills/deepal-product-bug-handler/SKILL.md`
- `agent/scripts/bug_project_preflight.py`
- `agent/scripts/test_bug_project_preflight.py`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/sync_bug_skill.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-11-team-onboarding-gate-v1.9.0-trial.1.md`

### 验证案例

- 新电脑无本机身份时预检返回 `mode=read_only` 并引导列出/绑定负责人；`pending + read_only` 人员不能初始化为可写身份。
- 本机默认仅允许绑定操作者负责人页；目标负责人不在 `allowed_write_owner_ids` 时拒绝写入。
- Jira/Drive短期回执缺失或超过24小时，要求真实读取后重新标记；任何本机配置均不包含凭据。
- `.env` 不进入Git且权限为 `0600`；权限过宽时预检自动降级为只读。
- Skill安装路径随当前用户或 `$CODEX_HOME` 变化，Git模板和安装副本保持一致。
- onboarding单测、证据门禁测试、表格契约测试、规则架构校验、Skill同步校验、敏感信息扫描和 `git diff --check` 全部通过。

### 回滚口径

- 通过新的Git提交恢复v1.8.0-trial.1对应规则，不使用`git reset --hard`。
- 回滚不得把本机身份、Token、Cookie或连接器授权纳入Git，也不得恢复任何用户专属绝对路径。

## v1.8.0-trial.1 — 2026-08-11

### 试行内容

- manifest 升级为 `schema_version=3`；检索词改为带 `kind` 的结构化 query，并由机器配置按必查动作要求 Jira key、问题概念、模块资料、原话、功能点或项目范围等检索维度。
- Drive、PRD、UE、交互和正式配置检索在写 `not_found` 时必须提交 `candidate_audit`；检索命中的强候选逐项记录 `read / excluded / unavailable`。已读候选必须登记为来源，并以 `gap` 表示资料缺少目标条款，不能隐藏为“未找到资料”。
- `bug_sheet_contract.py` 的 `build / patch` 请求必须绑定每票已通过校验且 Jira key 一致的 schema v3 manifest；缺失、无效、重复或错配时不生成写表请求。
- `agent/scripts/` 改为显式允许清单；四个历史一次性批量构建脚本移入 `agent/archive/scripts/`，架构校验会拒绝新的未登记脚本进入操作目录。

### 修改原因

- HUR-82937、HUR-82934、HUR-82949 和 HUR-82655 的处理暴露出执行层可只用 Jira key 与标题片段登记“未找到资料”，未打开实际命中的 PRD/UE 候选，之后仍能通过 schema v2 门禁并生成写表请求。
- 复核证明旧门禁只验证 `queries` 非空；即使替换为无语义的单字符字符串也能通过。问题不是原规则完全没有要求，而是检索质量、候选审计和写表入口之间缺少机器闭环。

### 影响文件

- `README.md`
- `agent/config/evidence-requirements.json`
- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/sheet-contract.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/archive/scripts/README.md`
- `agent/archive/scripts/build_2026_08_07_batch_recheck.py`
- `agent/archive/scripts/build_2026_08_07_recheck_artifacts.py`
- `agent/archive/scripts/build_2026_08_07_rows_159_176.py`
- `agent/archive/scripts/build_2026_08_11_non_wenyan_batch.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-11-evidence-search-gate-v1.8.0-trial.1.md`

### 验证案例

- 普通字符串 query、缺必要语义维度、Drive `not_found` 缺候选审计、已读候选仍写 `not_found` 均被门禁拒绝。
- 写表请求缺 manifest、manifest 的 Jira key 错配或同票重复 manifest 均被拒绝；schema v3 且 key 一致时通过。
- 架构校验确认 schema v3 配置完整、门禁和写表工具消费新字段，并阻止一次性脚本返回操作目录。
- `python3 agent/scripts/test_bug_evidence_gate.py` 通过 26 项；`python3 agent/scripts/test_bug_sheet_contract.py` 通过 15 项；`python3 agent/scripts/validate_rule_architecture.py` 返回 `ok: true`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.7.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得删除本次审计日志或 `agent/archive/scripts/` 中的历史脚本；schema v3 manifest 作为历史证据保留，不改写成旧格式。

## v1.7.0-trial.1 — 2026-08-06

### 试行内容

- 新增 `agent/config/evidence-requirements.json`，把通用、语音、地图导航、可见交互四类证据画像及其必查动作设为唯一机器可读配置；一个 Bug 可同时命中多个画像，且必须逐项说明选择或排除理由。
- manifest 升级为 `schema_version=2`；每条资料必须登记 `source_type`，每个必查动作必须留存检索日期、入口、关键词、状态、来源引用或精确不可用限制。
- 地图导航强制检索 Drive 主 PRD 和专项定义；可见交互强制检索生效配置和交互文档/UE；语音在正式定义之外继续强制核验 Alchemy 当前结果、标准功能点和项目功能点。
- Alchemy 当前结果、Jira、日志不能充当 `formal_target`；Alchemy 标准/项目定义也不能单独替代产品交互目标。资料缺失时只能在完整记录检索轨迹和限制后降级为待定结论。
- 普通 D 写入和复盘 H 写入共用同一证据门禁；批量日志必须按 Jira key 分别提供完整七项决策核验卡。

### 修改原因

- PC-38036 与 PC-37808 的旧 manifest 能在未证明已检索 Drive 正式定义、专项 PRD 或 UE 的情况下通过门禁。文字规则已有查资料要求，但机器校验只检查“已提供资料”，没有检查“应查资料是否实际执行”，因此本次遗漏不是单纯文案不清，而是规则与门禁没有闭环。

### 影响文件

- `AGENTS.md`
- `README.md`
- `agent/config/evidence-requirements.json`
- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/logs/bug-actions/README.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-06-evidence-profile-gate-v1.7.0-trial.1.md`

### 验证案例

- PC-38036 型通用 Bug 未执行 Drive 正式定义检索时失败；记录完整未找到/不可用轨迹并降为待定后才允许通过。
- PC-37808 型地图导航 Bug 缺主 PRD 或专项定义任一检索时失败；可见交互 Bug 缺生效配置或 UE/交互检索任一项时失败。
- Alchemy 项目功能点作为唯一产品正式目标、Alchemy 当前结果被标成 `formal_target` 时均失败。
- 批量日志缺任一 Jira 的独立决策核验卡时失败。
- `python3 agent/scripts/test_bug_evidence_gate.py`、`python3 agent/scripts/test_bug_sheet_contract.py`、`python3 agent/scripts/validate_rule_architecture.py`、`python3 agent/scripts/sync_bug_skill.py`、`jq empty agent/config/evidence-requirements.json` 与 `git diff --check`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.6.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得删除现有日志和证据；旧 `schema_version=1` manifest 仅作为历史记录保留，不能伪装成已完成 v1.7 必查动作。

## v1.6.0-trial.1 — 2026-08-06

### 试行内容

- 决策核验卡的每条资料新增必填 `source_location`；只写文档名、链接或检索关键词不能通过写表前门禁。
- PDF/PRD/交互必须写页码与章节/区域，表格必须写 Sheet 与行号/序号及 Key，UE 必须写页面/画板与图层，Jira 附件必须写附件名与时间码，Alchemy 必须写功能点名称与 `meta_id`。
- C、D/H 的依据短标签和 J 列文档标签同步显示精确证据位置，保证线上清单可以直接复查原文。

### 修改原因

- HUR-81074 第 84 行虽然引用了 J90A 功能清单、PRD 和交互文档，但没有写出证据所在 Sheet、序号和页码，无法从线上结论直接复查原文；这是执行未满足现行证据深度要求。

### 影响文件

- `agent/evidence-contract.md`
- `agent/output-contract.md`
- `agent/sheet-contract.md`
- `agent/workflows/bug.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-08-06-HUR-81074-evidence-location-correction.md`

### 验证案例

- HUR-81074：功能清单定位到 Sheet「J90A EU座舱功能清单」序号 938/939，PRD V2.4 与交互 V2.6 均定位到第 13 页，Jira 视频定位到 `00:02-00:06`。
- `test_missing_source_location_fails` 验证任一资料缺少 `source_location` 时门禁失败。
- `python3 agent/scripts/test_bug_evidence_gate.py`、`python3 agent/scripts/test_bug_sheet_contract.py`、`python3 agent/scripts/validate_rule_architecture.py` 与 `git diff --check`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.5.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得把 HUR-81074 已补充的证据位置从线上表和操作日志中删除。

## v1.5.0-trial.1 — 2026-07-30

### 试行内容

- 决策来源增加机器可校验角色：`formal_target`、`implementation_actual`、`context_only`；确定性结论必须分别引用有效目标来源和实现来源。
- `mismatch` 不再可能支撑目标行为；`partial` 正式定义只有经同项目继承声明连接并标记 `verified=true` 后才生效。
- 新增预期行为卡，覆盖触发、目标状态、意图/功能点/信号、UI/TTS/车端表现、边界和正式来源。
- `material=true` 的关键资料缺口强制把状态降为 `待复核 / 待确认 / 待会诊`；客户测试用例缺失仍固定降为 `待确认`。
- 语音门禁要求 Jira 用户原话、Alchemy 当前结果、`meta_id`、标准功能点和项目功能点；不可访问或未完成时必须记录原因和下一步，并禁止确定性语音定责。

### 修改原因

- PC-37681 首轮把 Jira 测试预期和 J90A 异车型资料当成 C385MCA 的目标定义；旧脚本只检查字段是否存在，无法拒绝这条证据链。
- 需要把“同范围正式定义优先”从人工提醒改成状态写入前的证据充分性硬门禁。

### 影响文件

- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/rules-version.md`
- `agent/logs/bug-actions/2026-07-30-evidence-sufficiency-gate-v1.5.0-trial.1.md`

### 验证案例

- PC-37681：仅有 Jira 测试预期、VOS 实现日志和 J90A `mismatch` 定义时，`可转语音` 必须失败；C385MCA 继承声明连接 C385 定义且 Alchemy 标准/项目功能点完整时才允许通过。
- PC-37681：未核验继承链、关键 UE 缺口或 Alchemy 不可用时，确定性状态失败；记录原因和下一步并降为 `待复核` 后通过。
- HUR-82492：同车型正式定义、精确实现事实和异范围补充资料的既有判断继续通过。
- ADS-47560：客户测试用例缺失时继续拒绝关闭，并只允许 `待确认`。
- `python3 agent/scripts/test_bug_evidence_gate.py`、`python3 agent/scripts/test_bug_sheet_contract.py`、`python3 agent/scripts/validate_rule_architecture.py` 与 `git diff --check`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.4.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得重新允许 Jira 测试预期、异车型资料或不完整 Alchemy 证据链单独支撑确定性结论。

## v1.4.0-trial.1 — 2026-07-29

### 试行内容

- 新增客户提报 Bug 识别：Jira 标题或描述开头带非 Jira Key 的长客户问题编号时，记录为客户提报。
- 客户提报 Bug 必查完整客户测试用例；用例缺失或不完整时，正式定义和研发日志不能单独支撑 `可关闭 / 非 Bug / 设计如此`，状态保持 `待确认`。
- 决策核验卡从五项扩为六项，新增 `客户问题识别`；机器校验要求记录客户问题编号、用例检查状态及缺失时的收集动作。
- ADS-47560 按用户复盘从 `可关闭` 更新为 `待确认`，H 写向客户收集完整测试用例后复核，保留原 D/F。

### 修改原因

- ADS-47560 虽有正式 18% 退出定义和一致的实现日志，但它是带客户问题编号的客户提报票；缺少客户实际测试用例时，无法确认 7% 预期的车型、版本、充电状态和操作前提，不能直接关票。

### 影响文件

- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/logs/bug-actions/README.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/validate_rule_architecture.py`
- `agent/bug-owners/wu-you/index.md`
- `agent/meetings/2026-07-29-ADS-47560-客户问题测试用例复盘.md`
- `agent/meetings/action-items.md`
- `agent/logs/bug-actions/2026-07-29-ADS-47560.md`
- `agent/logs/bug-actions/2026-07-29-customer-issue-test-case-gate-v1.4.0-trial.1.md`

### 验证案例

- ADS-47560：`bug!G150:H150:I150:J150` 按 `review` 更新并回读；A-F 保持不变，H/J 富文本链接目标正确。
- `test_customer_issue_without_test_case_cannot_close` 验证客户测试用例缺失时拒绝 `可关闭`。
- `test_customer_issue_missing_case_can_stay_pending` 验证缺失用例时可写 `待确认 + 收集动作 + 吴优责任方`。
- `python3 agent/scripts/test_bug_evidence_gate.py`、`python3 agent/scripts/test_bug_sheet_contract.py`、`python3 agent/scripts/validate_rule_architecture.py` 与 `git diff --check`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.3.0-trial.1 对应规则，不执行 `git reset --hard`。
- 回滚不得把 ADS-47560 的客户测试用例缺口改写成已完成核验，也不得在缺少客户用例时自动关票。

## v1.3.0-trial.1 — 2026-07-29

### 试行内容

- 在证据契约新增写表前决策核验卡：备注因果链、关联票、资料适用范围、冲突处理和唯一结论五项缺一不可。
- 明确读取 Jira 问题链接和直接关联票的门槛；共享日志或同根因只用于排查分组，不能自动推导产品目标、重复票或非问题。
- 把研发评论的实现事实/产品目标双线判断与范围冲突取舍统一收敛至 `agent/evidence-contract.md`；`jira-comment-signals.md` 仅保留检索和标注信号。
- 新增 `validate_bug_evidence_gate.py` 和对应单元测试；操作日志新增可读决策核验卡，并由架构校验确认关键字段和引用存在。

### 修改原因

- HUR-82492 首轮虽读取了 Jira 备注，但未把备注因果链、关联票和资料适用范围作为同一决策关口，错误放大了 BTPhone 创建/销毁现象及非 J90A 通用资料，未先完成同日志关联票和触发差异的闭环。
- 既有评论信号库重复维护评论权重和判断顺序，违反“证据规则只在证据契约维护”的架构边界，容易产生漂移。

### 影响文件

- `AGENTS.md`
- `README.md`
- `agent/evidence-contract.md`
- `agent/workflows/bug.md`
- `agent/product-kb/rules/jira-comment-signals.md`
- `agent/logs/bug-actions/README.md`
- `agent/logs/bug-actions/2026-07-29-HUR-82492.md`
- `agent/scripts/validate_bug_evidence_gate.py`
- `agent/scripts/test_bug_evidence_gate.py`
- `agent/scripts/validate_rule_architecture.py`

### 验证案例

- HUR-82492：HUR-82490、HUR-82491、J90A 专项定义和共通资料的范围差异均写入核验卡。
- `python3 agent/scripts/test_bug_evidence_gate.py` 覆盖关联票未读、资料范围缺失和 Jira key 漂移拦截。
- `python3 agent/scripts/validate_bug_evidence_gate.py --log agent/logs/bug-actions/2026-07-29-HUR-82492.md --key HUR-82492`、`python3 agent/scripts/test_bug_sheet_contract.py`、`python3 agent/scripts/validate_rule_architecture.py` 与 `git diff --check`。

### 回滚口径

- 通过新的 Git 提交恢复 v1.2.0-trial.3 对应规则，不执行 `git reset --hard`。
- 回滚不得再次允许未读关联票、未标资料适用范围或未处理证据冲突时写入确定性结论。

## v1.2.0-trial.3 — 2026-07-28

### 试行内容

- 修正富文本首标签从单元格第 0 位开始时的重叠运行段；J 列首标签回读不再出现重复链接目标。

### 修改原因

- Google Sheets 会将第 0 位的默认运行段与链接运行段扩展为两个相同链接，导致已有行补丁的链接校验失败。

### 影响文件

- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_sheet_contract.py`

### 验证案例

- `test_first_link_at_zero_has_one_run` 覆盖首标签位于第 0 位的多链接单元格。
- `python3 agent/scripts/test_bug_sheet_contract.py` 与 `python3 agent/scripts/validate_rule_architecture.py`。

### 回滚口径

- 通过新提交恢复旧生成逻辑；回滚前须确认不会重新引入首标签重复链接。

## v1.2.0-trial.2 — 2026-07-28

### 试行内容

- 新增 `agent/config/sheet-update-modes.json`，作为 `recheck` 与 `review` 允许列/保护列的唯一机器可读来源；活动规则与脚本改为消费模式名。
- 新增 Git 内 Skill 唯一模板和安装副本同步校验，修复 Skill 位于仓库外、无法随规则提交回滚的问题。
- 新增行先复制格式、再设置 E 列校验、最后写入值与 `textFormatRuns`，避免后续格式复制影响富文本链接。
- C、D、H、J 可见文本在生成请求前禁止显示长 URL；链接目标只接受完整 `http(s)` 原始入口。
- 新增 `validate-append`，按输入逐格核对新增 A:J，并逐项比较 C、D、H、J 的可见文本和全部链接目标。
- 已有行 `patch` 对外只接受表格可见的 1-based `row-number`，内部转换为 API `rowIndex`；manifest 同时记录两者。
- 明确预览后、batchUpdate 前必须新鲜回读完整 A:J 并与预览 fingerprint 比较；不一致即停止，写后继续回读。

### 修改原因

- 原校验只要求 J 至少存在一个链接，多来源单元格缺少部分链接仍可能通过。
- 原生成阶段允许长 URL，只有写后才能发现，可能先把错误内容写入线上表。
- 原新增顺序为“写链接后复制格式”，与稳定的原生行写入顺序相反。
- 零基行号容易与用户看到的表格行号混淆；外置 Skill 和多处列白名单也存在回滚、漂移风险。

### 影响文件

- `README.md`
- `AGENTS.md`
- `agent/output-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/config/sheet-update-modes.json`
- `agent/skills/deepal-product-bug-handler/SKILL.md`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/sync_bug_skill.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/validate_rule_architecture.py`

### 验证案例

- J 显示两个来源但只保留一个链接时，`validate-append` 必须失败。
- C、D、H 或 J 可见文本含 `http://` / `https://` 时，生成请求前必须失败。
- 新增请求前三步固定为 `copyPaste`、`setDataValidation`、`updateCells`。
- 表格第 145 行输出 `sheetRow=145` 和 `rowIndex=144`。
- Git 内 Skill 模板与安装副本逐字一致；任一副本漂移时架构校验失败。
- 单元测试、架构校验、Skill 同步校验和 `git diff --check` 均通过。

### 回滚口径

- 通过 Git 新提交恢复 `v1.2.0-trial.1`，再执行 `python3 agent/scripts/sync_bug_skill.py --install` 同步对应 Skill；不执行 `git reset --hard`。
- 回滚不得移除逐链接回读、写前长 URL 拦截或 1-based 行号保护。

## v1.2.0-trial.1 — 2026-07-28

### 试行内容

- 将普通二次复查与会议/复盘拆成两种已有行更新模式。
- 用户再次发送同一 Jira 或要求重新查看时，仍走普通 Bug 流程；重新核验后可按需更新原行 C、D、G、I、J，保留 A、B、E、F、H。
- 用户提供会议纪要、可姐/leader 教学、客户复盘或明确复盘材料时，按复盘流程更新 G、H、I、J，保留 A、B、C、D、E、F。
- 写表脚本新增已有行列级 `patch`、写前 A:J fingerprint、目标列白名单、变更 manifest 和写后保护列校验。
- 新增和已有行写入均明确提交 `textFormatRuns`，避免只写入短标签文字而丢失富文本链接。

### 修改原因

- 普通二次查看仍应修正初次处理阶段的原列，不能因为是第二次处理就把结论绕写到 H。
- 只有会议纪要、leader/客户复盘等复盘材料才形成 H 的最终判断。
- 原追加请求只声明 `userEnteredValue`，未明确提交已生成的 `textFormatRuns`，存在短标签不可点击风险。

### 影响文件

- `AGENTS.md`
- `agent/output-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/validate_rule_architecture.py`
- `/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`

### 验证案例

- 普通二次复查允许 C、D、G、I、J，拒绝 H、E、F。
- 会议/复盘允许 G、H、I、J，拒绝 C、D、E、F。
- fingerprint 不一致时停止生成请求；写后未声明列发生变化时校验失败。
- C、D、H、J 更新请求字段包含 `userEnteredValue,textFormatRuns`。
- `python3 agent/scripts/test_bug_sheet_contract.py` 与 `python3 agent/scripts/validate_rule_architecture.py` 均通过。

### 回滚口径

- 通过 Git 新提交恢复 `v1.1.0-trial.3` 的规则和脚本，不执行 `git reset --hard`。
- 回滚不得恢复整行覆盖已有 Bug，也不得移除 C/D/H/J 可点击短标签的回读要求。

## v1.1.0-trial.3 — 2026-07-28

### 试行内容

- 在 Bug 工作区初始化本地 Git 仓库，默认分支为 `main`。
- 将当前规则、索引、知识库、历史证据和操作日志建立为第一份可回滚基线。
- `.env`、`.mastergo/`、`.DS_Store`、`__pycache__/` 和 Python 字节码不纳入版本库；保留无凭据的 `.env.example`。
- 架构校验增加 Git 仓库存在性与敏感/缓存忽略规则检查。

### 修改原因

- 原有版本文件只能描述回滚口径，不能恢复具体文件状态；建立 Git 基线后可以查看差异、提交变更和按提交回退。

### 影响文件

- `.gitignore`
- `.git/`
- `agent/rules-version.md`
- `agent/scripts/validate_rule_architecture.py`
- `agent/logs/bug-actions/2026-07-28-git-baseline.md`

### 验证案例

- `git branch --show-current` 返回 `main`。
- `git status --short --ignored` 显示 `.env`、`.mastergo/` 和 `.DS_Store` 为 ignored。
- `python3 agent/scripts/validate_rule_architecture.py` 返回 `ok: true`。
- 基线提交后 `git status --short` 为空。

### 回滚口径

- 规则回滚使用明确提交，不执行 `git reset --hard`；默认通过新提交恢复所需文件。
- `.env` 和 `.mastergo/` 始终保持未跟踪，不能因回滚进入版本库。

## v1.1.0-trial.2 — 2026-07-28

### 试行内容

- 将 `http://jira.i-tetris.com/secure/Dashboard.jspa?selectPageId=17302` 登记为 Bug 清单总入口。
- 用户说“看 Bug 列表 / Bug 清单 / 待处理 Bug”且未给具体 Key 时，先从 Dashboard 17302 读取当前列表。
- 打开列表不等于授权批量处理；只读取或处理用户指定范围。
- 冯智秀、李欣、罗稚钦的清单扩充本轮暂不执行，后续按用户指令分别增加。
- 架构校验增加 Dashboard 入口与流程引用检查。

### 修改原因

- 需要为后续“去看 Bug 列表”建立唯一、稳定的 Jira 总入口，避免重新猜测过滤器或从历史链接进入。

### 影响文件

- `agent/context.md`
- `agent/workflows/bug.md`
- `agent/scripts/validate_rule_architecture.py`
- `agent/rules-version.md`

### 验证案例

- 检索 `Dashboard.jspa?selectPageId=17302`，确认只登记在固定入口和对应流程中。
- `python3 agent/scripts/validate_rule_architecture.py` 返回 `ok: true`。

### 回滚口径

- 若 Dashboard 17302 失效，只替换 `agent/context.md` 中的总入口并同步本段验证；不改负责人注册表和既有 Bug 行。

## v1.1.0-trial.1 — 2026-07-28

### 试行内容

- 新增 `agent/evidence-contract.md`，统一正式定义、实现事实、规则空白、来源优先级、专项资料、Alchemy、MasterGo 和结论门槛。
- 新增 `agent/output-contract.md`，统一 `decision_text`、`final_decision_text`、D/H、Jira、日志和聊天的可见文本与追加边界。
- `AGENTS.md` 只保留身份、默认意图、权威导航和全局权限；工作流只保留执行顺序；表格契约只保留 A:J 写入和回读。
- `context.md` 只保留稳定身份和公共入口；日期模块基线迁移到 `agent/product-kb/sources.md`。
- Skill 精简为规则加载和工具适配器，不再复制证据、输出、路由和表格业务规则。
- `agent/scripts/bug_sheet_contract.py` 停止生成多 `HYPERLINK` 拼接，改为 C/D/H/J 富文本独立链接，并明确只用于追加新行。
- 当前版本号只在本文件维护，其他权威文件统一引用。

### 修改原因

- 回复、证据、表格和 Skill 中存在重复规则，已经形成版本漂移。
- 旧写表脚本生成方式与当前 J 列富文本多链接契约冲突，也不能生成 C/D/H 的内联证据链接。
- `context.md` 混合稳定身份、可变表格配置和日期检索快照，容易把历史结果当成当前事实。

### 影响文件

- `AGENTS.md`
- `README.md`
- `agent/evidence-contract.md`
- `agent/output-contract.md`
- `agent/workflows/bug.md`
- `agent/workflows/review.md`
- `agent/sheet-contract.md`
- `agent/context.md`
- `agent/product-kb/README.md`
- `agent/product-kb/sources.md`
- `agent/product-kb/rules/source-freshness.md`
- `agent/bug-owners/wu-you/index.md`
- `agent/bug-owners/li-xin/index.md`
- `agent/bug-owners/feng-zhi-xiu/index.md`
- `agent/bug-owners/luo-zhiqin/index.md`
- `agent/logs/bug-actions/README.md`
- `agent/meetings/README.md`
- `agent/scripts/bug_sheet_contract.py`
- `agent/scripts/test_bug_sheet_contract.py`
- `agent/scripts/validate_rule_architecture.py`
- `/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`

### 验证案例

- `ADS-47367 / bug!C138:D138 / J138`：验证两个落域定义、正式 PRD、D 原文和多富文本链接契约。
- `python3 agent/scripts/test_bug_sheet_contract.py`：验证 C/D/J 独立链接、缺失标签失败和旧多 HYPERLINK 拼接拒绝。
- `python3 agent/scripts/validate_rule_architecture.py`：验证权威文件引用、兼容入口、Skill 加载、版本号唯一性和写表实现。

### 回滚口径

- 若新契约边界造成执行遗漏，回滚到 `v1.0.0-trial.3` 的工作流和表格规则内容；保留本版本日志作为变更证据。
- 写表脚本即使回滚，也不得恢复多个 `HYPERLINK` 拼接；暂时停用 build，改用经过回读的定向富文本写入。

## v1.0.0-trial.3 — 2026-07-23

### 试行内容

- D 列中的决定性依据改为可点击的短说明文字，不再显示原始长 URL。
- H 列在复盘后承担最终流转说明，因此同步遵守 D 的短文字链接规则。
- 执行 Jira 评论时保持短标签与原始链接的关联；若 Jira 编辑器未保留表格富文本链接，执行评论时重新绑定，不把长 URL 写回 Bug 表。

### 修改原因

- D/H 中铺开完整 URL 占用较多空间，影响 Bug 表阅读。

### 影响文件

- `AGENTS.md`
- `agent/workflows/bug.md`
- `agent/sheet-contract.md`
- `agent/rules-version.md`

### 验证案例

- `ADS-46239 / bug!D38`

### 回滚口径

- 若 Jira 编辑器无法稳定保留短文字链接，只在实际 Jira 评论动作中展开或重新绑定 URL；Bug 表 D/H 仍保持短文字链接展示。

## v1.0.0-trial.2 — 2026-07-23

### 试行内容

- J 列只显示能说明来源的短文字标签，标签文字本身可点击，不再显示原始长 URL。
- 多个来源在同一单元格内每行一个短标签，每个标签分别绑定对应原始入口。
- 若短标签不可点击，修复富文本链接元数据或写入方式，不再用“标签 + 完整 URL”回退。
- D/H 作为可复制到 Jira 的流转说明，仍保留决定性依据的完整 URL。

### 修改原因

- 完整 URL 在 J 列占用空间过大，影响 Bug 表扫描和阅读。

### 影响文件

- `AGENTS.md`
- `agent/workflows/bug.md`
- `agent/sheet-contract.md`
- `agent/rules-version.md`

### 验证案例

- `ADS-46239 / bug!J38`

### 回滚口径

- 若 Google Sheets 富文本多链接出现兼容性问题，优先减少 J 的来源数量或拆分短标签，不恢复显示原始长 URL；D/H 的 Jira-ready 完整 URL 规则不变。

## v1.0.0-trial.1 — 2026-07-23

### 试行内容

- D 列同时作为 Jira 流转评论原文，采用“结论 -> 决定性依据完整 URL -> 处理动作与责任方”的自包含结构。
- C 列中出现的 Jira、评论、PRD/UE、Alchemy、工作说明等证据名称原位可点击；J 只作全部入口汇总。
- 链接验收以用户实际界面可见、可点为准，不以标签颜色或仅存在 API 元数据代替。

### 验证案例

- `ADS-47039 / bug!C145:D145 / J145`

### 回滚口径

- 若 D 的 Jira-ready 结构导致表格过长或不便使用，只回滚 D 为“一条动作 + 一个责任方”的短结论；C 内联链接和 J 汇总链接规则继续保留。
