#!/usr/bin/env python3
"""Validate the hard gates for a UE-to-Alchemy voice coverage audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PAGE_STATUSES = {
    "active",
    "deleted",
    "shelved",
    "deprecated",
    "draft",
    "backup",
    "status_conflict",
}
REPORTABLE = {
    "unsupported",
    "misrouted",
    "empty_required_slot",
    "chat_only",
    "blocked",
    "gui_only",
}
VERDICTS = REPORTABLE | {"pass", "ambiguous"}
EXPECTED_EFFECTS = {"direct", "navigate", "configure", "content_operation"}


def require_text(value: object, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    for field in ("module", "vehicle", "alchemy_environment"):
        require_text(data.get(field), field, errors)

    pages = data.get("pages")
    controls = data.get("controls")
    if not isinstance(pages, list) or not pages:
        errors.append("pages must be a non-empty array")
        pages = []
    if not isinstance(controls, list):
        errors.append("controls must be an array")
        controls = []

    page_status: dict[str, str] = {}
    for index, page in enumerate(pages):
        prefix = f"pages[{index}]"
        if not isinstance(page, dict):
            errors.append(f"{prefix} must be an object")
            continue
        page_id = page.get("id")
        require_text(page_id, f"{prefix}.id", errors)
        require_text(page.get("name"), f"{prefix}.name", errors)
        status = page.get("status")
        if status not in PAGE_STATUSES:
            errors.append(f"{prefix}.status is invalid: {status!r}")
        if status != "active":
            require_text(page.get("evidence"), f"{prefix}.evidence", errors)
        if isinstance(page_id, str) and page_id:
            if page_id in page_status:
                errors.append(f"duplicate page id: {page_id}")
            page_status[page_id] = status

    seen_controls: set[str] = set()
    for index, control in enumerate(controls):
        prefix = f"controls[{index}]"
        if not isinstance(control, dict):
            errors.append(f"{prefix} must be an object")
            continue
        control_id = control.get("id")
        require_text(control_id, f"{prefix}.id", errors)
        require_text(control.get("name"), f"{prefix}.name", errors)
        require_text(control.get("query"), f"{prefix}.query", errors)
        tested_queries = control.get("tested_queries")
        if tested_queries is not None:
            if not isinstance(tested_queries, list) or not tested_queries:
                errors.append(f"{prefix}.tested_queries must be a non-empty array")
            else:
                for query_index, query in enumerate(tested_queries):
                    require_text(
                        query,
                        f"{prefix}.tested_queries[{query_index}]",
                        errors,
                    )
        expected_effect = control.get("expected_effect", "direct")
        if expected_effect not in EXPECTED_EFFECTS:
            errors.append(
                f"{prefix}.expected_effect is invalid: {expected_effect!r}"
            )
        if isinstance(control_id, str) and control_id:
            if control_id in seen_controls:
                errors.append(f"duplicate control id: {control_id}")
            seen_controls.add(control_id)

        page_id = control.get("page_id")
        if page_id not in page_status:
            errors.append(f"{prefix}.page_id does not reference a known page")
        elif page_status[page_id] != "active":
            errors.append(
                f"{prefix} references non-active page {page_id} "
                f"({page_status[page_id]})"
            )

        verdict = control.get("verdict")
        if verdict not in VERDICTS:
            errors.append(f"{prefix}.verdict is invalid: {verdict!r}")
        report = control.get("report")
        if not isinstance(report, bool):
            errors.append(f"{prefix}.report must be boolean")
        elif verdict in REPORTABLE and not report:
            errors.append(f"{prefix} has reportable verdict but report is false")
        elif verdict in {"pass", "ambiguous"} and report:
            errors.append(f"{prefix} cannot report verdict {verdict}")

        check = control.get("operation_check")
        if not isinstance(check, dict):
            errors.append(f"{prefix}.operation_check must be an object")
            continue
        require_text(check.get("evidence"), f"{prefix}.operation_check.evidence", errors)
        for field in ("target_match", "action_match", "value_match"):
            if not isinstance(check.get(field), bool):
                errors.append(f"{prefix}.operation_check.{field} must be boolean")
        context_match = check.get("context_match")
        if context_match is not None and not isinstance(context_match, bool):
            errors.append(f"{prefix}.operation_check.context_match must be boolean")
        if expected_effect in {"configure", "content_operation"} and not isinstance(
            context_match, bool
        ):
            errors.append(
                f"{prefix} {expected_effect} requires boolean context_match"
            )
        if verdict == "pass" and not all(
            check.get(field) is True
            for field in ("target_match", "action_match", "value_match")
        ):
            errors.append(f"{prefix} pass requires all operation checks to be true")
        if verdict == "pass" and expected_effect in {
            "configure",
            "content_operation",
        } and context_match is not True:
            errors.append(f"{prefix} pass requires context_match=true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid manifest: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
