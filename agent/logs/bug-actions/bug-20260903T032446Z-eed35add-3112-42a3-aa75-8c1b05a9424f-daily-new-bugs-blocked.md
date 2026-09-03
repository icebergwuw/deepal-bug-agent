# Daily new Bug run blocked

- run_id: `bug-20260903T032446Z-eed35add-3112-42a3-aa75-8c1b05a9424f`
- operator/owner: `wu-you` / 吴优
- JQL: `assignee = you.wu AND project in (SD,HUR,ADS,BGS,BEO,PC,SM,SLV) AND issuetype = Bug AND status in (To Do,Reopened,In Progress,Pending)`
- Jira result count: 24
- Wu You online bug sheet: 447 unique keys; duplicate keys exist in historical rows; current query has 5 unregistered keys.
- New keys: `HUR-80638` (row 409 planned), `ADS-47883` (row 410 planned), `ADS-47882` (row 411 planned), `ADS-47078` (row 412 planned), `ADS-44267` (row 413 planned).
- Jira full-page reads completed for all five, including current fields, description, attachments metadata, visible comments and linked issue references.
- Evidence blockers: Google Drive connector-origin receipts unavailable/expired; Alchemy current/standard/project receipts unavailable/expired for voice tickets; MasterGo current layer receipts unavailable/expired for ADS-44267.
- Decision gate: blocked/downgraded; no sheet build or patch request generated. No online sheet, local index, Jira, Alchemy or MasterGo writes performed.
- Customer case: ADS-44267 contains customer issue `ID20260602134722264`; its layer arbitration target remains unresolved. Other four are internal test tickets.
- 回读校验: not applicable because no write occurred. This run must not be reported as completed until required platform receipts and schema-v5 manifests pass.

## Access clarification

- 2026-09-03 11:26 +08:00: direct authenticated Chrome verification succeeded for Alchemy (`运营平台`, user `you.wu`) and MasterGo (`主页 - MasterGo`, 吴优 workspace). Google Sheets was also directly readable. The earlier blocker referred to expired local short-term receipts and unavailable connector-origin Drive receipts, not an expired Chrome login session.
- Preflight access receipts were refreshed for `google_drive`, `alchemy` and `mastergo`; no external write was performed.
