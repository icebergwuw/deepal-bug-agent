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
      --sheet-id 149420397 --start-row-index 11 --owner-id li-xin \
      --manifest ADS-TEST-manifest.json < rows.json > requests.json

validate 示例：
    python3 agent/scripts/bug_sheet_contract.py validate < readback.json

validate-append 示例：
    python3 agent/scripts/bug_sheet_contract.py validate-append \
      < append-readback-bundle.json

snapshot / patch 示例：
    python3 agent/scripts/bug_sheet_contract.py snapshot < current-row.json
    python3 agent/scripts/bug_sheet_contract.py patch \
      --sheet-id 2135747181 --row-number 145 --key ADS-47039 \
      --owner-id wu-you \
      --mode recheck --preview-fingerprint <fingerprint> \
      --manifest ADS-47039-manifest.json < patch.json

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
import re
import sys
from pathlib import Path
from typing import Any

from bug_project_preflight import (
    PLATFORMS,
    assess,
    load_owners,
    load_profile,
    skill_status,
)
from validate_bug_evidence_gate import validate_manifest
from validate_bug_run import validate_run_bundle
from urllib.parse import urlparse


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
RICH_TEXT_COLUMNS = frozenset(("C", "D", "H", "J"))
DEFAULT_FORMAT_ANCHOR_ROW = 107
DEFAULT_FORMAT_ANCHOR_ROW_INDEX = DEFAULT_FORMAT_ANCHOR_ROW - 1
UPDATE_MODES_PATH = (
    Path(__file__).resolve().parents[1] / "config/sheet-update-modes.json"
)


def _load_update_modes() -> dict[str, dict[str, Any]]:
    payload = json.loads(UPDATE_MODES_PATH.read_text(encoding="utf-8"))
    modes = payload.get("modes")
    if payload.get("schema_version") != 1 or not isinstance(modes, dict) or not modes:
        raise RuntimeError("sheet-update-modes.json 结构无效")

    expected = set(COLUMN_INDEX)
    for mode, spec in modes.items():
        allowed = set(spec.get("allowed_columns", []))
        protected = set(spec.get("protected_columns", []))
        if not allowed or allowed & protected or allowed | protected != expected:
            raise RuntimeError(f"更新模式 {mode} 未完整且互斥地覆盖 A:J")
    return modes


UPDATE_MODES = _load_update_modes()
PATCH_ALLOWED_COLUMNS = {
    mode: frozenset(spec["allowed_columns"]) for mode, spec in UPDATE_MODES.items()
}
PATCH_PROTECTED_COLUMNS = {
    mode: frozenset(spec["protected_columns"]) for mode, spec in UPDATE_MODES.items()
}


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
        label = str(link["label"])
        url = str(link["url"])
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"链接不是可访问的 http(s) 原始入口：{label}")
        normalized.append({"label": label, "url": url})
    return normalized


def rich_text_cell(text: str, links: Any) -> dict[str, Any]:
    """Return a string cell with independent link runs on named labels."""

    if "http://" in text or "https://" in text:
        raise ValueError("C/D/H/J 可见文本不得显示原始长 URL")
    normalized = _normalize_links(links)
    if not normalized:
        return _cell(text)

    runs: list[dict[str, Any]] = []
    cursor = 0
    for link in normalized:
        label = link["label"]
        start_char = text.find(label, cursor)
        if start_char < 0:
            raise ValueError(f"链接标签未出现在文本中或顺序不一致：{label}")
        end_char = start_char + len(label)
        start = len(text[:start_char].encode("utf-16-le")) // 2
        end = len(text[:end_char].encode("utf-16-le")) // 2
        # At position 0, a default run would overlap the link run. Sheets
        # expands that overlap into duplicate link targets on readback.
        if not runs and start > 0:
            runs.append({})
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
    # Google Sheets drops a lone rich-text run that spans the entire cell.
    # A single source must therefore use its native HYPERLINK formula; multiple
    # sources remain rich text so every short label can carry its own URL.
    if len(normalized) == 1:
        link = normalized[0]
        return _cell(hyperlink(link["url"], link["label"]))
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
    formula = str(entered.get("formulaValue", ""))
    hyperlink = re.match(
        r'^=HYPERLINK\("[^"]+"\s*,\s*"((?:[^"]|"")*)"\)$',
        formula,
        flags=re.IGNORECASE,
    )
    if hyperlink:
        return hyperlink.group(1).replace('""', '"')
    for key in ("stringValue", "formulaValue", "numberValue", "boolValue"):
        if key in entered:
            return str(entered[key])
    return ""


