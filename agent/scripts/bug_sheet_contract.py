#!/usr/bin/env python3
"""机械化生成和校验 bug 表写入契约。

这个脚本只处理稳定、重复的表格层动作：B 列 HYPERLINK 公式、十列行结构、
C/D/H/J 富文本链接、BOOLEAN 复选框、已有行列级更新、格式复制、自动行高、
筛选边界和回读校验。

它不读取 Jira，不判断产品口径，不解释评论，不调用 Google API，也不替代
Alchemy/Drive 证据判断。输入应先由人工或上层流程整理成 JSON。`build` 只用于
追加新行；`patch` 用于更新已有 Bug，并按普通二次复查或会议复盘模式限制列范围。

build 示例：
    python3 agent/scripts/bug_sheet_contract.py build \
      --sheet-id 149420397 --start-row-index 11 < rows.json > requests.json

validate 示例：
    python3 agent/scripts/bug_sheet_contract.py validate < readback.json

snapshot / patch 示例：
    python3 agent/scripts/bug_sheet_contract.py snapshot < current-row.json
    python3 agent/scripts/bug_sheet_contract.py patch \
      --sheet-id 2135747181 --row-index 144 --key ADS-47039 \
      --mode recheck --expected-fingerprint <fingerprint> < patch.json

rows.json 是一个对象数组，每项至少包含 key、summary、info、judgment、status、
note；可选 date、owner_judgment、review_judgment、links、info_links、
judgment_links、review_links。链接数组元素统一为 {"label": "...", "url": "..."}。
旧字段 wu_you 继续兼容。

patch.json 包含 `current_row` 和 `changes`。`changes` 使用列字母作为 key：
C/D/H 为 `{"text": "...", "links": [...]}`，G/I 为字符串，J 为
`{"links": [...]}`。`recheck` 只允许 C/D/G/I/J；`review` 只允许 G/H/I/J。
"""

from __future__ import annotations

import argparse
import hashlib
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

COLUMN_INDEX = {chr(ord("A") + index): index for index in range(len(COLUMNS))}
PATCH_ALLOWED_COLUMNS = {
    "recheck": frozenset(("C", "D", "G", "I", "J")),
    "review": frozenset(("G", "H", "I", "J")),
}
RICH_TEXT_COLUMNS = frozenset(("C", "D", "H", "J"))


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


def _one_row(payload: Any) -> dict[str, Any]:
    """Return exactly one A:J row from a row object or readback payload."""

    if isinstance(payload, dict) and isinstance(payload.get("values"), list):
        row = payload
    else:
        rows = _readback_rows(payload)
        if len(rows) != 1:
            raise ValueError(f"已有行操作必须精确回读 1 行，实际 {len(rows)} 行")
        row = rows[0]
    if len(row.get("values", [])) != len(COLUMNS):
        raise ValueError(
            f"已有行必须包含完整 A:J，实际 {len(row.get('values', []))} 列"
        )
    return row


def _cell_write_state(cell: dict[str, Any]) -> dict[str, Any]:
    """Return fields that must not change when a column is protected."""

    return {
        key: cell[key]
        for key in ("userEnteredValue", "textFormatRuns", "dataValidation")
        if key in cell
    }


