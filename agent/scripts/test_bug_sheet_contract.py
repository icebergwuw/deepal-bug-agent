#!/usr/bin/env python3

import unittest

from bug_sheet_contract import build_row, validate_readback


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


if __name__ == "__main__":
    unittest.main()
