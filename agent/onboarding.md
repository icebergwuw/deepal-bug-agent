# 团队首次运行与权限引导

本文件只定义项目在新电脑上的身份与运行环境准备。Bug业务规则继续以 `AGENTS.md`、`agent/workflows/` 和各契约文件为准，不在这里复制。

## 安全边界

- 本仓库包含公司内部 Bug 信息、线上表格入口和资料线索，只能使用访问受控的私有仓库。
- Git 不保存密码、Token、Cookie、测试账号、连接器授权或浏览器会话。
- 用户把密钥粘贴到聊天、终端或文件后，应立即撤销并通过平台安全登录重新授权；Agent不得复用、回显或代存该密钥。
- 本机身份配置固定为 `agent/config/local-profile.json`，已由 `.gitignore` 排除。
- 如本机使用 `.env` 保存运行凭据，必须保持Git忽略并使用仅当前用户可读的权限（macOS/Linux为 `chmod 600 .env`）。

## 同事独立使用

本节给不在本项目、也不使用现有 Bug 表的同事。已登记负责人不要走本节，继续用下一节绑定自己的身份。

开始处理任何 Bug 之前，先问清三件事。没问清之前只提问，不查整批，不写表。

1. 使用人是谁。必须由对方在对话里自己说出姓名。不得根据电脑用户名、Git 作者、浏览器账号或聊天称呼猜测。对方没说出姓名之前，禁止运行 `--init-external`。
2. 在哪里更新。请对方给出自己的 Google 表格链接或本地 Excel 路径。没有现成表格时，新建本地 Excel，不写入已登记负责人的线上清单。
3. Bug 列表。请对方发 Jira 链接或 Key。一批最多 5 条。超过 5 条先停下，请对方拆成小批量，不自动全部处理。

当前是测试版本，判断可能不准。开始和结束都要请对方反馈哪里不对。

姓名和写入位置都确认后，才把本机身份写成同事模式。这个身份只留在已忽略的 `local-profile.json`，不写入 `registry.yaml`，也不能因此获得别人的表。

```sh
python3 agent/scripts/bug_project_preflight.py \
  --init-external \
  --operator-name "<对方刚刚说出的姓名>" \
  --identity-source explicit_user_confirmation \
  --result-type excel
```

对方已经有自己的 Google 表格时，把 `--result-type excel` 换成 `--result-type google_sheet --result-location "<对方自己的表格链接>"`。链接如果指向本仓库已登记的团队 Bug 表，命令会拒绝。

新建本地 Excel 默认放在 `agent/external-results/`。同事处理日志放在 `agent/logs/bug-actions/external/`。这两处都不进入 Git。列仍然使用 `agent/sheet-contract.md` 的 A:J。

本机如果已经绑定了团队负责人，不要改成同事模式，除非当前使用人明确说自己是另一个人，并确认使用 `--replace-profile`。

## 第一次打开项目

已登记负责人使用本节。同事独立使用不要从注册表里挑选别人的身份。


1. 列出注册表中可绑定的负责人：

   ```sh
   python3 agent/scripts/bug_project_preflight.py --list-owners
   ```

2. 由使用者本人明确选择身份。默认只允许写自己的负责人清单：

   ```sh
   python3 agent/scripts/bug_project_preflight.py --init-owner <owner-id>
   ```

   不得根据 macOS 用户名、Git作者、Google账号或浏览器账号自动猜身份。需要更换身份时，必须由使用者明确执行 `--replace-profile`。

3. 安装或同步 Git 内唯一 Bug Skill：

   ```sh
   python3 agent/scripts/sync_bug_skill.py --install
   ```

   安装位置自动使用 `$CODEX_HOME/skills`；未设置时使用当前用户目录下的 `.codex/skills`，不依赖任何人的绝对路径。

4. 执行本机检查：

   ```sh
   python3 agent/scripts/bug_project_preflight.py
   ```

   输出 `mode=read_only` 时，按 `guidance` 逐项完成，不得先写线上清单。

## 平台登录与真实读取验证

权限不随 Git 迁移。每名成员使用自己的公司账号完成以下登录，并由 Agent真实读取对应内容后才能记录通过：

外部平台的真实读取和写回默认优先使用操作者当前 Chrome 的已登录态。Chrome 会话可用时，不得因为内置连接器更方便而绕过该会话；仅在 Chrome 不可用、未登录或无法完成所需操作时，才使用内置浏览器、连接器或其他受支持入口。

| 平台 | 验证动作 | 失败时引导 |
| --- | --- | --- |
| Jira | 打开本人有权访问的 Bug，读取标题和评论时间线 | 在受支持浏览器中登录 Jira；仍无权时联系 Jira 管理员 |
| Google Drive/Sheets | 读取本人负责人页的 A:J 样例和表格元数据 | 连接 Google Drive并确认该工作表已共享给本人 |
| Alchemy | 读取标准功能点或完成一次在线原话测试 | 登录 Alchemy；语音 Bug 在未验证前按证据门禁降级 |
| MasterGo | 打开对应项目/页面/图层 | 登录并申请项目权限；可见交互证据缺失时不得硬判 |

真实读取成功后，由 Agent记录不含凭据的短期访问回执：

```sh
python3 agent/scripts/bug_project_preflight.py --mark-access jira --mark-access google_drive
```

语音或可见交互任务再分别增加 `alchemy`、`mastergo`。回执默认24小时过期；即使回执仍有效，每次线上写入也必须按原流程回读结果。

## 写入其他负责人范围

本机默认只允许写绑定操作者自己的清单。确需代处理其他成员时，由操作者明确增加范围：

```sh
python3 agent/scripts/bug_project_preflight.py --allow-owner <owner-id>
```

协调人需要覆盖全部当前 `active + read_write` 负责人时，可明确执行 `--allow-all-active`。该设置只是本机防误写边界，不代替 Jira、Drive或组织权限。

每次写表前按实际 Jira 当前负责人执行：

```sh
python3 agent/scripts/bug_project_preflight.py \
  --require-owner <current-owner-id> \
  --require-platform jira \
  --require-platform google_drive
```

语音任务追加 `--require-platform alchemy`；需要 MasterGo目标图层的任务追加 `--require-platform mastergo`。检查失败时只能只读分析并提供具体登录/授权步骤。

## 定时任务和GitHub

- Codex定时任务属于每台电脑的本机配置，不随Git同步。成员确认身份和权限后再单独创建。
- 推送前检查敏感信息、确认远端为私有仓库，并使用系统凭据管理或平台安全登录；不要在聊天或命令中粘贴Token。
- 本项目完成并验证规则、脚本、索引、操作日志、知识库或会议沉淀更新后，默认提交并推送当前分支；无文件变化时不创建空提交。远端不可达、权限不足或私有性无法确认时停止推送并明确报告。
- 克隆路径可以不同；项目脚本必须从仓库位置和当前用户目录动态解析路径。
