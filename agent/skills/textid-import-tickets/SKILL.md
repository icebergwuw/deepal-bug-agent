---
name: textid-import-tickets
description: Create or refresh J90A overseas HMI TextID import stories for IFS and SIC, including no-image branch files, Jira attachments, assignees, and MD5. Use when 吴优 says 下票导入, 文言导入, TextID导入, or asks to update those import tickets. Do not use for 变更表建票, ordinary Bug analysis, or HUR translation parent tickets.
---

# TextID 导入下票

Create six HUR stories from the latest no-image LanguageList, attach the branch file, and report MD5. Jira MCP cannot create or assign issues. Use the Bug project `.env` with Jira REST, then read the issues back. Do not print the password.

This is not the change-sheet story flow. Do not send that Feishu notice.

## Confirm before creating

- Search Jira for an existing story with the same version and import date. Do not create a duplicate.
- Use the branch text the user gives for this run. If they say 跟上次一样, reuse the 261030 mapping below. If they give no branches, ask. Do not invent a branch.
- The three import files are byte-identical copies. The branch exists only in the filename.

## Files

Put the copies in the version's `导入` folder. Name them:

`J90A_海外LanguageList_V{version}_{中科返回日期}_{最后编辑日期}_B{branch}_{导入日期}.xlsx`

The 261014 reference is `/Users/ice/Desktop/Project/Mega/TextID/V1.2/1015导入研发`.

Make the source by removing pictures from the latest final workbook:

- Delete `xl/media/*`, `xl/drawings/drawing*.xml`, and `xl/drawings/_rels/drawing*.xml.rels`.
- Remove worksheet `<drawing>` tags and drawing relationship entries. Keep comments and `commentsDrawing*.vml`.
- Remove drawing and image content-type overrides.
- Do not clear the screenshot column header or any cell values.
- Verify the no-image file has zero media and the same cell values.

## Tickets

Copy the field shape of HUR-85980 through HUR-85985:

- Project `HUR`, story id `10001`, priority id `2`
- Component `Android - General` id `14331`
- Fix version `无发版计划` id `13341`
- Epic `HUR-2`
- Vehicle Model: `0904` and `0507` are J90A/EU (`11726` / `11728`). `0109` is J90A/EU PI (`11726` / `13315`).

Titles:

- SIC: `[HMI文言导入]{branch}分支导入TextID{version}_{导入日期}-SIC`
- IFS: `[HMI文言导入]{branch}分支导入TextID_{导入日期}`

Assignees, unless the user names someone else for this run:

- SIC: 祝成雄 `chengxiong.zhu`
- IFS: 袁威 `wei.yuan`

Do not restore the older 85980 assignees 吴厚东, 熊佳欣, or 梁先伟. 吴优 changed this on 2026-10-30.

Description:

- The `0904` tickets list every 主线 the user supplied.
- The `0109` ticket lists only the CC delivery branch.
- The `0507` ticket lists only the OTA4 delivery branch.
- Include `文档名称`.
- End with `详细变更点见《变更履历-MJ》、《变更履历-TS》`. The sheet is `变更履历-TS`, not TJ.
- Do not copy one-off notes from old tickets, such as 新增 `20_OFF`, unless the user says that note still applies.

Attach the matching branch file. If the workbook changes after the tickets exist, patch the final file, the no-image file, and all three import copies, then upload the new attachment and delete the old attachment with the same filename. Read back summary, assignee, vehicle, attachment name, and size.

Report the MD5 of the final workbook and the MD5 of the no-image import file. The three branch files must share one MD5.

## 261030 branch mapping

Use this only when the user says to follow the last import:

- J90A-EU 主线 `sop/huron_hqx.1.2.1_20240904`；OTA4 `release/huron_hqx.1.2.1_20250507`
- J90A-EU PI 主线 `sop/huron_hqx.1.2.1_20240904`；CC `release/huron_hqx.1.2.1_20260109`
- J90A-EU 27CY、J90A-ER27CY、J90A-EL27CY、ER、EL 主线都是 `sop/huron_hqx.1.2.1_20240904`
