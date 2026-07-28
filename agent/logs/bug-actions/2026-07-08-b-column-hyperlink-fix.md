# 2026-07-08 B Column Hyperlink Fix

## Trigger

- User reported that links in column B could not be opened.

## Cause

- Existing B-column values were plain text like `PC-37264｜摘要`, not Google Sheets hyperlink formulas.

## Sheet Update

- Spreadsheet: `1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs`
- Sheet: `bug`
- Range updated: `B2:B34`
- Change: converted each plain Jira key + summary into clickable formula:
  - `=HYPERLINK("http://jira.i-tetris.com/browse/<JiraKey>","<JiraKey>｜<摘要>")`

## Verification

- Re-read `bug!B2:B34` with `FORMULA`; all rows returned `HYPERLINK` formulas.

## Rule Updates

- Updated `AGENTS.md`.
- Updated `agent/sheet-template.md`.
- Updated `agent/workflow.md`.

## Jira Actions

- No Jira comments were posted.
- No Jira transitions or assignee changes were made.
