---
name: translation-key-excel-organizer
description: Read Jira translation parent issues and all relates-to tickets, follow comment timelines for final string keys, and create or update a standardized Excel workbook. Use when the user asks to整理翻译票、提取语种/Key/文言 or update the translation-key Excel list.
---

# Translation Key Excel Organizer

## Workflow

1. Read the repository Bug rules and run `agent/scripts/bug_project_preflight.py`. Keep this task read-only unless the user explicitly requests Jira or online-sheet writes.
2. Before every run, present the latest TextID workbook, then ask the operator which workbook is current for this run. Do not look up keys until they confirm. Do not silently reuse an old path. The confirmed workbook is the authority for `模块(表单)` and `中文`.
   - Default latest workbook to present: `/Users/ice/Desktop/Project/Mega/TextID/V1.2.1/J90A_海外LanguageList_V1.2.1_261030.xlsx`. Still ask the operator to confirm it is current before lookup. If they confirm another workbook, use that instead.
   - Chrome blocks direct `gviz` and `/export` downloads (`ERR_BLOCKED_BY_CLIENT`). Do not treat a failed download as an empty workbook. Read the open sheet, or use another workbook only after the operator confirms it.
3. Open the supplied Jira parent in the signed-in browser. Extract every `relates to` and `blocks` key, expand “more links,” de-duplicate keys, and record the total.
   - Before adding a ticket, read its fix version and title. Domestic wording does not enter this workbook or the 长马 translation parent. A fix version containing `国内` is domestic, including `J90A国内26年OTA版本发布`. A title containing `【0408】`, `[0408]`, or `0408分支` is 0408 and is also excluded. Do not treat every ticket on fix version `J90A-ER_VAVE_20261110` as 0408. Do not link, close, or list excluded tickets here. Project `HUR` or the word 文言 in the title is not enough to treat it as overseas.
4. Open each related issue and read the full comment timeline in chronological order. Select the last comment containing `<string name="KEY">VALUE</string>`. If absent, use only an explicitly stated key or source from the title/comments and mark missing fields as `未提供`.
5. Look up each extracted key with the workbook's Find dialog, only in sheets `01` through `21`. Never read the key, Chinese source, module, or translation from `All Key` or from any history/record sheet.
   - Open `编辑` → `查找和替换`. Search `所有工作表`, enable `匹配整个单元格内容`, and do not use `替换` or `全部替换`.
   - Start from `21_huronMars` cell `A1` so numbered sheets are searched before `All Key`. If the hit sheet is not `01_`–`21_`, click `查找` again until it is. If no numbered sheet matches, mark the key `未提供`.
   - `模块(表单)` is the sheet name, such as `01_3D Control` or `19_Toast`. Copy `文本` / `Words` on that row verbatim as `中文`. Read the requested language from that same row.
   - If Jira explicitly states a Chinese source itself is the missing key (for example `key 就是“辅助驾驶系统过热，降温后恢复”`), use that exact source in `KEY` and `中文`, and record that it is a source-key rather than inventing an identifier.
   - Treat Jira language signals explicitly: `EL` means 阿拉伯语; `英语` or `英文模式` as a language/mode label means 英语; `阿拉伯` means 阿拉伯语. Do not treat result text such as “显示英文/英文 toast” as the test language. When an `EL` title also names English mode, record both `阿拉伯语、英语` rather than leaving the language unknown.
6. Query the system date at the start of each run. Set every row's `时间` to that run date (`YYYY/M/D`) and every row's `提出人` to `吴优`; do not use Jira reporter/comment author for these two output fields.
7. Build rows only for the sentence named in the ticket title. Columns are exactly: `时间`, `提出人`, `模块(表单)`, `KEY`, `中文`, `文言状态`, `备注`, `涉及语种`, `对应语种当前文言`, `票号`, `是否更新`.
   - If comments, the same screen, or analysis mention other keys, those are clutter. Do not add them. Do not keep a `不用改` row to say they should not be changed.
   - Keep more than one row only when the title itself names more than one sentence, such as 疲劳和分神, 按键1和2, 界面和即将进入页面, or two places that must match. Like `HUR-86678` and `HUR-86679`, the title sentence is the only row.
8. Look up `对应语种当前文言` from the confirmed TextID workbook using KEY and the language column; for multiple languages, label each value with its language. Put the Jira key (`HUR-XXXXX`) in `票号`. Put the requested action in `文言状态` (for example `缩减翻译`, `确认翻译`, `补充翻译`, `删除多余换行`, `先确认`, `未提供`).
   - `备注` must answer what 中科 should do, in plain Chinese a translator can act on. Lead with the Chinese sentence, then the language, the current wording, and the action: shorten so it fits, use the table wording, add a missing word, fix a line break, or fix punctuation. Put the Key after the Chinese sentence, not first.
   - Never write `本行`, `同票带出`, `请中科不要改本行`, `同票另一句不用改`, or `未确认前不要改`.
   - Do not leave `备注` as only link type, ticket status, or lookup source. If the Key is missing or absent from sheets `01`–`21`, write that 中科 must match the screenshot to the Chinese sentence first and must not guess a translation.
9. Never infer a missing key, language, or translation from a similar issue. Keep Jira hyperlinks in the workbook, freeze the header row, enable filters, wrap text, and verify row counts and hyperlinks after saving. Configure `是否更新` as a BOOLEAN/list validation field with default `FALSE` so the operator can manually check it.

## Output Contract

- Preserve all previously collected sheets when updating a workbook; append or replace only the requested parent sheet.
- Keep one row per title-named sentence. A ticket with no identifiable title sentence still gets one incomplete row.
- Date values are always the queried run date in `YYYY/M/D`; relative Jira dates may remain in `备注` as evidence context.
- Do not write passwords, tokens, cookies, or private credentials to the workbook or skill.
