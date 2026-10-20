#!/usr/bin/env python3
"""Authorize one Jira comment only after the evidence gate passes.

add_jira_comment does not check evidence. This script is the gate in front of
that write. It emits a receipt only when the schema v5 manifest passes and the
comment body is exactly decision.text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from validate_bug_evidence_gate import validate_manifest


AI_SUFFIX = "（AI Generated）"


def _canonical(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def authorize(
    manifest: Any, comment: str, phase: str
) -> tuple[dict[str, Any] | None, list[str]]:
    """Return a receipt, or gate errors and no receipt."""

    errors = validate_manifest(manifest)
    if not isinstance(manifest, dict):
        return None, errors or ["manifest 必须是对象"]

    decision = manifest.get("decision")
    text = decision.get("text") if isinstance(decision, dict) else None
    normalized = comment.replace("\r\n", "\n").strip()
    if AI_SUFFIX in normalized:
        errors.append("评论正文不要自带（AI Generated）；MCP 会追加")
    if not isinstance(text, str) or normalized != text.strip():
        errors.append("评论正文必须与 decision.text 完全一致")
    if phase not in {"d", "h"}:
        errors.append("phase 必须为 d 或 h")
    jira_key = manifest.get("jira_key")
    if not isinstance(jira_key, str) or not jira_key.strip():
        errors.append("manifest 缺少 jira_key")
    if errors:
        return None, errors

    receipt = {
        "schema_version": 1,
        "gate": "passed",
        "jira_key": jira_key,
        "phase": phase,
        "status": decision.get("status"),
        "decision_text_sha256": _sha256(text.strip()),
        "manifest_sha256": _sha256(_canonical(manifest)),
        "authorized_comment": text.strip(),
    }
    return receipt, []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--comment-file", type=Path, required=True)
    parser.add_argument("--phase", choices=("d", "h"), required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    comment = args.comment_file.read_text(encoding="utf-8")
    receipt, errors = authorize(manifest, comment, args.phase)
    if errors or receipt is None:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.receipt.with_suffix(args.receipt.suffix + ".tmp")
    temporary.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(args.receipt)
    print(
        json.dumps(
            {
                "ok": True,
                "jira_key": receipt["jira_key"],
                "status": receipt["status"],
                "receipt": str(args.receipt),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
