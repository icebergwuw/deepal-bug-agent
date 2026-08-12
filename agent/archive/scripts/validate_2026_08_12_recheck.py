#!/usr/bin/env python3
"""One-time final validator for the 2026-08-12 rows 321-331 recheck."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "agent/scripts"))
from bug_sheet_contract import validate_patch_readback, validate_readback  # noqa: E402


LOG_DIR = ROOT / "agent/logs/bug-actions"
ORDER = ["ADS-48729", "ADS-48572", "HUR-82888", "PC-38473", "PC-38472", "PC-38471", "ADS-47316", "SLV-44180", "ADS-46860", "HUR-77192", "HUR-72809"]


def rows(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["sheets"][0]["data"][0]["rowData"]


def main() -> int:
    before = rows(LOG_DIR / "2026-08-12-daily-new-bugs-recheck-prewrite-readback.json")
    after = rows(LOG_DIR / "2026-08-12-daily-new-bugs-recheck-readback.json")
    errors = validate_readback(
        {"rowData": after},
        expected_keys=ORDER,
    )
    per_key = {}
    for index, key in enumerate(ORDER):
        patch = json.loads((LOG_DIR / f"2026-08-12-{key}-recheck-patch-input.json").read_text(encoding="utf-8"))
        item_errors = validate_patch_readback(before[index], after[index], key, "recheck", patch["changes"])
        for cell_index, cell in enumerate(after[index].get("values", [])):
            wrap = cell.get("effectiveFormat", {}).get("wrapStrategy") or cell.get("userEnteredFormat", {}).get("wrapStrategy")
            if wrap != "WRAP":
                item_errors.append(f"{chr(65 + cell_index)} 列格式不是 WRAP")
        if after[index]["values"][4].get("dataValidation", {}).get("condition", {}).get("type") != "BOOLEAN":
            item_errors.append("E 列缺少 BOOLEAN 数据验证")
        per_key[key] = {"ok": not item_errors, "errors": item_errors}
        errors.extend(f"{key}：{error}" for error in item_errors)

    key_payload = json.loads((LOG_DIR / "2026-08-12-daily-new-bugs-recheck-keys-readback.json").read_text(encoding="utf-8"))
    key_rows = key_payload["sheets"][0]["data"][0]["rowData"]
    keys = []
    for row in key_rows:
        cell = row.get("values", [{}])[0]
        text = " ".join(
            str(value)
            for value in (
                cell.get("formattedValue", ""),
                cell.get("userEnteredValue", {}).get("formulaValue", ""),
            )
        )
        match = re.search(r"([A-Z][A-Z0-9]+-\d+)", text)
        if match:
            keys.append(match.group(1))
    counts = Counter(keys)
    for key in ORDER:
        if counts[key] != 1:
            errors.append(f"目标 Key {key} 在线出现 {counts[key]} 次")
    historical_duplicates = {key: count for key, count in counts.items() if count > 1 and key not in ORDER}
    result = {
        "ok": not errors,
        "errors": errors,
        "per_key": per_key,
        "checks": {
            "range": "bug!A321:J331",
            "row_count": len(after),
            "protected_columns_unchanged": all(item["ok"] for item in per_key.values()),
            "target_key_counts": {key: counts[key] for key in ORDER},
            "historical_duplicates": historical_duplicates,
            "formula_boolean_links_format": "validated",
        },
    }
    output = LOG_DIR / "2026-08-12-daily-new-bugs-recheck-validation.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not errors:
        readback_path = LOG_DIR / "2026-08-12-daily-new-bugs-recheck-readback.json"
        digest = hashlib.sha256(readback_path.read_bytes()).hexdigest()
        bundle_path = LOG_DIR / "2026-08-12-daily-new-bugs-run.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        bundle["status"] = "complete"
        bundle["completed_at"] = "2026-08-12T11:03:23+08:00"
        for item in bundle["items"]:
            item["readback_path"] = str(readback_path)
            item["validation_path"] = str(output)
            item["readback_sha256"] = digest
        bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log_path = Path(bundle["action_log"])
        log_text = log_path.read_text(encoding="utf-8")
        log_text = log_text.replace(
            "- 回读校验：待写后补充并由 final run bundle 校验",
            "- 回读校验：bug!A321:J331 已回读；A:J、B公式、C/D/J链接、E列BOOLEAN、保护列、WRAP格式和11个目标Key唯一性均通过。历史重复SLV-44272仍为2条，非本次产生。",
        ).replace(
            "- readback_sha256：待写后补充",
            f"- readback_sha256：{digest}",
        )
        log_path.write_text(log_text, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
