# Bug 处理规则版本

- 当前版本：`v1.1.0-trial.3`
- 状态：`trial`
- 生效日期：`2026-07-28`
- 适用范围：`.gitignore`、`AGENTS.md`、`agent/evidence-contract.md`、`agent/output-contract.md`、`agent/workflows/bug.md`、`agent/workflows/review.md`、`agent/sheet-contract.md`、`agent/context.md`、`agent/bug-owners/registry.yaml`、`agent/scripts/bug_sheet_contract.py`、`agent/scripts/validate_rule_architecture.py`
- Skill 消费端：`/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md`，只加载本项目规则，不定义独立业务口径。
- 说明：当前目录从 `v1.1.0-trial.3` 起使用本地 Git `main` 分支管理；本文件继续记录业务规则版本、试行状态、验证案例和回滚口径。更早版本没有 Git 提交，不追溯伪造。

## 版本规则

- `MAJOR`：列职责、默认授权边界或完整流程发生不兼容变化。
- `MINOR`：新增证据门槛、写表契约或核验步骤。
- `PATCH`：不改变职责边界的文字澄清和缺陷修正。
- `trial.N`：试行次数；用户确认转正后移除 trial 标记。
- 每次修改必须记录日期、原因、影响文件、验证案例和回滚口径，并在 `agent/logs/bug-actions/` 留痕。

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
