#!/usr/bin/env python3
"""Build signed-in Google Sheets page /save commands.

The Sheets API batchUpdate path stays the default. When it is blocked, the
already-open sheet page can post to its own /save endpoint. This module only
builds the proven plain-text, formula, clear, and rich-text link command shapes and a page expression that reads the live
session from that page. It must not store or print sid, token, or ouid.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


WRAP_OPCODE = 21299578
RICH_WRAP_OPCODE = 25813757
SET_OPCODE = 132274236
CLEAR_OPCODE = 132274237
RICH_SET_OPCODE = 125982780
RICH_SET_FLAG = 6291459
LINK_COLOR = 1136076
RICH_PREFIX_CODE = 67108350
BIND_ONLY_PARAMS = ("VER", "lsq", "u", "gsi", "cimpl", "RID", "CVER", "zx", "t", "MODE")
SECRET_PARAMS = ("id", "sid", "token", "ouid")


class PageSaveUnsupported(ValueError):
    """Raised when a cell needs a command this channel cannot express."""


def column_index(column: str) -> int:
    text = column.strip().upper()
    if not text.isalpha():
        raise ValueError(f"invalid column: {column}")
    index = 0
    for char in text:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def cell_range(gid: str, row: int, column: str) -> list[Any]:
    if not str(gid).isdigit():
        raise ValueError("gid must be numeric")
    if row < 1:
        raise ValueError("row must be 1-based")
    start_column = column_index(column)
    start_row = row - 1
    return [str(gid), start_row, start_row + 1, start_column, start_column + 1]


def set_string_command(gid: str, row: int, column: str, text: str) -> list[Any]:
    if not isinstance(text, str) or text == "":
        raise ValueError("text must be a non-empty string; use clear_command to erase")
    return [
        cell_range(gid, row, column),
        [SET_OPCODE, 3, [2, text], None, None, 0],
        [None, [[None, 513, [0], None, None, None, None, None, None, None, None, 0]]],
    ]


def clear_command(gid: str, row: int, column: str) -> list[Any]:
    return [cell_range(gid, row, column), [CLEAR_OPCODE], []]


def link_format() -> list[Any]:
    return [None, [2, LINK_COLOR], None, None, None, None, None, None, 1]


def normalize_links(links: list[Any]) -> list[dict[str, str]]:
    if not isinstance(links, list):
        raise ValueError("links must be a list of {text, url}")
    normalized: list[dict[str, str]] = []
    for item in links:
        if not isinstance(item, dict):
            raise ValueError("each link must be an object with text and url")
        label = item.get("text")
        url = item.get("url")
        if not isinstance(label, str) or label == "":
            raise ValueError("link text must be a non-empty string")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ValueError("link url must start with http:// or https://")
        normalized.append({"text": label, "url": url})
    return normalized


def locate_link_spans(text: str, links: list[dict[str, str]]) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    cursor = 0
    for link in links:
        label = link["text"]
        start = text.find(label, cursor)
        if start < 0:
            earlier = text.find(label)
            if (
                earlier >= 0
                and spans
                and earlier < spans[-1][1]
                and earlier + len(label) > spans[-1][0]
            ):
                raise ValueError("link labels overlap")
            raise ValueError(f"link label not found: {label}")
        end = start + len(label)
        if spans and start < spans[-1][1]:
            raise ValueError("link labels overlap")
        spans.append((start, end, link["url"]))
        cursor = end
    return spans


def rich_text_command(gid: str, row: int, column: str, text: str, links: list[Any]) -> list[Any]:
    if not isinstance(text, str) or text == "":
        raise ValueError("text must be a non-empty string")
    if text.startswith("="):
        raise PageSaveUnsupported("公式不能带富文本链接；单个 HYPERLINK 继续用纯公式命令")
    normalized = normalize_links(links)
    if not normalized:
        raise ValueError("rich text requires at least one link")
    spans = locate_link_spans(text, normalized)
    format_runs: list[Any] = []
    link_runs: list[Any] = []
    for start, end, url in spans:
        format_runs.extend([[start, link_format()], [end]])
        link_runs.extend([[start, url], [end]])
    mutation: list[Any] = [None] * 27
    mutation[0] = RICH_SET_OPCODE
    mutation[1] = RICH_SET_FLAG
    mutation[2] = [2, text]
    mutation[5] = 0
    mutation[25] = format_runs
    mutation[26] = link_runs
    return [
        cell_range(gid, row, column),
        mutation,
        [None, [[RICH_PREFIX_CODE, 513, [0], None, None, None, None, None, None, None, None, 0]]],
    ]


def build_command(gid: str, row: int, column: str, text: str | None, *, links: list[Any] | None = None) -> list[Any]:
    if links:
        if text is None:
            raise ValueError("clear cannot carry links")
        return rich_text_command(gid, row, column, text, links)
    if text is None:
        return clear_command(gid, row, column)
    return set_string_command(gid, row, column, text)


def wrap_opcode_for(command: list[Any]) -> int:
    mutation = command[1] if len(command) > 1 and isinstance(command[1], list) else None
    if mutation and mutation[0] == RICH_SET_OPCODE:
        return RICH_WRAP_OPCODE
    return WRAP_OPCODE


def dump_command(command: list[Any]) -> str:
    return json.dumps(command, ensure_ascii=False, separators=(",", ":"))


def wrap_command(command: list[Any]) -> list[Any]:
    return [wrap_opcode_for(command), dump_command(command)]


def save_url_from_resource(resource_url: str) -> str:
    parts = urlsplit(resource_url)
    path = parts.path
    if path.endswith("/bind"):
        path = path[: -len("/bind")] + "/save"
    elif not path.endswith("/save"):
        raise ValueError("resource url must be a sheet /bind or /save url")
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key not in BIND_ONLY_PARAMS
    ]
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), ""))


def redact_resource_url(resource_url: str) -> str:
    parts = urlsplit(resource_url)
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key.lower() in SECRET_PARAMS:
            value = "[redacted]"
        query.append((key, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))


def parse_save_response(body: str) -> dict[str, Any]:
    raw = body.lstrip()
    if raw.startswith(")]}'"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": False, "error": "unparsed response"}
    if not isinstance(payload, dict):
        return {"ok": False, "error": "response is not an object"}
    ranges = payload.get("revisionRanges") or []
    new_revision = None
    if ranges and isinstance(ranges[0], list) and len(ranges[0]) >= 2:
        new_revision = ranges[0][1]
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    return {
        "ok": new_revision is not None,
        "server_revision": metadata.get("serverRevision"),
        "new_revision": new_revision,
    }


def page_post_expression(command: list[Any], revision: int, req_id: int) -> str:
    if revision < 0 or req_id < 0:
        raise ValueError("revision and req_id must be non-negative")
    encoded = dump_command(command)
    wrap_opcode = wrap_opcode_for(command)
    template = r"""(() => new Promise((resolve) => {
  try {
    const command = __COMMAND__;
    const source = performance.getEntriesByType("resource").map((entry) => entry.name).filter((name) => /\/(bind|save)(\?|$)/.test(name)).pop();
    if (!source) { resolve({ ok: false, error: "missing bind or save url" }); return; }
    const url = new URL(source);
    url.pathname = url.pathname.replace(/\/(bind|save)$/, "/save");
    for (const key of ["VER", "lsq", "u", "gsi", "cimpl", "RID", "CVER", "zx", "t", "MODE"]) url.searchParams.delete(key);
    const sid = url.searchParams.get("sid");
    if (!sid) { resolve({ ok: false, error: "missing sid" }); return; }
    const body = new FormData();
    body.set("rev", "__REV__");
    body.set("bundles", JSON.stringify([{ commands: [[__WRAP__, JSON.stringify(command)]], sid, reqId: __REQ__ }]));
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url.toString());
    xhr.setRequestHeader("X-Same-Domain", "1");
    const prefix = ")]}'";
    xhr.onloadend = () => {
      let raw = String(xhr.responseText || "");
      if (raw.startsWith(prefix)) raw = raw.slice(prefix.length).replace(/^\n/, "");
      try {
        const parsed = JSON.parse(raw);
        const ranges = parsed.revisionRanges || [];
        const metadata = parsed.metadata || {};
        resolve({
          ok: xhr.status >= 200 && xhr.status < 300 && ranges.length > 0,
          status: xhr.status,
          serverRevision: metadata.serverRevision ?? null,
          newRevision: ranges.length ? ranges[0][1] : null
        });
      } catch (error) {
        resolve({ ok: false, status: xhr.status, error: "unparsed response" });
      }
    };
    xhr.onerror = () => resolve({ ok: false, error: "xhr error" });
    xhr.send(body);
  } catch (error) {
    resolve({ ok: false, error: String(error).slice(0, 160) });
  }
}))()"""
    return (
        template.replace("__REV__", repr(int(revision)))
        .replace("__REQ__", str(int(req_id)))
        .replace("__WRAP__", str(wrap_opcode))
        .replace("__COMMAND__", encoded)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    command = sub.add_parser("command")
    command.add_argument("--gid", required=True)
    command.add_argument("--row", type=int, required=True)
    command.add_argument("--column", required=True)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--text")
    mode.add_argument("--clear", action="store_true")
    command.add_argument("--links-json", help="JSON list of {text, url} short labels")
    expression = sub.add_parser("expression")
    expression.add_argument("--gid", required=True)
    expression.add_argument("--row", type=int, required=True)
    expression.add_argument("--column", required=True)
    expression.add_argument("--rev", type=int, required=True)
    expression.add_argument("--req-id", type=int, required=True)
    mode = expression.add_mutually_exclusive_group(required=True)
    mode.add_argument("--text")
    mode.add_argument("--clear", action="store_true")
    expression.add_argument("--links-json", help="JSON list of {text, url} short labels")
    args = parser.parse_args()
    text = None if args.clear else args.text
    links = json.loads(args.links_json) if args.links_json else None
    try:
        built = build_command(args.gid, args.row, args.column, text, links=links)
    except (PageSaveUnsupported, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.action == "command":
        print(dump_command(built))
        return 0
    print(page_post_expression(built, args.rev, args.req_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
