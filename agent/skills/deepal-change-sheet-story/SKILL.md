---
name: deepal-change-sheet-story
description: Create Deepal change-management-sheet requirement stories, assign the sheet owner, write the Jira key back, and notify the recorded Feishu group with missing PRD/UE and named contacts. Use when a new session says 建票, asks to create tickets, process recent owner rows such as 吴优、李欣、冯智秀 or 罗稚钦, or send the post-create Feishu notice. Do not use for a standalone Jira Bug link, ordinary Bug analysis, HUR translation parent tickets, Jira comments, or read-only review.
---

# Deepal Change Sheet Story

A new session that says 建票 uses this workflow. Do not invent another ticket-creation path. A standalone Jira Bug link still uses `deepal-product-bug-handler`. If this skill conflicts with `AGENTS.md` or `agent/workflows/review.md`, those files win.

## Boundaries

- Read the operator from `agent/config/local-profile.json`. Do not guess identity from the computer name or chat.
- Jira MCP cannot create or transition issues. Create and assign through Jira REST with the local `.env` credentials, then read the new issue back with `get_jira_issue`.
- Do not print or commit the Jira password or Feishu App Secret. The secret stays in gitignored `agent/config/feishu-bot.local.json`.
- Do not fill PJM columns, write a frozen sheet tab, reassign unrelated existing issues, close issues, or write Alchemy.
- HUR translation bugs use `agent/product-kb/rules/hur-translation-parent.md`. Do not create a change-sheet story or send this Feishu notice for them.
- A user saying "只看" means read only.

## Select Rows

- Open the workbook in `agent/context.md` with the operator's signed-in Chrome. Choose the sheet tab from the source project. Do not always write `gid=1443256155`; that gid is only `深蓝8295平台（国内）OTA 项目`.
- Header is row 3. Product may fill `功能模块` and `JIRA-Story`. For an existing row, write only column D after the new key is read back.
- Keep only rows whose column B, `变更提出时间`, falls in the calendar month ending today. A date without a year uses the workbook year; if that date is later than today, subtract one year. Skip a row when the date cannot be parsed, column D already has a Jira key, or the row is completed, abandoned, cancelled, duplicated, waiting for a quote, or an internal bug.
- When the user asks for each owner's latest ticket, take that owner's last in-window row. If that row is ineligible, do not walk backward and create an older row.
- Resolve the assignee from column U and `agent/bug-owners/registry.yaml`: 吴优 `you.wu`, 李欣 `xin.li03`, 冯智秀 `zhixiu.feng`. A shared cell such as `冯智秀/陈羸` uses the named registered product owner. If U does not match a registered owner, use the current operator. If the registered owner has no Jira account, stop and say so. Set the assignee at creation. Do not leave it to the component default.
- For `深蓝8295平台（国内）OTA 项目`, Epic Link is `ADS-7` (`ECR_待签署`). Do not reuse that Epic on another tab unless `agent/context.md` records it. Do not invent a fix version or copy a Dongfeng example. If the selected tab has no recorded fix version, stop before creating the issue.

## Create And Read Back

- Search Jira for an existing story covering the same module and change before creating one.
- Title with the module and the change. Description uses this shape:

```text
【需求背景】
客户输入
【需求详情】
<column E text>

PRD：<latest formal PRD for this module, or state that none was found>
UE：<latest formal UE for this module, or state that none was found>
```

- Search the signed-in Drive for the current module's latest PRD and UE. Record the search limit instead of guessing a document.
- Read back the key, summary, assignee, Epic, and description. Only then write the key into column D. Jump with the name box, confirm the target cell, edit the formula bar, and do not click the grid while editing. Read back D and the neighboring E/U cells.
- Log the action under `agent/logs/bug-actions/` without secrets. After the rule and log checks pass, commit and push the project changes. Do not claim a push succeeded if it failed.

## Feishu Notice

- After readback, send one group message per created issue with `agent/scripts/notify_feishu_ticket.py`.
- The app ID and group ID live in `agent/config/feishu-notify.json`. Do not hard-code a secret.
- Include the key, summary, link, assignee, change-sheet serial, and dependencies. Dependencies name missing PRD/UE, cross-module dependencies, and contacts already written on the row. If the sheet does not name a contact, write `待指定`. Do not invent a person.
- 李欣 is 塞林格 and 冯智秀 is 芝芝 in the group. These names are recognition only. Do not claim an @ mention unless the bot returns a real mention. A missing member-read scope means the message is a notice, not an @.
- If sending fails, say it failed and include the error. Do not say the group was notified.
