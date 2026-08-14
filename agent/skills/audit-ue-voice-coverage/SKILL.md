---
name: audit-ue-voice-coverage
description: Audit vehicle UE controls against live Alchemy voice execution and update a voice-coverage Google Sheet. Use when a user asks to inspect assigned modules, read MasterGo or Drive UE documents, test whether switches, sliders, selectors, buttons, or mode controls can be completed by voice, identify missing or incorrect voice capabilities, or maintain a 车型语音功能覆盖走查/新增能力申报表.
---

# Audit UE Voice Coverage

Audit only current, effective UE behavior. Treat a visible control as reportable only after its page status and live Alchemy execution are both verified.

## Required tools

- Prefer MasterGo MCP for structural node reads.
- Use the signed-in browser for visual status checks, Alchemy tests, Drive fallback, and Google Sheets edits.
- When working in a governed project, read and follow its `AGENTS.md`, identity preflight, logging, and Git delivery rules.

## Operator binding

Before reading assigned modules, resolve the operator from a machine-local binding. In a governed project, prefer its ignored `agent/config/local-profile.json`; otherwise use the ignored `agent/config/audit-ue-local-profile.json`.

- If no binding exists, ask the operator for their name. Never infer identity from the OS username, browser account, Git author, or chat nickname.
- Read [references/team-module-sources.json](references/team-module-sources.json). For a preloaded person, show the matched workbook and module sheet names and ask them to confirm before persisting the binding.
- If the name is not preloaded, search the authorized Drive for that person's work-instruction or work-module sheet. Inspect the candidate workbook and module tab, then ask the operator to confirm the exact file and tab before binding it.
- Store only the confirmed display name, stable local owner id, workbook id, sheet name/gid, and column mapping. Keep the binding machine-local and Git-ignored; never store credentials or browser session data.
- A missing or unconfirmed binding permits read-only discovery only. Do not update the coverage sheet until identity and target write scope are confirmed.

## Workflow

1. Resolve and confirm the operator binding, then verify write access before changing a sheet.
2. Read assigned module names from the confirmed module sheet and its declared module/UE columns. Do not assume every coworker uses the same tab or columns.
3. Open the MasterGo UE first. If no usable MasterGo document exists, search the authorized Drive UE source. Report modules with no readable UE; do not infer controls.
4. Build a page-state matrix before extracting controls.
5. Extract every user-operable control from active pages: switches, sliders, steppers, selectors, segmented modes, buttons, and direct setting entrances.
6. Generate concrete Chinese voice queries that include the parent configuration context, mode, target, action, and value when applicable.
7. Run each query in the correct Alchemy project/environment and inspect the returned operation, not only the classification. For configuration UIs, verify that the operation changes the configuration instead of immediately executing the underlying vehicle action.
8. Classify each control using [references/audit-contract.md](references/audit-contract.md).
9. Build an audit manifest and run `scripts/validate_audit.py <manifest.json>` before writing.
10. Deduplicate against the target sheet. Add only controls whose active UE behavior cannot be executed correctly by voice.
11. Preserve the sheet's existing column order, wording style, formatting, formulas, and unrelated rows. Re-read the exact written range.
12. Record the source, UE version, Alchemy environment, page-state exclusions, test evidence, changed range, and readback. Do not perform Jira actions for this workflow.

When the team source registry changes, run `scripts/validate_team_sources.py references/team-module-sources.json` and re-read every source workbook used for the change.

## Page-status hard gate

Inspect both layer structure and the rendered canvas. MCP node existence does not prove current validity.

Exclude a page or group when any authoritative current-version signal marks it as:

- deleted / 删除;
- shelved / 搁置;
- deprecated / 废弃;
- draft / 草稿;
- backup / 备份;
- historical or superseded.

Visual deletion overlays and current-version labels override the presence of extractable historical nodes. Do not test or report controls from excluded pages. If signals conflict, pause the affected control as `status_conflict`; do not write it.

## Alchemy correctness gate

A query passes only when its returned operation can perform the UE action with the correct target, action, and required value. The following are failures and must be reported when the UE page is active:

- unsupported intent;
- wrong target or wrong operation;
- missing/empty target, action, channel, value, or canonical required for execution;
- chat text without an executable operation;
- scenario block for an otherwise valid UE action;
- GUI-only response when the requested voice action should execute directly.
- direct execution of an underlying vehicle action when the UE control is configuring a trigger, precondition, delayed action, scenario action, automation, or another parent object.

For configuration UIs, set `expected_effect=configure` and require `operation_check.context_match=true`. A correct door, window, seat, climate, media, or navigation operation is still `misrouted` when it acts immediately instead of updating the named configuration object.

Do not report a query merely because its wording could be improved. Try one direct, unambiguous query first; use a second natural paraphrase only when the first result is ambiguous. Preserve both results when they disagree.

## Sheet writing

- Use the operator and vehicle values supplied by the source task or bound profile.
- Describe the control, value domain, and example command precisely.
- Keep semantically different contexts separate even when they share the same underlying target, such as a trigger condition versus a precondition versus an execution action.
- For large option sets, use one row per independently implementable control family and combine repeated positions, modes, or numeric values in the range column. Preserve every exact test query in the manifest `tested_queries` array.
- Replace or remove stale rows when a later audit proves the UE was deleted or shelved.
- Report the final added, removed, and unchanged counts after exact-range readback.

## Completion

Keep the updated sheet open as the deliverable and close intermediate MasterGo, Alchemy, and research tabs. Stop temporary MCP clients. Validate and install the Skill copy when the Skill itself changes.
