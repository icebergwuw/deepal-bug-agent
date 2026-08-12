#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_bug_evidence_gate import hur_case
from validate_bug_run import validate_run_bundle


LOG_TEXT = """# Test run

- Run ID: test-run-001
- 涉及 Jira：HUR-82492
- 表格位置：bug!A2:J2，HUR-82492 行 2
- 回读校验：A:J、链接、公式、BOOLEAN、保护列、格式和重复 Key 均通过。

## HUR-82492 决策核验卡

- 备注因果链：完整因果链已读。
- 客户问题识别：非客户问题。
- 关联票：关联票已读。
- 证据画像与必查资料：通用画像和 Drive 已读。
- 资料适用范围：J90A exact。
- 冲突处理：以同项目正式定义为准。
- 唯一结论：待复核，吴优负责补齐资料。
"""


class BugRunTest(unittest.TestCase):
    def _bundle(self, directory: Path, *, final: bool = False) -> dict:
        manifest_path = directory / "manifest.json"
        log_path = directory / "run.md"
        readback_path = directory / "readback.json"
        validation_path = directory / "validation.json"
        manifest_path.write_text(json.dumps(hur_case(), ensure_ascii=False), encoding="utf-8")
        log_path.write_text(LOG_TEXT, encoding="utf-8")
        readback_path.write_text('{"row":2}', encoding="utf-8")
        validation_path.write_text('{"ok":true,"errors":[]}', encoding="utf-8")
        item = {
            "jira_key": "HUR-82492",
            "operator_owner_id": "wu-you",
            "target_owner_id": "wu-you",
            "sheet_name": "bug",
            "sheet_row": 2,
            "manifest_path": str(manifest_path),
        }
        if final:
            item.update(
                {
                    "readback_path": str(readback_path),
                    "validation_path": str(validation_path),
                    "readback_sha256": hashlib.sha256(readback_path.read_bytes()).hexdigest(),
                }
            )
        return {
            "schema_version": 1,
            "run_id": "test-run-001",
            "status": "complete" if final else "planned",
            "started_at": "2026-08-12T09:00:00+08:00",
            "completed_at": "2026-08-12T09:10:00+08:00" if final else None,
            "query_summary": "Jira 1 条，新增 1 条",
            "action_log": str(log_path),
            "items": [item],
        }

    def test_prewrite_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(validate_run_bundle(self._bundle(Path(directory))), [])

    def test_final_bundle_requires_matching_readback_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = self._bundle(Path(directory), final=True)
            self.assertEqual(validate_run_bundle(bundle, "final"), [])
            bundle["items"][0]["readback_sha256"] = "bad"
            self.assertIn("HUR-82492 回读文件 sha256 不一致", validate_run_bundle(bundle, "final"))

    def test_no_change_run_still_requires_log(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nochange.md"
            path.write_text("# Run\n\n- Run ID: nochange-1\n- 本次无新增。\n", encoding="utf-8")
            bundle = {
                "schema_version": 1,
                "run_id": "nochange-1",
                "status": "no_changes",
                "started_at": "2026-08-12T09:00:00+08:00",
                "completed_at": "2026-08-12T09:01:00+08:00",
                "query_summary": "Jira 145 条，新增 0 条",
                "action_log": str(path),
                "items": [],
            }
            self.assertEqual(validate_run_bundle(bundle, "final"), [])


if __name__ == "__main__":
    unittest.main()
