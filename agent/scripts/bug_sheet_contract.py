#!/usr/bin/env python3
"""机械化生成和校验 bug 表写入契约。

这个脚本只处理稳定、重复的表格层动作：B 列 HYPERLINK 公式、十列行结构、
C/D/H/J 富文本链接、BOOLEAN 复选框、格式复制、自动行高、筛选边界和回读校验。

它不读取 Jira，不判断产品口径，不解释评论，不调用 Google API，也不替代
Alchemy/Drive 证据判断。输入应先由人工或上层流程整理成 JSON。本脚本的 build
只用于追加新行；更新已有 Bug 必须做列级定向写入，不能用整行 payload 覆盖 F/H。

build 示例：
    python3 agent/scripts/bug_sheet_contract.py build \
      --sheet-id 149420397 --start-row-index 11 < rows.json > requests.json

validate 示例：
    python3 agent/scripts/bug_sheet_contract.py validate < readback.json

rows.json 是一个对象数组，每项至少包含 key、summary、info、judgment、status、
note；可选 date、owner_judgment、review_judgment、links、info_links、
judgment_links、review_links。链接数组元素统一为 {"label": "...", "url": "..."}。
旧字段 wu_you 继续兼容。
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


COLUMNS = (
    "日期",
    "问题jira链接+摘要",
    "收集到的信息",
    "产品Agent判断",
    "准确率标注",
    "负责人判断",
    "状态",
    "复盘后的产品Agent判断",
    "备注",
    "相关文档",
)


def _formula_text(value: str) -> str:
    return value.replace('"', '""')


def hyperlink(url: str, label: str) -> str:
    """Return one Sheets HYPERLINK formula without concatenation."""

    return f'=HYPERLINK("{_formula_text(url)}","{_formula_text(label)}")'


def _cell(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        return {"userEnteredValue": {"boolValue": value}}
    if value is None or value == "":
        return {}
    if isinstance(value, str) and value.startswith("="):
        return {"userEnteredValue": {"formulaValue": value}}
    return {"userEnteredValue": {"stringValue": str(value)}}


def _normalize_links(links: Any) -> list[dict[str, str]]:
    if links is None:
        return []
    if not isinstance(links, list):
        raise ValueError("links 必须是对象数组")

    normalized: list[dict[str, str]] = []
    for link in links:
        if not isinstance(link, dict) or not link.get("label") or not link.get("url"):
            raise ValueError("每个链接必须包含非空 label 和 url")
        normalized.append({"label": str(link["label"]), "url": str(link["url"])})
    return normalized


def rich_text_cell(text: str, links: Any) -> dict[str, Any]:
    """Return a string cell with independent link runs on named labels."""

    normalized = _normalize_links(links)
    if not normalized:
        return _cell(text)

    runs: list[dict[str, Any]] = [{}]
    cursor = 0
    for link in normalized:
        label = link["label"]
        start_char = text.find(label, cursor)
        if start_char < 0:
            raise ValueError(f"链接标签未出现在文本中或顺序不一致：{label}")
        end_char = start_char + len(label)
        start = len(text[:start_char].encode("utf-16-le")) // 2
        end = len(text[:end_char].encode("utf-16-le")) // 2
        runs.append(
            {
                "startIndex": start,
                "format": {
                    "foregroundColor": {"red": 0.0667, "green": 0.3333, "blue": 0.8},
                    "underline": True,
                    "link": {"uri": link["url"]},
                },
            }
        )
        if end_char < len(text):
            runs.append({"startIndex": end})
        cursor = end_char

    return {
        "userEnteredValue": {"stringValue": text},
        "textFormatRuns": runs,
    }


def link_list_cell(links: Any) -> dict[str, Any]:
    """Return one J cell with one clickable short label per line."""

    normalized = _normalize_links(links)
    if not normalized:
        raise ValueError("J 列至少需要一个原始入口")
    text = "\n".join(link["label"] for link in normalized)
    return rich_text_cell(text, normalized)


def build_row(item: dict[str, Any], date: str = "") -> list[dict[str, Any]]:
    """Convert one human-reviewed bug object into the fixed A:J cell payload."""

    key = str(item["key"])
    summary = str(item["summary"])
    jira_url = str(item.get("jira_url") or f"http://jira.i-tetris.com/browse/{key}")
    links = item.get("links") or [{"label": "Jira原票", "url": jira_url}]

    return [
        _cell(item.get("date") or date),
        _cell(hyperlink(jira_url, f"{key}｜{summary}")),
        rich_text_cell(str(item["info"]), item.get("info_links")),
        rich_text_cell(str(item["judgment"]), item.get("judgment_links")),
        _cell(False),
        _cell(item.get("owner_judgment", item.get("wu_you", ""))),
        _cell(item["status"]),
        rich_text_cell(
            str(item.get("review_judgment", "")),
            item.get("review_links"),
        ),
        _cell(item["note"]),
        link_list_cell(links),
    ]


def build_batch_requests(
    sheet_id: int,
    start_row_index: int,
    items: list[dict[str, Any]],
    *,
    date: str = "",
    format_source_row_index: int = 1,
    filter_end_row_index: int | None = None,
) -> list[dict[str, Any]]:
    """Build Sheets batchUpdate requests for appending one new bug block."""

    rows = [build_row(item, date=date) for item in items]
    end_row_index = start_row_index + len(rows)
    filter_end = filter_end_row_index or end_row_index
    return [
        {
            "updateCells": {
                "start": {"sheetId": sheet_id, "rowIndex": start_row_index, "columnIndex": 0},
                "rows": [{"values": row} for row in rows],
                "fields": "userEnteredValue",
            }
        },
        {
            "copyPaste": {
                "source": {
                    "sheetId": sheet_id,
                    "startRowIndex": format_source_row_index,
                    "endRowIndex": format_source_row_index + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 10,
                },
                "destination": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index,
                    "startColumnIndex": 0,
                    "endColumnIndex": 10,
                },
                "pasteType": "PASTE_FORMAT",
            }
        },
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5,
                },
                "rule": {
                    "condition": {"type": "BOOLEAN"},
                    "strict": True,
                    "showCustomUi": True,
                },
            }
        },
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": start_row_index,
                    "endIndex": end_row_index,
                }
            }
        },
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": filter_end,
                        "startColumnIndex": 0,
                        "endColumnIndex": 10,
                    }
                }
            }
        },
    ]


def _readback_rows(payload: Any) -> list[dict[str, Any]]:
    """Accept common get_spreadsheet_cells response fragments."""

    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("rowData"), list):
        return payload["rowData"]
    if isinstance(payload, dict):
        for sheet in payload.get("sheets", []):
            for data in sheet.get("data", []):
                if isinstance(data.get("rowData"), list):
                    return data["rowData"]
    raise ValueError("readback JSON 中找不到 rowData")


def validate_readback(payload: Any, expected_keys: list[str] | None = None) -> list[str]:
    """Return all structural/formula/checkbox errors; an empty list means pass."""

    errors: list[str] = []
    rows = _readback_rows(payload)
    if expected_keys and len(rows) != len(expected_keys):
        errors.append(f"行数不符：实际 {len(rows)}，预期 {len(expected_keys)}")

    for index, row in enumerate(rows):
        cells = row.get("values", [])
        label = f"第{index + 1}行"
        if len(cells) != 10:
            errors.append(f"{label}列数为 {len(cells)}，不是 10")
            continue

        key = cells[1].get("effectiveValue", {}).get("stringValue")
        if expected_keys and index < len(expected_keys) and not str(key or "").startswith(
            expected_keys[index] + "｜"
        ):
            errors.append(f"{label} key 错位：{key!r}，预期 {expected_keys[index]}")

        if not cells[1].get("userEnteredValue", {}).get("formulaValue", "").startswith(
            "=HYPERLINK("
        ):
            errors.append(f"{label} B列不是 HYPERLINK 公式")

        e_value = cells[4].get("effectiveValue", {})
        if e_value.get("boolValue") is not False:
            errors.append(f"{label} E列不是 FALSE BOOLEAN")
        if cells[4].get("dataValidation", {}).get("condition", {}).get("type") != "BOOLEAN":
            errors.append(f"{label} E列缺 BOOLEAN 校验")

        j_cell = cells[9]
        if j_cell.get("effectiveValue", {}).get("errorValue"):
            errors.append(f"{label} J列出现公式错误")
        j_formula = j_cell.get("userEnteredValue", {}).get("formulaValue", "")
        j_text = j_cell.get("userEnteredValue", {}).get("stringValue", "")
        j_runs = j_cell.get("textFormatRuns", [])
        has_formula_links = j_formula.startswith("=HYPERLINK(")
        has_rich_links = bool(j_text) and any(
            run.get("format", {}).get("link", {}).get("uri") for run in j_runs
        )
        if not (has_formula_links or has_rich_links):
            errors.append(f"{label} J列既不是 HYPERLINK 公式，也没有富文本链接")
        if j_formula and '&' in j_formula:
            errors.append(f"{label} J列使用了禁止的多 HYPERLINK 拼接")

        for column_index, column_name in ((2, "C"), (3, "D"), (7, "H"), (9, "J")):
            visible = cells[column_index].get("formattedValue", "")
            if "http://" in visible or "https://" in visible:
                errors.append(f"{label} {column_name}列显示了原始长 URL")

    return errors


def _load_json(stream: Any) -> Any:
    return json.load(stream)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="从人工审核后的 bug JSON 生成 Sheets requests")
    build.add_argument("--sheet-id", type=int, required=True)
    build.add_argument("--start-row-index", type=int, required=True)
    build.add_argument("--date", default="")
    build.add_argument("--format-source-row-index", type=int, default=1)
    build.add_argument("--filter-end-row-index", type=int)

    validate = sub.add_parser("validate", help="校验 get_spreadsheet_cells 回读 JSON")
    validate.add_argument("--expected-keys", nargs="*")

    args = parser.parse_args(argv)
    payload = _load_json(sys.stdin)

    if args.command == "build":
        if not isinstance(payload, list):
            parser.error("build 输入必须是 JSON 数组")
        requests = build_batch_requests(
            args.sheet_id,
            args.start_row_index,
            payload,
            date=args.date,
            format_source_row_index=args.format_source_row_index,
            filter_end_row_index=args.filter_end_row_index,
        )
        json.dump({"requests": requests}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    errors = validate_readback(payload, expected_keys=args.expected_keys or None)
    json.dump({"ok": not errors, "errors": errors}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
