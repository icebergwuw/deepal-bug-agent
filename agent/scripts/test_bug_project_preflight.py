#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest

from bug_project_preflight import (
    assess,
    format_time,
    initialize_external,
    initialize_profile,
    load_owners,
    load_profile,
    local_secret_file_status,
    record_access,
)
import zipfile


class BugProjectPreflightTest(unittest.TestCase):
    def setUp(self) -> None:
        self.owners = {
            "wu-you": {
                "id": "wu-you",
                "name": "吴优",
                "status": "active",
                "write_mode": "read_write",
            },
            "pending-owner": {
                "id": "pending-owner",
                "name": "待确认人员",
                "status": "pending",
                "write_mode": "read_only",
            },
        }
        self.skill = {"installed": True, "matches_template": True, "target": "test"}

    def test_registry_parser_reads_current_active_owners(self) -> None:
        owners = load_owners()
        self.assertEqual(owners["wu-you"]["name"], "吴优")
        self.assertEqual(owners["li-xin"]["write_mode"], "read_write")

    def test_missing_profile_is_read_only(self) -> None:
        result = assess(
            None,
            self.owners,
            required_owner_id="wu-you",
            required_platforms=[],
            max_access_age_hours=24,
            skill=self.skill,
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["mode"], "read_only")

    def test_init_rejects_pending_owner_and_requires_explicit_replace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            with self.assertRaisesRegex(ValueError, "不是 active"):
                initialize_profile(
                    "pending-owner", [], replace=False, owners=self.owners, path=path
                )
            initialize_profile(
                "wu-you", [], replace=False, owners=self.owners, path=path
            )
            with self.assertRaisesRegex(ValueError, "已存在"):
                initialize_profile(
                    "wu-you", [], replace=False, owners=self.owners, path=path
                )

    def test_profile_contains_no_credentials_and_is_private(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            initialize_profile(
                "wu-you", [], replace=False, owners=self.owners, path=path
            )
            payload = load_profile(path)
            self.assertEqual(payload["operator_owner_id"], "wu-you")
            self.assertNotIn("token", json.dumps(payload).lower())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_required_access_expires_and_must_be_live_verified(self) -> None:
        now = datetime(2026, 8, 11, 2, 0, tzinfo=timezone.utc)
        profile = {
            "operator_owner_id": "wu-you",
            "allowed_write_owner_ids": ["wu-you"],
            "online_access": {
                "jira": {"verified_at": format_time(now - timedelta(hours=25))}
            },
        }
        expired = assess(
            profile,
            self.owners,
            required_owner_id="wu-you",
            required_platforms=["jira"],
            max_access_age_hours=24,
            skill=self.skill,
            now=now,
        )
        self.assertFalse(expired["ok"])
        profile["online_access"]["jira"]["verified_at"] = format_time(
            now - timedelta(hours=1)
        )
        fresh = assess(
            profile,
            self.owners,
            required_owner_id="wu-you",
            required_platforms=["jira"],
            max_access_age_hours=24,
            skill=self.skill,
            now=now,
        )
        self.assertTrue(fresh["ok"])

    def test_record_access_only_records_receipt_metadata(self) -> None:
        profile = {"online_access": {}}
        record_access(profile, ["jira", "google_drive"])
        self.assertEqual(
            profile["online_access"]["jira"]["method"],
            "live_read_verified_by_agent",
        )

    def test_local_secret_file_must_not_be_world_readable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("SECRET=not-a-real-secret\n", encoding="utf-8")
            path.chmod(0o644)
            self.assertFalse(local_secret_file_status(path)["private_permissions"])
            path.chmod(0o600)
            self.assertTrue(local_secret_file_status(path)["private_permissions"])

    def test_external_operator_gets_excel_without_team_sheet_access(self) -> None:
        owners = {
            **self.owners,
            "wu-you": {**self.owners["wu-you"], "spreadsheet_id": "team-sheet-id"},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile_path = root / "profile.json"
            workbook = root / "colleague-bug-sheet.xlsx"
            with self.assertRaisesRegex(ValueError, "明确确认身份"):
                initialize_external(
                    "张三",
                    "guessed",
                    "excel",
                    str(workbook),
                    replace=False,
                    owners=owners,
                    path=profile_path,
                )
            payload = initialize_external(
                "张三",
                "explicit_user_confirmation",
                "excel",
                str(workbook),
                replace=False,
                owners=owners,
                path=profile_path,
            )
            self.assertEqual(payload["operator_mode"], "external")
            self.assertEqual(payload["allowed_write_owner_ids"], [])
            self.assertTrue(workbook.is_file())
            with zipfile.ZipFile(workbook) as archive:
                sheet = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
            self.assertIn("产品Agent判断", sheet)
            result = assess(
                payload,
                owners,
                required_owner_id=None,
                required_platforms=[],
                max_access_age_hours=24,
                skill=self.skill,
            )
            self.assertTrue(result["ok"])
            self.assertEqual(result["mode"], "external_write")
            self.assertIn("测试版本", " ".join(result["warnings"]))
            blocked = assess(
                payload,
                owners,
                required_owner_id="wu-you",
                required_platforms=[],
                max_access_age_hours=24,
                skill=self.skill,
            )
            self.assertFalse(blocked["ok"])
            self.assertEqual(blocked["mode"], "read_only")
            with self.assertRaisesRegex(ValueError, "团队 Bug 表"):
                initialize_external(
                    "张三",
                    "explicit_user_confirmation",
                    "google_sheet",
                    "https://docs.google.com/spreadsheets/d/team-sheet-id/edit",
                    replace=True,
                    owners=owners,
                    path=profile_path,
                )

    def test_team_profile_remains_read_write(self) -> None:
        profile = {
            "operator_owner_id": "wu-you",
            "allowed_write_owner_ids": ["wu-you"],
            "online_access": {},
        }
        result = assess(
            profile,
            self.owners,
            required_owner_id="wu-you",
            required_platforms=[],
            max_access_age_hours=24,
            skill=self.skill,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["mode"], "read_write")
        self.assertEqual(result["operator_mode"], "team")


if __name__ == "__main__":
    unittest.main()
