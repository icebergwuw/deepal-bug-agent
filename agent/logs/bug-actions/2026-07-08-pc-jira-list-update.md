# 2026-07-08 PC Jira List Update

## Source

- User provided Jira list URL starting at `PC-37264`.
- JQL shown in URL: `project = PC AND issuetype = Bug AND status in ("To Do", Reopened, "In Progress", Pending) AND assignee in (membersOf(product-ca)) AND assignee = you.wu`.

## Issues Read

- `PC-37264`
- `PC-37249`
- `PC-37242`
- `PC-37220`
- `PC-37186`
- `PC-37181`
- `PC-37175`
- `PC-37167`
- `PC-37092`
- `PC-36290`
- `PC-35462`

## Evidence Checks

- Read Jira details and comments through Chrome logged-in session.
- Checked `bug` sheet and `agent/bug-index.md` before writing.
- Checked local KB and meeting review notes:
  - `agent/product-kb/modules/voice-vui.md`
  - `agent/product-kb/rules/bug-to-requirement.md`
  - `agent/product-kb/org/component-owner-map.md`
  - `agent/meetings/2026-07-06-leader-review.md`
- Checked `深蓝8155` background sheet rows for module entry points:
  - 地图
  - 蓝牙电话
  - 场景积木
  - 语音形象&GUI
- Ran Alchemy online conversation checks:
  - `打开地图偏好设置页面` -> `meta_id=1305`, `type=app:ctrl`
  - `打开高德地图` -> `meta_id=1305`, `type=app:ctrl`, `target=gaode`
  - `我要变更目的地` / `嘉麟融府` -> `meta_id=1209`, `type=navi:dest:search`
  - `取消` -> `meta_id=1435`, `type=common:ctrl`
  - `选择华为ADS` -> `meta_id=1919`, `type=common:func:not:supported`
- Checked Alchemy standard function details:
  - `1305` / standard point `1423`: 打开特定页面/APP
  - `1209` / standard point `1433`: 导航去【地址】
  - `1020` / standard point `1448`: 地图放大/缩小
  - `1435` / standard point `1421`: 退出/取消/关闭
  - `1919` / standard point `1442`: 车型无此功能兜底

## Sheet Writes

- Updated Google Sheet `bug`, spreadsheet `1niNVFbugK2443IFe06H8nvZRC-e_r2b83YRBqXKGkqs`.
- Added rows:
  - Row 29: `PC-37264`
  - Row 30: `PC-37249`
  - Row 31: `PC-37220`
  - Row 32: `PC-37186`
  - Row 33: `PC-37181`
  - Row 34: `PC-37175`
- Updated existing notes:
  - Row 4 `PC-37242`: added linked demand tracking note for `PC-37447`.
  - Row 12 `PC-36290`: added `PC-37186` same-class会诊 note.
  - Row 14 `PC-35462`: added note that 熊东森 asked for the demand ticket link.
- Follow-up update after user asked why only 6 rows were added:
  - Row 4 `PC-37242`: refreshed collected info, action, and note.
  - Row 7 `PC-37167`: refreshed collected info, action, and note.
  - Row 9 `PC-37092`: refreshed collected info, action, and note.
  - Row 12 `PC-36290`: refreshed collected info, action, and note.
  - Row 14 `PC-35462`: refreshed collected info, action, and note.
- Re-read `bug!A29:J34` after writing; row/column alignment verified.
- Re-read `bug!B4:H14` after follow-up update; row/column alignment verified.

## Local Writes

- Updated `agent/bug-index.md` with rows 29-34.

## Jira Actions

- No Jira comments were posted.
- No Jira transitions or assignee changes were made.
