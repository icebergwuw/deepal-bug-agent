---
name: bug-chain-recheck-trigger
description: Re-run the complete Deepal/Megatronix Bug evidence and handling chain when the user sends only one or more standalone exclamation or question punctuation marks such as `!`, `！！`, `?`, or `？？？？`. Do not activate for punctuation mixed with words, Jira keys, links, or other content.
---

# Bug Chain Recheck Trigger

## Trigger

Activate only when the complete user message, after trimming surrounding whitespace, matches one or more of `!`, `！`, `?`, `？`, with optional spaces between them. Examples that trigger: `!`, `？？`, `!？！`. Examples that do not trigger: `! 看一下`, `HUR-12345!`, a Jira link, or punctuation embedded in a sentence.

Treat the punctuation as a request to re-audit the currently active Bug handling context. If there is no active Jira, Bug list, or clearly identifiable Bug context, report that the trigger has no target and remain read-only; do not invent a Jira or scan every Bug.

## Re-run The Complete Chain

1. Load the workspace `AGENTS.md`, onboarding state, current rule version, owner registry, evidence contract, output contract, sheet contract, and `agent/workflows/bug.md`. Read the review workflow only when the active context contains review or meeting feedback.
2. Run the project preflight and verify the bound local operator, platform access, owner route, and write scope. If preflight does not permit writes, continue with evidence collection only and state the exact limitation.
3. Re-read the active Jira issue in full: fields, description, attachments, all comments in time order, linked issues, duplicate/root-cause relationships, and current assignee/status.
4. Rebuild the applicable evidence profiles from the current issue. Re-search formal sources, follow cited document names, enumerate applicable version families, and read current implementation/platform evidence. Do not reuse a previous conclusion as proof.
5. Reconstruct the expected-behavior card, source roles, inheritance chain, conflicts, and one current decision. Run the schema-v5 evidence gate before any write. Missing or unreadable evidence downgrades the conclusion and must be recorded.
6. Apply the ordinary `recheck` mode: update the existing current-owner row with the newly verified conclusion, preserve protected columns, update the local index, and write the required action log. Never use review mode unless the user supplied review material.
7. Read back every changed artifact and validate the final run bundle. Do not perform Jira comments, assignment, status changes, closure, or other external actions unless the user separately authorized them.

## Output

Report the recheck target, evidence refreshed, current product decision, responsible party, action taken, write/readback status, and any unavailable source. Keep the result truthful if the chain is partial. Follow the project's output contract rather than creating a shortcut-specific format.

This trigger changes only how a recheck is requested; it does not bypass identity, evidence, write, logging, or external-action boundaries.
