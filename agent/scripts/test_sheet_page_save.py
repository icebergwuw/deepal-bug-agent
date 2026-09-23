#!/usr/bin/env python3

import unittest

from sheet_page_save import (
    PageSaveUnsupported,
    build_command,
    clear_command,
    dump_command,
    page_post_expression,
    parse_save_response,
    redact_resource_url,
    save_url_from_resource,
    set_string_command,
)


PROBE = (
    '[["2135747181",425,426,10,11],[132274236,3,[2,"probe"],null,null,0],'
    "[null,[[null,513,[0],null,null,null,null,null,null,null,null,0]]]]"
)
CLEAR = '[["2135747181",425,426,10,11],[132274237],[]]'
BIND_URL = (
    "https://docs.google.com/spreadsheets/d/sheet/bind"
    "?id=sid-1&sid=sid-1&token=token-1&ouid=ouid-1&vc=1&VER=1&zx=1&t=1"
)


class SheetPageSaveTest(unittest.TestCase):
    def test_string_command_matches_captured_shape(self) -> None:
        command = set_string_command("2135747181", 426, "K", "probe")
        self.assertEqual(dump_command(command), PROBE)

    def test_formula_uses_the_same_user_entered_string_shape(self) -> None:
        command = set_string_command("2135747181", 426, "K", "=2+2")
        self.assertIn('[2,"=2+2"]', dump_command(command))
        self.assertIn("132274236", dump_command(command))

    def test_clear_command_matches_captured_shape(self) -> None:
        self.assertEqual(dump_command(clear_command("2135747181", 426, "K")), CLEAR)

    def test_two_link_command_uses_captured_rich_text_shape(self) -> None:
        command = build_command(
            "2135747181",
            426,
            "K",
            "docA\ndocB",
            links=[
                {"text": "docA", "url": "https://example.com/script-a"},
                {"text": "docB", "url": "https://example.com/script-b"},
            ],
        )
        mutation = command[1]
        link_format = [None, [2, 1136076], None, None, None, None, None, None, 1]
        self.assertEqual(len(mutation), 27)
        self.assertEqual(mutation[0], 125982780)
        self.assertEqual(mutation[1], 6291459)
        self.assertEqual(mutation[2], [2, "docA\ndocB"])
        self.assertEqual(mutation[5], 0)
        self.assertIsNone(mutation[3])
        self.assertIsNone(mutation[24])
        self.assertEqual(
            mutation[25],
            [[0, link_format], [4], [5, link_format], [9]],
        )
        self.assertEqual(
            mutation[26],
            [
                [0, "https://example.com/script-a"],
                [4],
                [5, "https://example.com/script-b"],
                [9],
            ],
        )
        self.assertEqual(command[2][1][0][0], 67108350)
        expression = page_post_expression(command, 2159, 3)
        self.assertIn("25813757", expression)
        self.assertNotIn("21299578", expression)
        self.assertNotIn("sid-1", expression)
        self.assertNotIn("token=", expression)
        self.assertNotIn("ouid", expression)

    def test_rich_text_rejects_bad_links(self) -> None:
        with self.assertRaises(ValueError):
            build_command(
                "2135747181",
                426,
                "C",
                "证据",
                links=[{"text": "证据", "url": "ftp://example.com"}],
            )
        with self.assertRaises(ValueError):
            build_command(
                "2135747181",
                426,
                "C",
                "abbc",
                links=[
                    {"text": "ab", "url": "https://example.com/a"},
                    {"text": "bb", "url": "https://example.com/b"},
                ],
            )
        with self.assertRaises(ValueError):
            build_command(
                "2135747181",
                426,
                "C",
                "证据",
                links=[{"text": "缺失", "url": "https://example.com"}],
            )
        with self.assertRaises(PageSaveUnsupported):
            build_command(
                "2135747181",
                426,
                "B",
                '=HYPERLINK("https://example.com","证据")',
                links=[{"text": "证据", "url": "https://example.com"}],
            )

    def test_save_url_drops_bind_only_params(self) -> None:
        url = save_url_from_resource(BIND_URL)
        self.assertIn("/save?", url)
        self.assertNotIn("/bind", url)
        self.assertNotIn("VER=", url)
        self.assertNotIn("zx=", url)
        self.assertIn("sid=sid-1", url)

    def test_redaction_hides_session_fields(self) -> None:
        redacted = redact_resource_url(BIND_URL)
        self.assertNotIn("sid-1", redacted)
        self.assertNotIn("token-1", redacted)
        self.assertNotIn("ouid-1", redacted)
        self.assertIn("id=%5Bredacted%5D", redacted)
        self.assertIn("vc=1", redacted)

    def test_response_parser_reads_revision_and_drops_xssi_prefix(self) -> None:
        body = ")]}'\n" + (
            '{"revisionRanges":[[2145,2145]],"metadata":{"serverRevision":2144}}'
        )
        self.assertEqual(
            parse_save_response(body),
            {"ok": True, "server_revision": 2144, "new_revision": 2145},
        )
        self.assertFalse(parse_save_response("not json")["ok"])

    def test_page_expression_keeps_secrets_out_of_source(self) -> None:
        expression = page_post_expression(
            set_string_command("2135747181", 426, "K", "probe"),
            2144,
            2,
        )
        self.assertIn('body.set("rev", "2144")', expression)
        self.assertIn("reqId: 2", expression)
        self.assertIn("[2,\"probe\"]", expression)
        self.assertNotIn("sid-1", expression)
        self.assertNotIn("token=", expression)
        self.assertIn('url.searchParams.get("sid")', expression)


if __name__ == "__main__":
    unittest.main()
