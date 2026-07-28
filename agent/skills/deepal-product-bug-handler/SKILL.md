---
name: deepal-product-bug-handler
description: Handle Deepal/Megatronix product-side Jira Bugs for Wu You. Use when the user sends a Jira Bug link or list, asks "怎么回/怎么处理", asks to update an owner Bug sheet, or provides customer/leader follow-up for an already handled Bug. Read live Jira, Drive/work-instruction evidence, Alchemy for voice issues, and MasterGo UE when accessible; make a concise product-owner decision, route by current assignee, update the correct sheet/index when authorized by the project defaults, and leave traceable logs.
---

# Deepal Product Bug Handler

## Load The Current Rules

Use `/Users/you.wu/Desktop/Mega Project/Bug` as the workspace root. Before handling any Bug, read:

1. `AGENTS.md`
2. `agent/rules-version.md`
3. `agent/bug-owners/registry.yaml`
4. `agent/context.md`
5. `agent/evidence-contract.md`
6. `agent/output-contract.md`
7. `agent/sheet-contract.md`
8. `agent/workflows/bug.md`

Read `agent/workflows/review.md` when the input is customer, leader, 可姐, meeting, or复盘 feedback. Treat these project files as authoritative; do not copy owner lists, column definitions, links, mutable product rules, output templates, or evidence gates into this Skill.

## Execute The Project Rules

1. Select `agent/workflows/bug.md` or `agent/workflows/review.md` from the user input.
2. Resolve the owner only through `agent/bug-owners/registry.yaml`.
3. Apply `agent/evidence-contract.md` before forming a conclusion.
4. Form and reuse the single current conclusion through `agent/output-contract.md`.
5. Write and validate Sheets only through `agent/sheet-contract.md`; use `agent/scripts/bug_sheet_contract.py` for contract-supported append and existing-row patch operations.
6. Apply `AGENTS.md` for default intent, external-action permission and sensitive-data boundaries.
7. Read back every required artifact before reporting completion.

## Use The Available Tools

- Use Jira or the signed-in browser to read the complete current issue and timeline.
- Use Google Drive and Sheets connectors for current documents, work instructions and owner sheets.
- Use Alchemy and MasterGo only according to the current evidence contract and available authenticated runtime.
- Keep credentials in secure runtime configuration; never copy them into project artifacts or responses.

## Fail Closed

- Stop or downgrade the conclusion when a required source, owner route, write target or readback cannot be verified.
- Report the exact unavailable source or failed validation.
- Do not claim an online action or completed write without current readback evidence.