def row_fingerprint(payload: Any) -> str:
    """Fingerprint writable A:J state for a fresh-read precondition."""

    row = _one_row(payload)
    state = [_cell_write_state(cell) for cell in row["values"]]
    encoded = json.dumps(
        state,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _visible_text(cell: dict[str, Any]) -> str:
    if "formattedValue" in cell:
        return str(cell["formattedValue"])
    effective = cell.get("effectiveValue", {})
    for key in ("stringValue", "numberValue", "boolValue"):
        if key in effective:
            return str(effective[key])
    entered = cell.get("userEnteredValue", {})
    for key in ("stringValue", "formulaValue", "numberValue", "boolValue"):
        if key in entered:
            return str(entered[key])
    return ""


def _link_uris(cell: dict[str, Any]) -> list[str]:
    return [
        str(uri)
        for run in cell.get("textFormatRuns", [])
        if (uri := run.get("format", {}).get("link", {}).get("uri"))
    ]


def _patch_cell(column: str, spec: Any) -> tuple[dict[str, Any], str, list[str]]:
    """Build one target cell plus its expected visible text and link targets."""

    if column in ("G", "I"):
        if not isinstance(spec, str):
            raise ValueError(f"{column} 列变更必须是字符串")
        return _cell(spec), spec, []

    if not isinstance(spec, dict):
        raise ValueError(f"{column} 列变更必须是对象")
    if column == "J":
        links = _normalize_links(spec.get("links"))
        cell = link_list_cell(links)
        return cell, "\n".join(link["label"] for link in links), [
            link["url"] for link in links
        ]

    if "text" not in spec:
        raise ValueError(f"{column} 列变更缺少 text")
    text = str(spec["text"])
    links = _normalize_links(spec.get("links"))
    return rich_text_cell(text, links), text, [link["url"] for link in links]


def build_patch_requests(
    sheet_id: int,
    row_index: int,
    key: str,
    mode: str,
    current_row: Any,
    expected_fingerprint: str,
    changes: dict[str, Any],
) -> dict[str, Any]:
    """Build column-scoped requests for one existing Bug row."""

    if mode not in PATCH_ALLOWED_COLUMNS:
        raise ValueError(f"未知更新模式：{mode}")
    if row_index < 1:
        raise ValueError("row_index 必须指向数据行，不能是表头")
    row = _one_row(current_row)
    actual_fingerprint = row_fingerprint(row)
    if not expected_fingerprint or actual_fingerprint != expected_fingerprint:
        raise ValueError(
            "写前 A:J 已变化或缺少有效 fingerprint；停止生成更新请求并重新回读"
        )

    b_text = _visible_text(row["values"][COLUMN_INDEX["B"]])
    if not (b_text.startswith(f"{key}｜") or b_text.startswith(f"{key}|")):
        raise ValueError(f"B 列 Jira Key 不匹配：实际 {b_text!r}，预期 {key}")
    if not isinstance(changes, dict) or not changes:
        raise ValueError("changes 必须包含至少一个目标列")

    columns = set(changes)
    unknown = columns - set(COLUMN_INDEX)
    if unknown:
        raise ValueError(f"存在未知列：{','.join(sorted(unknown))}")
    forbidden = columns - PATCH_ALLOWED_COLUMNS[mode]
    if forbidden:
        raise ValueError(
            f"{mode} 模式禁止修改列：{','.join(sorted(forbidden))}"
        )

    requests: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    expected_after: dict[str, dict[str, Any]] = {}
    for column in sorted(columns, key=COLUMN_INDEX.__getitem__):
        column_index = COLUMN_INDEX[column]
        cell, visible, uris = _patch_cell(column, changes[column])
        fields = "userEnteredValue,textFormatRuns" if column in RICH_TEXT_COLUMNS else "userEnteredValue"
        requests.append(
            {
                "updateCells": {
                    "start": {
                        "sheetId": sheet_id,
                        "rowIndex": row_index,
                        "columnIndex": column_index,
                    },
                    "rows": [{"values": [cell]}],
                    "fields": fields,
                }
            }
        )
        manifest.append(
            {
                "column": column,
                "before": _visible_text(row["values"][column_index]),
                "after": visible,
                "links": uris,
            }
        )
        expected_after[column] = {"visible": visible, "links": uris}

    return {
        "key": key,
        "mode": mode,
        "sheetId": sheet_id,
        "rowIndex": row_index,
        "beforeFingerprint": actual_fingerprint,
        "changedColumns": [
            item["column"] for item in manifest
        ],
        "manifest": manifest,
        "expectedAfter": expected_after,
        "requests": requests,
    }


def validate_patch_readback(
    before_row: Any,
    after_row: Any,
    key: str,
    mode: str,
    changes: dict[str, Any],
) -> list[str]:
    """Validate target cells and prove every unsubmitted column stayed unchanged."""

    errors: list[str] = []
    if mode not in PATCH_ALLOWED_COLUMNS:
        return [f"未知更新模式：{mode}"]
    before = _one_row(before_row)
    after = _one_row(after_row)
    changed_columns = set(changes)

    b_text = _visible_text(after["values"][COLUMN_INDEX["B"]])
    if not (b_text.startswith(f"{key}｜") or b_text.startswith(f"{key}|")):
        errors.append(f"B 列 Jira Key 不匹配：{b_text!r}")

    forbidden = changed_columns - PATCH_ALLOWED_COLUMNS[mode]
    if forbidden:
        errors.append(f"{mode} 模式出现禁止列：{','.join(sorted(forbidden))}")

    for column, column_index in COLUMN_INDEX.items():
        before_cell = before["values"][column_index]
        after_cell = after["values"][column_index]
        if column not in changed_columns:
            if _cell_write_state(before_cell) != _cell_write_state(after_cell):
                errors.append(f"{column} 列未声明修改但写后发生变化")
            continue

        try:
            _cell_data, expected_visible, expected_links = _patch_cell(
                column, changes[column]
            )
        except ValueError as exc:
            errors.append(str(exc))
            continue
        actual_visible = _visible_text(after_cell)
        if actual_visible != expected_visible:
            errors.append(
                f"{column} 列可见文本不符：实际 {actual_visible!r}，预期 {expected_visible!r}"
            )
        if column in RICH_TEXT_COLUMNS and _link_uris(after_cell) != expected_links:
            errors.append(
                f"{column} 列链接目标不符：实际 {_link_uris(after_cell)!r}，"
                f"预期 {expected_links!r}"
            )

    return errors


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
                "fields": "userEnteredValue,textFormatRuns",
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

    sub.add_parser("snapshot", help="读取完整 A:J 后生成写前 fingerprint")

    patch = sub.add_parser("patch", help="为已有 Bug 生成列级定向更新请求")
    patch.add_argument("--sheet-id", type=int, required=True)
    patch.add_argument("--row-index", type=int, required=True)
    patch.add_argument("--key", required=True)
    patch.add_argument("--mode", choices=sorted(PATCH_ALLOWED_COLUMNS), required=True)
    patch.add_argument("--expected-fingerprint", required=True)

    validate_patch = sub.add_parser("validate-patch", help="校验已有 Bug 列级更新回读")
    validate_patch.add_argument("--key", required=True)
    validate_patch.add_argument(
        "--mode", choices=sorted(PATCH_ALLOWED_COLUMNS), required=True
    )

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

    if args.command == "snapshot":
        json.dump(
            {"fingerprint": row_fingerprint(payload)},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    if args.command == "patch":
        if not isinstance(payload, dict):
            parser.error("patch 输入必须是 JSON 对象")
        result = build_patch_requests(
            args.sheet_id,
            args.row_index,
            args.key,
            args.mode,
            payload.get("current_row"),
            args.expected_fingerprint,
            payload.get("changes"),
        )
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    if args.command == "validate-patch":
        if not isinstance(payload, dict):
            parser.error("validate-patch 输入必须是 JSON 对象")
        errors = validate_patch_readback(
            payload.get("before_row"),
            payload.get("after_row"),
            args.key,
            args.mode,
            payload.get("changes"),
        )
        json.dump({"ok": not errors, "errors": errors}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0 if not errors else 1

    errors = validate_readback(payload, expected_keys=args.expected_keys or None)
    json.dump({"ok": not errors, "errors": errors}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
