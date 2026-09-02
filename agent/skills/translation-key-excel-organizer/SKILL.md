---
name: translation-key-excel-organizer
description: Read Jira translation parent issues and all relates-to tickets, follow comment timelines for final string keys, and create or update a standardized Excel workbook. Use when the user asks to整理翻译票、提取语种/Key/文言 or update the translation-key Excel list.
---

# Translation Key Excel Organizer

## Workflow

1. Read the repository Bug rules and run `agent/scripts/bug_project_preflight.py`. Keep this task read-only unless the user explicitly requests Jira or online-sheet writes.
2. Before every run, ask the operator to confirm which TextID workbook is the latest. Do not silently reuse an old path. The confirmed workbook is the authority for `模块(表单)` and `中文`.
3. Open the supplied Jira parent in the signed-in browser. Extract every `relates to` key, expand “more links,” de-duplicate keys, and record the total.
4. Open each related issue and read the full comment timeline in chronological order. Select the last comment containing `<string name="KEY">VALUE</string>`. If absent, use only an explicitly stated key or source from the title/comments and mark missing fields as `未提供`.
5. Look up each extracted key in the confirmed TextID workbook (prefer `All Key`, then the exact module sheet). Copy its module and Chinese source verbatim. If a key is absent or conflicting, keep the Jira evidence and mark the gap in `备注`.
6. Build one row per Jira issue with exactly these columns: `时间`, `提出人`, `模块(表单)`, `KEY`, `中文`, `文言状态`, `备注`, `涉及语种`.
7. Use the translation evidence comment date and author for time/proposer. Put the requested action in `文言状态` (for example `缩减翻译`, `确认翻译`, `补充翻译`, `删除多余换行`, `未提供`). Preserve uncertainty in `备注`.
8. Never infer a missing key, language, or translation from a similar issue. Keep Jira hyperlinks in the workbook, freeze the header row, enable filters, wrap text, and verify row counts and hyperlinks after saving.

## Output Contract

- Preserve all previously collected sheets when updating a workbook; append or replace only the requested parent sheet.
- Keep one row per related Jira ticket, including tickets with incomplete evidence.
- Date values should use `YYYY/M/D` when a precise date is known; relative dates such as “昨天” remain in `备注` if they cannot be resolved.
- Do not write passwords, tokens, cookies, or private credentials to the workbook or skill.
