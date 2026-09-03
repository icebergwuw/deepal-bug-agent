#!/usr/bin/env python3

import json
from pathlib import Path
import tempfile
import unittest

from bug_sheet_contract import (
    PATCH_ALLOWED_COLUMNS,
    PATCH_PROTECTED_COLUMNS,
    build_batch_requests,
    build_patch_requests,
    build_row,
    rich_text_cell,
    row_fingerprint,
    validate_append_readback,
    validate_patch_readback,
    validate_readback,
    validate_bound_manifests,
    required_platforms_for_manifests,
    resolve_format_source_row_index,
    validate_append_format,
)
from test_bug_evidence_gate import hur_case


class BugSheetContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.item = {
            "key": "ADS-TEST",
            "summary": "富文本链接回归",
            "date": "2026-07-28",
            "info": "现象🙂Jira记录与天气PRD支持该结论。",
            "info_links": [
                {"label": "Jira记录", "url": "http://jira.i-tetris.com/browse/ADS-TEST"},
                {"label": "天气PRD", "url": "https://drive.google.com/file/d/test"},
            ],
            "judgment": "结论：需要修复。\n依据：天气PRD。\n处理：研发处理。",
            "judgment_links": [
                {"label": "天气PRD", "url": "https://drive.google.com/file/d/test"},
            ],
            "status": "可转研发",
            "note": "回归验证。",
            "links": [
                {"label": "Jira原票", "url": "http://jira.i-tetris.com/browse/ADS-TEST"},
                {"label": "天气PRD", "url": "https://drive.google.com/file/d/test"},
            ],
        }

    def _readback_row(self) -> dict:
        cells = build_row(self.item)
        for cell in cells:
            entered = cell.get("userEnteredValue", {})
            if "stringValue" in entered:
                cell["formattedValue"] = entered["stringValue"]
                cell["effectiveValue"] = {"stringValue": entered["stringValue"]}
            elif "boolValue" in entered:
                cell["formattedValue"] = str(entered["boolValue"]).upper()
                cell["effectiveValue"] = {"boolValue": entered["boolValue"]}
        cells[1]["formattedValue"] = "ADS-TEST｜富文本链接回归"
        cells[1]["effectiveValue"] = {
            "stringValue": "ADS-TEST｜富文本链接回归"
        }
        cells[4]["dataValidation"] = {"condition": {"type": "BOOLEAN"}}
        return {"values": cells}

    def test_build_uses_independent_rich_text_links(self) -> None:
        row = build_row(self.item)

        self.assertTrue(
            row[1]["userEnteredValue"]["formulaValue"].startswith("=HYPERLINK(")
        )
        self.assertEqual(row[4]["userEnteredValue"], {"boolValue": False})
        self.assertEqual(row[9]["userEnteredValue"]["stringValue"], "Jira原票\n天气PRD")
        self.assertNotIn("formulaValue", row[9]["userEnteredValue"])

        j_uris = [
            run.get("format", {}).get("link", {}).get("uri")
            for run in row[9]["textFormatRuns"]
        ]
        self.assertIn("http://jira.i-tetris.com/browse/ADS-TEST", j_uris)
        self.assertIn("https://drive.google.com/file/d/test", j_uris)

        c_uris = [
            run.get("format", {}).get("link", {}).get("uri")
            for run in row[2]["textFormatRuns"]
        ]
        self.assertEqual(
            [uri for uri in c_uris if uri],
            [
                "http://jira.i-tetris.com/browse/ADS-TEST",
                "https://drive.google.com/file/d/test",
            ],
        )
        first_c_link = next(
            run
            for run in row[2]["textFormatRuns"]
            if run.get("format", {}).get("link", {}).get("uri")
        )
        self.assertEqual(first_c_link["startIndex"], 4)

    def test_sheet_request_requires_one_manifest_per_key(self) -> None:
        self.assertIn(
            "写表请求必须为每个 Jira 绑定一个证据 manifest",
            validate_bound_manifests([], ["HUR-82492"])[0],
        )

    def test_sheet_request_rejects_key_mismatch_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(
                json.dumps(hur_case(), ensure_ascii=False), encoding="utf-8"
            )
            errors = validate_bound_manifests([str(path)], ["ADS-TEST"])
        self.assertTrue(any("Jira key 不一致" in error for error in errors), errors)

    def test_sheet_request_accepts_valid_schema_v5_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(
                json.dumps(hur_case(), ensure_ascii=False), encoding="utf-8"
            )
            errors = validate_bound_manifests([str(path)], ["HUR-82492"])
        self.assertEqual(errors, [])

    def test_first_link_at_zero_has_one_run(self) -> None:
        cell = rich_text_cell(
            "Jira原票\n天气PRD",
            [
                {"label": "Jira原票", "url": "http://jira.i-tetris.com/browse/ADS-TEST"},
                {"label": "天气PRD", "url": "https://drive.google.com/file/d/test"},
            ],
        )
        zero_runs = [
            run
            for run in cell["textFormatRuns"]
            if run.get("startIndex", 0) == 0
        ]
        self.assertEqual(len(zero_runs), 1)
        self.assertEqual(
            zero_runs[0]["format"]["link"]["uri"],
            "http://jira.i-tetris.com/browse/ADS-TEST",
        )

    def test_single_j_link_uses_native_hyperlink_and_validates(self) -> None:
        self.item["links"] = [
            {"label": "Jira原票", "url": "http://jira.i-tetris.com/browse/ADS-TEST"}
        ]
        row = build_row(self.item)
        self.assertEqual(
            row[9]["userEnteredValue"],
            {
                "formulaValue": (
                    '=HYPERLINK("http://jira.i-tetris.com/browse/ADS-TEST",'
                    '"Jira原票")'
                )
            },
        )
        self.assertNotIn("textFormatRuns", row[9])

        readback = self._readback_row()
        readback["values"][9]["formattedValue"] = "Jira原票"
        readback["values"][9]["effectiveValue"] = {"stringValue": "Jira原票"}
        self.assertEqual(
            validate_append_readback({"rowData": [readback]}, [self.item]),
            [],
        )

    def test_missing_inline_label_fails_closed(self) -> None:
        self.item["judgment_links"] = [
            {"label": "不存在的资料", "url": "https://example.com/missing"}
        ]
        with self.assertRaisesRegex(ValueError, "链接标签未出现在文本中"):
            build_row(self.item)

    def test_validate_rejects_concatenated_j_formula(self) -> None:
        cells = []
        for index in range(10):
            cells.append({"formattedValue": ""})
        cells[1] = {
            "formattedValue": "ADS-TEST｜富文本链接回归",
            "effectiveValue": {"stringValue": "ADS-TEST｜富文本链接回归"},
            "userEnteredValue": {
                "formulaValue": '=HYPERLINK("http://jira","ADS-TEST")'
            },
        }
        cells[4] = {
            "formattedValue": "FALSE",
            "effectiveValue": {"boolValue": False},
            "dataValidation": {"condition": {"type": "BOOLEAN"}},
        }
        cells[9] = {
            "formattedValue": "Jira；PRD",
            "userEnteredValue": {
                "formulaValue": '=HYPERLINK("http://jira","Jira")&HYPERLINK("http://prd","PRD")'
            },
        }

        errors = validate_readback(
            {"rowData": [{"values": cells}]},
            expected_keys=["ADS-TEST"],
        )
        self.assertIn("第1行 J列使用了禁止的多 HYPERLINK 拼接", errors)

    def test_append_request_submits_rich_text_runs(self) -> None:
        requests = build_batch_requests(123, 5, [self.item])
        self.assertEqual(
            [next(iter(request)) for request in requests[:3]],
            ["copyPaste", "setDataValidation", "updateCells"],
        )
        self.assertEqual(
            requests[2]["updateCells"]["fields"],
            "userEnteredValue,textFormatRuns",
        )
        self.assertEqual(
            requests[0]["copyPaste"]["source"]["startRowIndex"],
            106,
        )

    def test_wu_you_format_anchor_is_fixed_to_row_107(self) -> None:
        owners = {"wu-you": {"format_anchor_row": "107"}}
        self.assertEqual(resolve_format_source_row_index("wu-you", None, owners), 106)
        self.assertEqual(resolve_format_source_row_index("wu-you", 106, owners), 106)
        with self.assertRaisesRegex(ValueError, "固定格式锚点为第 107 行"):
            resolve_format_source_row_index("wu-you", 411, owners)

    def test_append_format_must_match_anchor(self) -> None:
        def cell(column: int) -> dict:
            return {
                "effectiveFormat": {
                    "numberFormat": {"type": "DATE"} if column == 0 else None,
                    "backgroundColor": {"red": 1, "green": 1, "blue": 1},
                    "borders": {"bottom": {"style": "SOLID"}},
                    "padding": {"top": 6, "right": 8, "bottom": 6, "left": 8},
                    "horizontalAlignment": "CENTER" if column in (0, 1, 4, 6) else "LEFT",
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP",
                    "hyperlinkDisplayType": "LINKED" if column in (1, 9) else "PLAIN_TEXT",
                    "textFormat": {
                        "foregroundColor": {"red": 0.1},
                        "fontFamily": "Arial",
                        "fontSize": 10,
                        "bold": column in (1, 6),
                        "italic": False,
                        "strikethrough": False,
                        "underline": column == 1,
                    },
                }
            }

        anchor = {"rowData": [{"values": [cell(i) for i in range(10)]}]}
        matching = json.loads(json.dumps(anchor))
        self.assertEqual(validate_append_format(anchor, matching), [])
        mismatched = json.loads(json.dumps(anchor))
        mismatched["rowData"][0]["values"][2]["effectiveFormat"]["padding"]["top"] = 2
        errors = validate_append_format(anchor, mismatched)
        self.assertIn("新增第1行 C列固定格式与第 107 行锚点不一致", errors)

    def test_voice_manifest_requires_alchemy_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "voice-manifest.json"
            path.write_text(
                json.dumps({"evidence_profiles": ["voice"]}), encoding="utf-8"
            )
            self.assertEqual(
                required_platforms_for_manifests([str(path)]),
                {"jira", "google_drive", "alchemy"},
            )

    def test_build_rejects_visible_url_before_write(self) -> None:
        self.item["judgment"] = (
            "结论：需要修复。\n"
            "依据：https://drive.google.com/file/d/test\n"
            "处理：研发处理。"
        )
        with self.assertRaisesRegex(ValueError, "不得显示原始长 URL"):
            build_row(self.item)

    def test_append_validation_requires_every_expected_link(self) -> None:
        readback = self._readback_row()
        readback["values"][9]["textFormatRuns"] = [
            run
            for run in readback["values"][9]["textFormatRuns"]
            if run.get("format", {}).get("link", {}).get("uri")
            != "https://drive.google.com/file/d/test"
        ]
        errors = validate_append_readback(
            {"rowData": [readback]},
            [self.item],
        )
        self.assertTrue(
            any("J列链接目标不符" in error for error in errors),
            errors,
        )

    def test_update_modes_come_from_complete_partition_config(self) -> None:
        self.assertEqual(
            PATCH_ALLOWED_COLUMNS["recheck"],
            frozenset(("C", "D", "G", "I", "J")),
        )
        self.assertEqual(
            PATCH_ALLOWED_COLUMNS["review"],
            frozenset(("G", "H", "I", "J")),
        )
        all_columns = frozenset("ABCDEFGHIJ")
        for mode in PATCH_ALLOWED_COLUMNS:
            self.assertFalse(
                PATCH_ALLOWED_COLUMNS[mode] & PATCH_PROTECTED_COLUMNS[mode]
            )
            self.assertEqual(
                PATCH_ALLOWED_COLUMNS[mode] | PATCH_PROTECTED_COLUMNS[mode],
                all_columns,
            )

    def test_recheck_patch_is_column_scoped(self) -> None:
        before = self._readback_row()
        changes = {
            "C": {
                "text": "重新核验：天气PRD定义目标行为。",
                "links": [
                    {
                        "label": "天气PRD",
                        "url": "https://drive.google.com/file/d/test",
                    }
                ],
            },
            "D": {
                "text": "结论：需要修复。\n依据：天气PRD。\n处理：语音研发处理。",
                "links": [
                    {
                        "label": "天气PRD",
                        "url": "https://drive.google.com/file/d/test",
                    }
                ],
            },
            "G": "可转语音",
            "I": "待车端回归。",
            "J": {
                "links": [
                    {
                        "label": "Jira原票",
                        "url": "http://jira.i-tetris.com/browse/ADS-TEST",
                    },
                    {
                        "label": "天气PRD",
                        "url": "https://drive.google.com/file/d/test",
                    },
                ]
            },
        }
        result = build_patch_requests(
            123,
            145,
            "ADS-TEST",
            "recheck",
            before,
            row_fingerprint(before),
            changes,
        )
        self.assertEqual(result["changedColumns"], ["C", "D", "G", "I", "J"])
        self.assertEqual(result["sheetRow"], 145)
        self.assertEqual(result["rowIndex"], 144)
        self.assertTrue(result["freshReadRequiredImmediatelyBeforeBatchUpdate"])
        self.assertEqual(len(result["requests"]), 5)
        self.assertEqual(
            result["requests"][0]["updateCells"]["fields"],
            "userEnteredValue,textFormatRuns",
        )
        self.assertEqual(
            result["requests"][2]["updateCells"]["fields"],
            "userEnteredValue",
        )

    def test_patch_rejects_stale_fingerprint_and_forbidden_columns(self) -> None:
        before = self._readback_row()
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            build_patch_requests(
                123,
                6,
                "ADS-TEST",
                "recheck",
                before,
                "stale",
                {"G": "待复核"},
            )
        with self.assertRaisesRegex(ValueError, "review 模式禁止修改列：D"):
            build_patch_requests(
                123,
                6,
                "ADS-TEST",
                "review",
                before,
                row_fingerprint(before),
                {"D": {"text": "不能覆盖初次判断", "links": []}},
            )

    def test_review_patch_allows_g_h_i_j_and_preserves_other_columns(self) -> None:
        before = self._readback_row()
        changes = {
            "G": "可关闭",
            "H": {
                "text": "结论：客户接受现状。\n依据：客户复盘。\n处理：结束跟进；吴优处理。",
                "links": [
                    {
                        "label": "客户复盘",
                        "url": "https://drive.google.com/file/d/review",
                    }
                ],
            },
            "I": "无。",
            "J": {
                "links": [
                    {
                        "label": "客户复盘",
                        "url": "https://drive.google.com/file/d/review",
                    }
                ]
            },
        }
        result = build_patch_requests(
            123,
            6,
            "ADS-TEST",
            "review",
            before,
            row_fingerprint(before),
            changes,
        )
        self.assertEqual(result["changedColumns"], ["G", "H", "I", "J"])

        after = self._readback_row()
        for column, spec in changes.items():
            index = ord(column) - ord("A")
            patch_cell = result["requests"][
                result["changedColumns"].index(column)
            ]["updateCells"]["rows"][0]["values"][0]
            after["values"][index] = patch_cell
            if column in ("G", "I"):
                after["values"][index]["formattedValue"] = spec
                after["values"][index]["effectiveValue"] = {"stringValue": spec}
            elif column == "J":
                visible = "\n".join(link["label"] for link in spec["links"])
                after["values"][index]["formattedValue"] = visible
                after["values"][index]["effectiveValue"] = {
                    "stringValue": visible
                }
            else:
                after["values"][index]["formattedValue"] = spec["text"]
                after["values"][index]["effectiveValue"] = {
                    "stringValue": spec["text"]
                }

        self.assertEqual(
            validate_patch_readback(before, after, "ADS-TEST", "review", changes),
            [],
        )
        after["values"][5]["userEnteredValue"] = {"stringValue": "被误覆盖"}
        self.assertIn(
            "F 列未声明修改但写后发生变化",
            validate_patch_readback(
                before,
                after,
                "ADS-TEST",
                "review",
                changes,
            ),
        )


if __name__ == "__main__":
    unittest.main()
