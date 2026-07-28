# 2026-07-22 Bug 工作区证据治理

## 范围

- 触发：用户要求审核并整理 `/Users/you.wu/Desktop/Mega Project/Bug` 全目录，重点校正新 session 的 Bug 处理深度和结构混乱。
- 关联 Jira：`ADS-47165`。本次只复核其线上表格行和既有日志，不改 Jira 评论、经办人或状态。
- 外部写入：仅将 `bug!A140:J140` 的行高从固定值恢复为“适合数据”自动行高；未改任何单元格内容。
- 安全边界：未读取 `.env`，未记录账号、密码、token 或测试口令。

## 发现的问题

1. “必须有依据”已体现在单次 ADS-47165 处理和记忆说明里，但没有完整进入项目权威规则，新 session 仍可能只看 Jira 标题、历史判断或研发的“当前逻辑”。
2. `agent/workflows/bug.md` 与 `agent/sheet-contract.md` 对关键证据应写 C、J 还是日志存在冲突。
3. 产品知识库 README 的检索顺序可能让历史案例先于生效正式资料，容易把旧案例当当前依据。
4. J 列已支持多个富文本链接，但 `agent/scripts/bug_sheet_contract.py` 只接受 `HYPERLINK` 公式，会误报合规行。
5. 负责人简介重复登记账号、清单和状态等易变信息；三名负责人缺少 `sheet_gid`，路由配置不完整。
6. ADS-47165 第 140 行被固定为 140 px，与统一“适合数据”行高契约冲突。
7. 13 个历史案例均未补齐现行案例模板元数据；不能伪造补写，必须明确降级为 `historical / 未重新核验`。

## 已完成治理

- 在 `AGENTS.md`、根 `README.md`、`agent/workflows/bug.md` 和 `agent/workflows/review.md` 统一证据门槛：完整 Jira + 生效主 PRD + 直接相关专项 PRD/交互/UE/工作说明；语音问题还要核对 Alchemy 标准点与项目继承点。
- 明确区分“正式产品定义、当前实现行为、规则缺口”；“当前逻辑、可见优先、设计如此、历史如此”只能作为线索，不能自动证明非 Bug。
- 明确关闭或非 Bug 结论必须有正式定义或客户最终结论；否则写清规则缺口、补充定义、动作和责任方。
- 将决定性依据和规则缺口统一写入 C，来源链接统一写入 J，详细链路写操作日志；H 只保留复盘后的最终产品动作。
- 在 `agent/context.md`、`agent/product-kb/README.md`、`agent/product-kb/index.md` 明确知识库只负责定位线索，历史案例不能覆盖当前 Jira 和生效正式资料。
- 在 `agent/bug-owners/registry.yaml` 补齐吴优、李欣、冯智秀、罗稚钦四个线上页 `sheet_gid`；四份负责人 README 和模板不再复制易变配置，统一以注册表为准。
- 更新 `agent/scripts/bug_sheet_contract.py`，J 列同时接受公式链接和富文本多链接。
- 更新 `agent/sheet-contract.md`：C 不再设可能挤掉依据的固定字数上限；J 支撑 C/D/H；行高必须自动适配，禁止为省事固定高度。
- 更新 `.gitignore`，忽略 `.DS_Store`、`__pycache__/` 和 `*.pyc`；历史文件和历史日志未批量删除或改写。

## 校验与回读

- 本地 Markdown 权威区引用扫描：真实缺失路径 0；`agent/bug-owners/<owner>/index.md` 仅为模板占位，不计缺失。
- 负责人注册表：4 名 `active + read_write` 负责人均有 `sheet_gid`。
- 本地负责人索引：冯智秀 61 条、李欣 129 条、罗稚钦 134 条、吴优 140 条；各自页内重复 key 均为 0。
- 产品知识库：13 个历史案例文件与 `agent/product-kb/index.md` 一一对应，无漏项、无陈旧索引；13 个旧案例均缺模板元数据，现已在索引和 README 明确按历史线索处理，未伪造核验状态。
- 脚本语法：`python3 -m py_compile agent/scripts/bug_sheet_contract.py` 通过。
- 脚本回读样例：J 列 `HYPERLINK` 公式通过；富文本多链接通过；无链接普通文本被正确拒绝。
- 线上表格回读：`bug!A140:J140` 内容未变；B 仍为 ADS-47165 Jira 超链接公式；E 仍为 FALSE BOOLEAN 复选框；J 仍有 PRD、Jira、Alchemy 标准点和项目点四个链接；基础筛选覆盖 `A1:J141`。
- 线上视觉校验：行 140 恢复“适合数据”自动行高后，Google Sheets 页面显示 C/D/H 已按内容展开，未被压成单行。
- 本地索引回读：`agent/bug-owners/wu-you/index.md` 仍为 `ADS-47165 | 140 | 替换途经点时序号选错列表 | 可转语音`。
- 本日志写入后再次回读；本目录不是 Git 仓库，因此没有可提供的 Git diff/status。

## 最终结构口径

- 身份和默认路由：`AGENTS.md`。
- 单条 Bug 执行：`agent/workflows/bug.md`。
- 复盘/leader 反馈：`agent/workflows/review.md`。
- 线上 A:J 写法和格式：`agent/sheet-contract.md`。
- 固定资料入口：`agent/context.md`。
- 负责人可变配置：`agent/bug-owners/registry.yaml`。
- 产品知识与历史线索：`agent/product-kb/`，但不得代替当前正式证据。
- 每次动作留痕：`agent/logs/bug-actions/`。