def _link_uris(cell: dict[str, Any]) -> list[str]:
    rich_uris = [
        str(uri)
        for run in cell.get("textFormatRuns", [])
        if (uri := run.get("format", {}).get("link", {}).get("uri"))
    ]
    if rich_uris:
        return rich_uris
    formula = str(cell.get("userEnteredValue", {}).get("formulaValue", ""))
    match = re.match(r'^=HYPERLINK\("([^"]+)"\s*,', formula, flags=re.IGNORECASE)
    return [match.group(1)] if match else []


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
    row_number: int,
    key: str,
    mode: str,
    current_row: Any,
    preview_fingerprint: str,
    changes: dict[str, Any],
) -> dict[str, Any]:
    """Build column-scoped requests from a fresh A:J read of one existing row."""

    if mode not in PATCH_ALLOWED_COLUMNS:
        raise ValueError(f"未知更新模式：{mode}")
    if row_number < 2:
        raise ValueError("row_number 使用表格可见行号，必须指向第 2 行及之后的数据行")
    row_index = row_number - 1
    row = _one_row(current_row)
    actual_fingerprint = row_fingerprint(row)
    if not preview_fingerprint or actual_fingerprint != preview_fingerprint:
        raise ValueError(
            "预览后 A:J 已变化或缺少有效 fingerprint；停止生成更新请求并重新回读"
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
        "sheetRow": row_number,
        "rowIndex": row_index,
        "previewFingerprint": actual_fingerprint,
        "freshReadRequiredImmediatelyBeforeBatchUpdate": True,
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
    format_source_row_index: int = DEFAULT_FORMAT_ANCHOR_ROW_INDEX,
    filter_end_row_index: int | None = None,
) -> list[dict[str, Any]]:
    """Build Sheets batchUpdate requests for appending one new bug block."""

    rows = [build_row(item, date=date) for item in items]
    end_row_index = start_row_index + len(rows)
    filter_end = filter_end_row_index or end_row_index
    return [
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
            "updateCells": {
                "start": {
                    "sheetId": sheet_id,
                    "rowIndex": start_row_index,
                    "columnIndex": 0,
                },
                "rows": [{"values": row} for row in rows],
                "fields": "userEnteredValue,textFormatRuns",
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


def resolve_format_source_row_index(
    owner_id: str,
    requested_index: int | None,
    owners: dict[str, dict[str, Any]] | None = None,
) -> int:
    """Return the registered fixed format anchor and reject caller overrides."""

    owner = (owners or load_owners()).get(owner_id)
    if not owner:
        raise ValueError(f"负责人未登记：{owner_id}")
    configured = owner.get("format_anchor_row")
    if configured is None:
        return 1 if requested_index is None else requested_index
    try:
        anchor_row = int(configured)
    except (TypeError, ValueError) as error:
        raise ValueError(f"负责人 {owner_id} 的 format_anchor_row 无效") from error
    if anchor_row < 2:
        raise ValueError(f"负责人 {owner_id} 的 format_anchor_row 不得是表头")
    anchor_index = anchor_row - 1
    if requested_index is not None and requested_index != anchor_index:
        raise ValueError(
            f"负责人 {owner_id} 固定格式锚点为第 {anchor_row} 行"
            f"（索引 {anchor_index}），禁止改用索引 {requested_index}"
        )
    return anchor_index


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


def validate_append_readback(
    payload: Any,
    items: list[dict[str, Any]],
    *,
    date: str = "",
) -> list[str]:
    """Validate every appended A:J value and every expected rich-text link."""

    expected_keys = [str(item["key"]) for item in items]
    errors = validate_readback(payload, expected_keys=expected_keys)
    rows = _readback_rows(payload)
    if len(rows) != len(items):
        return errors

    for row_index, (actual_row, item) in enumerate(zip(rows, items), start=1):
        actual_cells = actual_row.get("values", [])
        if len(actual_cells) != len(COLUMNS):
            continue
        expected_cells = build_row(item, date=date)
        for column_index, column_name in enumerate(COLUMNS):
            actual_entered = actual_cells[column_index].get("userEnteredValue", {})
            expected_entered = expected_cells[column_index].get("userEnteredValue", {})
            if actual_entered != expected_entered:
                errors.append(
                    f"第{row_index}行 {chr(ord('A') + column_index)}列"
                    f"写入值不符：{column_name}"
                )

        for column_index, column_name in ((2, "C"), (3, "D"), (7, "H"), (9, "J")):
            expected_text = _visible_text(expected_cells[column_index])
            actual_text = _visible_text(actual_cells[column_index])
            if actual_text != expected_text:
                errors.append(
                    f"第{row_index}行 {column_name}列可见文本不符："
                    f"实际 {actual_text!r}，预期 {expected_text!r}"
                )

            expected_links = _link_uris(expected_cells[column_index])
            actual_links = _link_uris(actual_cells[column_index])
            if actual_links != expected_links:
                errors.append(
                    f"第{row_index}行 {column_name}列链接目标不符："
                    f"实际 {actual_links!r}，预期 {expected_links!r}"
                )

    return errors


FORMAT_FIELDS = (
    "numberFormat",
    "backgroundColor",
    "borders",
    "padding",
    "horizontalAlignment",
    "verticalAlignment",
    "wrapStrategy",
)
TEXT_FORMAT_FIELDS = (
    "foregroundColor",
    "fontFamily",
    "fontSize",
    "bold",
    "italic",
    "strikethrough",
    "underline",
)


def _fixed_format(cell: dict[str, Any]) -> dict[str, Any]:
    """Extract fixed style fields while excluding content-specific link URIs."""

    value = cell.get("effectiveFormat", {})
    result = {field: value.get(field) for field in FORMAT_FIELDS}
    text_format = value.get("textFormat", {})
    result["textFormat"] = {
        field: text_format.get(field) for field in TEXT_FORMAT_FIELDS
    }
    return result


def validate_append_format(anchor_payload: Any, appended_payload: Any) -> list[str]:
    """Require every appended A:J cell to match the fixed anchor's base style."""

    errors: list[str] = []
    anchor_rows = _readback_rows(anchor_payload)
    rows = _readback_rows(appended_payload)
    if len(anchor_rows) != 1:
        return [f"格式锚点必须精确回读 1 行，实际 {len(anchor_rows)} 行"]
    anchor_cells = anchor_rows[0].get("values", [])
    if len(anchor_cells) != len(COLUMNS):
        return [f"格式锚点列数为 {len(anchor_cells)}，不是 10"]
    for row_index, row in enumerate(rows, start=1):
        cells = row.get("values", [])
        if len(cells) != len(COLUMNS):
            errors.append(f"新增第{row_index}行列数为 {len(cells)}，不是 10")
            continue
        for column_index, (anchor, actual) in enumerate(zip(anchor_cells, cells)):
            if _fixed_format(anchor) != _fixed_format(actual):
                errors.append(
                    f"新增第{row_index}行 {chr(ord('A') + column_index)}列"
                    f"固定格式与第 {DEFAULT_FORMAT_ANCHOR_ROW} 行锚点不一致"
                )
    return errors


def _load_json(stream: Any) -> Any:
    return json.load(stream)


def validate_bound_manifests(
    manifest_paths: list[str], expected_keys: list[str]
) -> list[str]:
    """Validate one schema-v5 evidence manifest for every pending sheet row."""

    errors: list[str] = []
    if len(manifest_paths) != len(expected_keys):
        return [
            "写表请求必须为每个 Jira 绑定一个证据 manifest："
            f"keys={len(expected_keys)} manifests={len(manifest_paths)}"
        ]
    for index, (path_text, expected_key) in enumerate(
        zip(manifest_paths, expected_keys), start=1
    ):
        path = Path(path_text)
        if not path.is_file():
            errors.append(f"第 {index} 个 manifest 不存在：{path}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"第 {index} 个 manifest 无法解析：{error.msg}")
            continue
        manifest_errors = validate_manifest(payload, expected_key)
        errors.extend(
            f"{expected_key} manifest：{error}" for error in manifest_errors
        )
    return errors


def validate_bound_run_bundle(bundle_path: str) -> list[str]:
    """Validate the complete per-run log/manifest binding before any write request."""

    path = Path(bundle_path)
    if not path.is_file():
        return [f"run bundle 不存在：{path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"run bundle 无法解析：{error.msg}"]
    return validate_run_bundle(payload, phase="prewrite")


def required_platforms_for_manifests(manifest_paths: list[str]) -> set[str]:
    """Derive runtime platforms that must be freshly verified before writing."""

    required = {"jira", "google_drive"}
    for path_text in manifest_paths:
        try:
            payload = json.loads(Path(path_text).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if "voice" in payload.get("evidence_profiles", []):
            required.add("alchemy")
    return required


def validate_local_write_gate(
    owner_id: str,
    manifest_paths: list[str],
    extra_platforms: list[str],
) -> list[str]:
    required_platforms = sorted(
        required_platforms_for_manifests(manifest_paths) | set(extra_platforms)
    )
    try:
        profile = load_profile()
        result = assess(
            profile,
            load_owners(),
            required_owner_id=owner_id,
            required_platforms=required_platforms,
            max_access_age_hours=24,
            skill=skill_status(),
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"本机写前预检失败：{error}"]
    if result["ok"]:
        return []
    errors = [f"本机写前预检：{item}" for item in result["blockers"]]
    errors.extend(f"引导：{item}" for item in result["guidance"])
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="从人工审核后的 bug JSON 生成 Sheets requests")
    build.add_argument("--sheet-id", type=int, required=True)
    build.add_argument("--start-row-index", type=int, required=True)
    build.add_argument("--owner-id", required=True)
    build.add_argument("--date", default="")
    build.add_argument(
        "--format-source-row-index",
        type=int,
        help="兼容参数；若负责人已登记固定锚点，只允许传对应的 0-based 索引",
    )
    build.add_argument("--filter-end-row-index", type=int)
    build.add_argument(
        "--manifest",
        action="append",
        required=True,
        help="每个新增 Jira 对应的 schema-v5 manifest；按输入行顺序重复传入",
    )
    build.add_argument("--run-bundle", required=True, help="完整批次 run bundle")
    build.add_argument(
        "--require-platform",
        action="append",
        choices=PLATFORMS,
        default=[],
        help="除manifest自动推导外额外要求的已验证平台",
    )

    validate = sub.add_parser("validate", help="校验 get_spreadsheet_cells 回读 JSON")
    validate.add_argument("--expected-keys", nargs="*")

    validate_append = sub.add_parser(
        "validate-append",
        help="按原始 rows 输入逐格校验新增行和 C/D/H/J 链接",
    )
    validate_append.add_argument("--date", default="")

    sub.add_parser(
        "validate-format",
        help="将新增行完整格式与负责人固定锚点逐列对比",
    )

    sub.add_parser("snapshot", help="读取完整 A:J 后生成写前 fingerprint")

    patch = sub.add_parser("patch", help="为已有 Bug 生成列级定向更新请求")
    patch.add_argument("--sheet-id", type=int, required=True)
    patch.add_argument(
        "--row-number",
        type=int,
        required=True,
        help="Google 表格界面显示的 1-based 行号",
    )
    patch.add_argument("--key", required=True)
    patch.add_argument("--owner-id", required=True)
    patch.add_argument("--mode", choices=sorted(PATCH_ALLOWED_COLUMNS), required=True)
    patch.add_argument(
        "--preview-fingerprint",
        required=True,
        help="预览阶段 snapshot 生成的 fingerprint；current_row 必须在写前重新回读",
    )
    patch.add_argument(
        "--require-platform",
        action="append",
        choices=PLATFORMS,
        default=[],
        help="除manifest自动推导外额外要求的已验证平台",
    )
    patch.add_argument(
        "--manifest",
        required=True,
        help="与 --key 一致且已通过证据门禁的 schema-v5 manifest",
    )
    patch.add_argument("--run-bundle", required=True, help="完整批次 run bundle")

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
        preflight_errors = validate_local_write_gate(
            args.owner_id, args.manifest, args.require_platform
        )
        manifest_errors = validate_bound_manifests(
            args.manifest,
            [str(item.get("key", "")) for item in payload],
        )
        run_errors = validate_bound_run_bundle(args.run_bundle)
        if preflight_errors or manifest_errors or run_errors:
            json.dump(
                {"ok": False, "errors": [*preflight_errors, *manifest_errors, *run_errors]},
                sys.stdout,
                ensure_ascii=False,
                indent=2,
            )
            sys.stdout.write("\n")
            return 1
        try:
            format_source_row_index = resolve_format_source_row_index(
                args.owner_id, args.format_source_row_index
            )
        except ValueError as error:
            json.dump(
                {"ok": False, "errors": [str(error)]},
                sys.stdout,
                ensure_ascii=False,
                indent=2,
            )
            sys.stdout.write("\n")
            return 1
        requests = build_batch_requests(
            args.sheet_id,
            args.start_row_index,
            payload,
            date=args.date,
            format_source_row_index=format_source_row_index,
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

    if args.command == "validate-append":
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("items"), list)
            or "readback" not in payload
        ):
            parser.error("validate-append 输入必须包含 items 数组和 readback")
        errors = validate_append_readback(
            payload["readback"],
            payload["items"],
            date=args.date,
        )
        json.dump(
            {"ok": not errors, "errors": errors},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0 if not errors else 1

    if args.command == "validate-format":
        if (
            not isinstance(payload, dict)
            or "anchor_readback" not in payload
            or "readback" not in payload
        ):
            parser.error("validate-format 输入必须包含 anchor_readback 和 readback")
        errors = validate_append_format(
            payload["anchor_readback"], payload["readback"]
        )
        json.dump(
            {"ok": not errors, "errors": errors},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0 if not errors else 1

    if args.command == "patch":
        if not isinstance(payload, dict):
            parser.error("patch 输入必须是 JSON 对象")
        preflight_errors = validate_local_write_gate(
            args.owner_id, [args.manifest], args.require_platform
        )
        manifest_errors = validate_bound_manifests([args.manifest], [args.key])
        run_errors = validate_bound_run_bundle(args.run_bundle)
        if preflight_errors or manifest_errors or run_errors:
            json.dump(
                {"ok": False, "errors": [*preflight_errors, *manifest_errors, *run_errors]},
                sys.stdout,
                ensure_ascii=False,
                indent=2,
            )
            sys.stdout.write("\n")
            return 1
        result = build_patch_requests(
            args.sheet_id,
            args.row_number,
            args.key,
            args.mode,
            payload.get("current_row"),
            args.preview_fingerprint,
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
