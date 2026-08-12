#!/usr/bin/env python3
"""One-time patch-input builder for the 2026-08-12 rows 321-331 recheck."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "agent/scripts"))
from bug_sheet_contract import row_fingerprint  # noqa: E402


LOG_DIR = ROOT / "agent/logs/bug-actions"
PREWRITE = LOG_DIR / "2026-08-12-daily-new-bugs-recheck-prewrite-readback.json"
ROWS = {
    "ADS-48729": 321, "ADS-48572": 322, "HUR-82888": 323,
    "PC-38473": 324, "PC-38472": 325, "PC-38471": 326,
    "ADS-47316": 327, "SLV-44180": 328, "ADS-46860": 329,
    "HUR-77192": 330, "HUR-72809": 331,
}


def visible(cell: dict) -> str:
    return str(cell.get("formattedValue", ""))


def main() -> None:
    payload = json.loads(PREWRITE.read_text(encoding="utf-8"))
    row_data = payload["sheets"][0]["data"][0]["rowData"]
    request_paths = []
    for offset, (key, row_number) in enumerate(ROWS.items()):
        row = row_data[offset]
        if not visible(row["values"][1]).startswith(f"{key}｜"):
            raise RuntimeError(f"row {row_number} key mismatch")
        manifest_path = LOG_DIR / f"2026-08-12-{key}-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sources = [item for item in manifest["scope_checks"] if item["source_id"].startswith("drive-")]
        jira_url = f"http://jira.i-tetris.com/browse/{key}"
        c_parts = [visible(row["values"][2])]
        c_links = [{"label": "Jira原票", "url": jira_url}]
        j_links = [{"label": "Jira原票", "url": jira_url}]
        source_labels = []
        for source in sources:
            # Resolve URL through the candidate that references this source id.
            candidate = next(
                candidate
                for check in manifest["required_evidence_checks"]
                for candidate in check.get("candidate_audit", {}).get("candidates", [])
                if source["source_id"] in candidate.get("source_ids", [])
            )
            label = source["source"]
            source_labels.append(f"{label}·{source['source_location']}")
            c_links.append({"label": label, "url": candidate["url"]})
            j_links.append({"label": label, "url": candidate["url"]})
        if source_labels:
            c_parts.append("Drive复核：" + "；".join(source_labels) + "。")
        else:
            c_parts.append("Drive复核：检索回执中的候选已逐项排除，仍未定位同项目同场景正式目标。")

        lines = manifest["decision"]["text"].splitlines()
        evidence = "Jira原票；" + ("；".join(source_labels) + "；" if source_labels else "") + "Drive候选已逐项审计；Alchemy当前停在SSO登录页。"
        lines[1] = "依据：" + evidence
        judgment = "\n".join(lines)
        d_links = [{"label": "Jira原票", "url": jira_url}]
        for link in j_links[1:]:
            d_links.append(link)
        note = visible(row["values"][8])
        if sources:
            note += "；Drive正文已读，仍需补齐同范围决定性条款及Alchemy当前/标准/项目功能点"
        else:
            note += "；Drive候选已逐项排除，仍需补齐同范围正式资料及Alchemy当前/标准/项目功能点"
        changes = {
            "C": {"text": "\n".join(c_parts), "links": c_links},
            "D": {"text": judgment, "links": d_links},
            "I": note,
            "J": {"links": j_links},
        }
        patch_payload = {"current_row": row, "changes": changes}
        input_path = LOG_DIR / f"2026-08-12-{key}-recheck-patch-input.json"
        input_path.write_text(json.dumps(patch_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta_path = LOG_DIR / f"2026-08-12-{key}-recheck-patch-meta.json"
        meta_path.write_text(json.dumps({"key": key, "row": row_number, "fingerprint": row_fingerprint(row), "manifest": str(manifest_path), "input": str(input_path)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        request_paths.append(str(meta_path))
    (LOG_DIR / "2026-08-12-daily-new-bugs-recheck-patch-metas.txt").write_text("\n".join(request_paths) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
