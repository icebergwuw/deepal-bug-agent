---
name: deepal-product-bug-handler
description: Handle Deepal/Megatronix product-side Jira Bugs for registered team members. Use when the user sends a Jira Bug link or list, asks "怎么回/怎么处理", asks to update an owner Bug sheet, provides customer/leader follow-up, or opens the project on a new computer and needs identity/access onboarding. Verify the local operator and platform access, read live Jira and formal evidence, route by current assignee, update only an authorized owner sheet/index, and leave traceable logs.
---

# Deepal Product Bug Handler

## Load The Current Rules

Locate the workspace root containing `AGENTS.md` and `agent/rules-version.md`; do not assume a user-specific absolute path. Before handling any Bug, read:

1. `AGENTS.md`
2. `agent/onboarding.md`
3. `agent/rules-version.md`
4. `agent/bug-owners/registry.yaml`
5. `agent/context.md`
6. `agent/evidence-contract.md`
7. `agent/output-contract.md`
8. `agent/sheet-contract.md`
9. `agent/workflows/bug.md`

Read `agent/workflows/review.md` when the input is customer, leader, 可姐, meeting, or复盘 feedback. Treat these project files as authoritative; do not copy owner lists, column definitions, links, mutable product rules, output templates, or evidence gates into this Skill.

## Execute The Project Rules

1. Run `agent/scripts/bug_project_preflight.py`; guide first-time identity selection and real platform login when needed. Stay read-only until the operator, owner scope, and required platforms pass.
2. Select `agent/workflows/bug.md` or `agent/workflows/review.md` from the user input.
3. Resolve the owner only through `agent/bug-owners/registry.yaml` and the ignored local profile; never infer the operator from the OS or browser account.
4. Apply `agent/evidence-contract.md` before forming a conclusion.
5. Form and reuse the single current conclusion through `agent/output-contract.md`.
6. Write and validate Sheets through `agent/sheet-contract.md`. Use `agent/scripts/bug_sheet_contract.py` for the API path. If that API write is blocked and this sheet has no recorded page `/save` HTTP 400 without a new revision, use `agent/scripts/sheet_page_save.py` for plain text, one `=` formula, a clear, or http(s) rich-text labels. After that 400 is recorded, write through the Chrome UI instead of retrying `/save`: jump with the name box, paste only while editing, insert short links, and submit only while the links are still present. Do not click the grid while editing. Checkbox validation and anchor formatting still use the Chrome UI fallback and close with `validate_bug_run.py --phase ui`. Rich text counts only when edit mode shows each label URL and the links remain after leaving edit mode. Never report an API final pass for a page save or UI write.
7. Apply `AGENTS.md` for default intent, external-action permission and sensitive-data boundaries.
8. Read back every required artifact before reporting completion.

## Use The Available Tools

- Use Jira or the signed-in browser to read the complete current issue and timeline.
- Use the operator's current Chrome login state first for Jira, Google Drive/Sheets, and other external sources. Fall back to the in-app browser or connectors only when Chrome is unavailable, unauthenticated, or lacks the required capability; record the actual access surface in the run evidence.
- Use Alchemy and MasterGo only according to the current evidence contract and available authenticated runtime.
- Keep credentials in secure runtime configuration; never copy them into project artifacts or responses.

## Fail Closed

- Stop or downgrade the conclusion when a required source, owner route, write target or readback cannot be verified.
- Report the exact unavailable source or failed validation.
- Do not claim an online action or completed write without current readback evidence.
