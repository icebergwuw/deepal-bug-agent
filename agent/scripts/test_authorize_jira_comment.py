#!/usr/bin/env python3

from pathlib import Path
import tempfile
import unittest

from authorize_jira_comment import authorize
from test_bug_evidence_gate import hur_case


class AuthorizeJiraCommentTest(unittest.TestCase):
    def test_matching_comment_receives_receipt(self) -> None:
        manifest = hur_case()
        receipt, errors = authorize(manifest, manifest["decision"]["text"], "d")
        self.assertEqual(errors, [])
        self.assertIsNotNone(receipt)
        assert receipt is not None
        self.assertEqual(receipt["gate"], "passed")
        self.assertEqual(receipt["jira_key"], "HUR-82492")
        self.assertEqual(receipt["status"], "Invalid")
        self.assertEqual(receipt["authorized_comment"], manifest["decision"]["text"])

    def test_mismatched_or_suffixed_comment_is_rejected(self) -> None:
        manifest = hur_case()
        receipt, errors = authorize(
            manifest,
            manifest["decision"]["text"] + "\n（AI Generated）",
            "d",
        )
        self.assertIsNone(receipt)
        self.assertTrue(any("decision.text" in error for error in errors))
        self.assertTrue(any("AI Generated" in error for error in errors))

    def test_deterministic_comment_without_formal_target_writes_nothing(self) -> None:
        manifest = hur_case()
        manifest["decision"]["status"] = "可关闭"
        manifest["decision"]["text"] = (
            "结论：按非问题关闭。依据：无正式定义。处理：测试关闭。"
        )
        for source in manifest["scope_checks"]:
            if source["role"] == "formal_target":
                source["role"] = "context_only"
        receipt, errors = authorize(manifest, manifest["decision"]["text"], "d")
        self.assertIsNone(receipt)
        self.assertTrue(any("formal_target" in error for error in errors))

    def test_cli_failure_does_not_replace_receipt(self) -> None:
        import json
        import subprocess
        import sys

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = root / "manifest.json"
            comment_path = root / "comment.txt"
            receipt_path = root / "receipt.json"
            manifest_path.write_text("{}", encoding="utf-8")
            comment_path.write_text("结论：不行。", encoding="utf-8")
            receipt_path.write_text('{"gate":"stale"}\n', encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("authorize_jira_comment.py")),
                    "--manifest",
                    str(manifest_path),
                    "--comment-file",
                    str(comment_path),
                    "--phase",
                    "d",
                    "--receipt",
                    str(receipt_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 1)
            self.assertEqual(json.loads(receipt_path.read_text()), {"gate": "stale"})


if __name__ == "__main__":
    unittest.main()
