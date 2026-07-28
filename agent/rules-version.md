# Bug 处理规则版本

- 当前版本：`v1.2.0-trial.2`
- 状态：`trial`
- 生效日期：`2026-07-28`
- 适用范围：`.gitignore`、`AGENTS.md`、`agent/evidence-contract.md`、`agent/output-contract.md`、`agent/workflows/bug.md`、`agent/workflows/review.md`、`agent/sheet-contract.md`、`agent/config/sheet-update-modes.json`、`agent/context.md`、`agent/bug-owners/registry.yaml`、`agent/skills/deepal-product-bug-handler/SKILL.md`、`agent/scripts/bug_sheet_contract.py`、`agent/scripts/sync_bug_skill.py`、`agent/scripts/test_bug_sheet_contract.py`、`agent/scripts/validate_rule_architecture.py`
- Skill 唯一模板：`agent/skills/deepal-product-bug-handler/SKILL.md`；安装位置为 `/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`，安装副本不定义独立业务口径且必须与模板一致。
- 说明：当前目录从 `v1.1.0-trial.3` 起使用本地 Git `main` 分支管理；本文件继续记录业务规则版本、试行状态、验证案例和回滚口径。更早版本没有 Git 提交，不追溯伪造。

## 版本规则

- `MAJOR`：列职责、默认授权边界或完整流程发生不兼容变化。
- `MINOR`：新增证据门槛、写表契约或核验步骤。
- `PATCH`：不改变职责边界的文字澄清和缺陷修正。
- `trial.N`：试行次数；用户确认转正后移除 trial 标记。
- 每次修改必须记录日期、原因、影响文件、验证案例和回滚口径，并在 `agent/logs/bug-actions/` 留痕。

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
