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


    def _ui_readback(self, directory: Path) -> Path:
        payload = {
            "write_surface": "chrome_ui",
            "jira_key": "HUR-82492",
            "sheet_row": 2,
            "update_mode": "append",
            "api_block_reason": "batchUpdate 未能发送：gapi 没有 token，SAPISIDHASH 400，ERR_BLOCKED_BY_CLIENT",
            "selection": "A2",
            "row_height_fit": True,
            "entered_edit_with_escape": True,
            "screenshot_not_used_as_cell_proof": True,
            "filter_action": "no_filter_recorded",
            "cells": {
                "A": {"formula_bar": "2026-09-23"},
                "B": {"formula_bar": '=HYPERLINK("http://jira.i-tetris.com/browse/HUR-82492","HUR-82492｜摘要")'},
                "C": {
                    "formula_bar": "现象。[Jira原票]",
                    "links": [{"text": "Jira原票", "uri": "http://jira.i-tetris.com/browse/HUR-82492"}],
                },
                "D": {
                    "formula_bar": "结论：保留。\n依据：Jira原票·描述。\n处理：关闭。吴优处理。",
                    "links": [{"text": "Jira原票·描述", "uri": "http://jira.i-tetris.com/browse/HUR-82492"}],
                },
                "E": {"formula_bar": "FALSE", "checkbox": True},
                "F": {"formula_bar": "", "before_formula_bar": ""},
                "G": {"formula_bar": "可关闭"},
                "H": {"formula_bar": "", "before_formula_bar": ""},
                "I": {"formula_bar": "无隐藏需求。"},
                "J": {
                    "formula_bar": "Jira原票·描述",
                    "links": [{"text": "Jira原票·描述", "uri": "http://jira.i-tetris.com/browse/HUR-82492"}],
                },
            },
        }
        ui_path = directory / "ui-readback.json"
        ui_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return ui_path

    def test_ui_phase_accepts_formula_bar_readback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._bundle(root)
            ui_path = self._ui_readback(root)
            log_path = Path(bundle["action_log"])
            log_path.write_text(
                LOG_TEXT + "\n- 界面回读已完成。未通过 API final。\n- HUR-82492 行 2\n",
                encoding="utf-8",
            )
            bundle["status"] = "ui_verified"
            bundle["completed_at"] = "2026-09-23T16:00:00+08:00"
            bundle["items"][0]["ui_readback_path"] = str(ui_path)
            bundle["items"][0]["ui_readback_sha256"] = hashlib.sha256(ui_path.read_bytes()).hexdigest()
            self.assertEqual(validate_run_bundle(bundle, "ui"), [])
            final_errors = validate_run_bundle(bundle, "final")
            self.assertTrue(any("不能冒充 API final" in error for error in final_errors), final_errors)

    def test_ui_phase_rejects_contaminated_owner_column(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._bundle(root)
            ui_path = self._ui_readback(root)
            payload = json.loads(ui_path.read_text(encoding="utf-8"))
            payload["cells"]["F"]["formula_bar"] = "PC-37245｜导航播报智能提示不支持"
            ui_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            log_path = Path(bundle["action_log"])
            log_path.write_text(LOG_TEXT + "\n界面回读。未通过 API final。\nHUR-82492 行 2\n", encoding="utf-8")
            bundle["status"] = "ui_verified"
            bundle["completed_at"] = "2026-09-23T16:00:00+08:00"
            bundle["items"][0]["ui_readback_path"] = str(ui_path)
            bundle["items"][0]["ui_readback_sha256"] = hashlib.sha256(ui_path.read_bytes()).hexdigest()
            errors = validate_run_bundle(bundle, "ui")
            self.assertTrue(any("F 新增行写后必须为空" in error for error in errors), errors)

    def test_ui_phase_rejects_screenshot_only_proof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._bundle(root)
            ui_path = self._ui_readback(root)
            payload = json.loads(ui_path.read_text(encoding="utf-8"))
            payload["screenshot_not_used_as_cell_proof"] = False
            payload["api_block_reason"] = "api failed"
            ui_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            log_path = Path(bundle["action_log"])
            log_path.write_text(LOG_TEXT + "\n界面回读。未通过 API final。\nHUR-82492 行 2\n", encoding="utf-8")
            bundle["status"] = "ui_verified"
            bundle["completed_at"] = "2026-09-23T16:00:00+08:00"
            bundle["items"][0]["ui_readback_path"] = str(ui_path)
            bundle["items"][0]["ui_readback_sha256"] = hashlib.sha256(ui_path.read_bytes()).hexdigest()
            errors = validate_run_bundle(bundle, "ui")
            self.assertTrue(any("截图不能代替" in error for error in errors), errors)
            self.assertTrue(any("真实 API 阻断" in error for error in errors), errors)



if __name__ == "__main__":
    unittest.main()
