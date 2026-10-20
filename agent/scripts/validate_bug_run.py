#!/usr/bin/env python3
"""Validate one complete Bug run before sheet write or after a Jira comment."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_bug_evidence_gate import nonempty, validate_log, validate_manifest


RUN_SCHEMA_VERSION = 1
RUN_STATUSES = {"planned", "complete", "no_changes", "ui_verified", "comment_verified"}
UI_BLOCK_TOKENS = ("gapi", "SAPISIDHASH", "ERR_BLOCKED_BY_CLIENT", "batchUpdate")
UI_UPDATE_MODES = {"append", "recheck", "review"}
UI_FILTER_ACTIONS = {"existing_covers_row", "no_filter_recorded", "extended_existing"}
UI_COLUMNS = tuple("ABCDEFGHIJ")
UI_LINK_COLUMNS = ("C", "D", "J")


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))



def validate_ui_readback(payload: Any, *, jira_key: str, sheet_row: int) -> list[str]:
    """Validate a Chrome UI write. This is not an API final readback."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["界面回读必须是 JSON 对象"]
    if payload.get("write_surface") != "chrome_ui":
        errors.append("界面回读 write_surface 必须为 chrome_ui")
    if payload.get("jira_key") != jira_key:
        errors.append("界面回读 jira_key 与 run item 不一致")
    if payload.get("sheet_row") != sheet_row:
        errors.append("界面回读 sheet_row 与 run item 不一致")
    reason = payload.get("api_block_reason")
    if not nonempty(reason) or not any(token in str(reason) for token in UI_BLOCK_TOKENS):
        errors.append("界面回读必须记录真实 API 阻断：" + "、".join(UI_BLOCK_TOKENS))
    mode = payload.get("update_mode")
    if mode not in UI_UPDATE_MODES:
        errors.append("界面回读 update_mode 必须为 append、recheck 或 review")
    if payload.get("row_height_fit") is not True:
        errors.append("界面回读必须确认行高已按内容撑开")
    links_verified = (
        payload.get("edit_mode_links_verified") is True
        and payload.get("links_remain_after_exit") is True
    )
    legacy_escape_only = (
        "edit_mode_links_verified" not in payload
        and "links_remain_after_exit" not in payload
        and payload.get("entered_edit_with_escape") is True
    )
    if not links_verified and not legacy_escape_only:
        errors.append("富文本必须在编辑态读到每个短标签 URL，并且退出编辑后链接仍在；Esc 清掉链接标记时不得提交")
    if payload.get("screenshot_not_used_as_cell_proof") is not True:
        errors.append("截图不能代替逐列公式栏回读")
    if payload.get("filter_action") not in UI_FILTER_ACTIONS:
        errors.append("界面回读 filter_action 无效")
    selection = payload.get("selection")
    if not isinstance(selection, str) or not re.fullmatch(r"[A-J][0-9]+", selection):
        errors.append("选区必须收回单个 A:J 单元格")
    elif int(selection[1:]) != sheet_row:
        errors.append("选区单元格不在目标行")
    cells = payload.get("cells")
    if not isinstance(cells, dict):
        errors.append("界面回读 cells 必须是对象")
        return errors
    for column in UI_COLUMNS:
        cell = cells.get(column)
        if not isinstance(cell, dict) or not isinstance(cell.get("formula_bar"), str):
            errors.append(f"{column} 缺少公式栏原文")
    if any(f"{column} 缺少公式栏原文" in error for error in errors):
        return errors

    formula_b = cells["B"]["formula_bar"].strip()
    if not formula_b.startswith("=HYPERLINK(") or jira_key not in formula_b:
        errors.append("B 必须是包含本 Jira Key 的 HYPERLINK 公式")
    formula_e = cells["E"]["formula_bar"].strip()
    if cells["E"].get("checkbox") is not True or formula_e not in {"FALSE", "TRUE"}:
        errors.append("E 必须是 BOOLEAN 复选框，不能用文本冒充")
    formula_d = cells["D"]["formula_bar"]
    for label in ("结论：", "依据：", "处理："):
        if label not in formula_d:
            errors.append(f"D 公式栏缺少{label}")
    for column in UI_LINK_COLUMNS:
        formula = cells[column]["formula_bar"]
        links = cells[column].get("links")
        if not isinstance(links, list) or not links:
            errors.append(f"{column} 缺少可点击短标签")
            continue
        texts: list[str] = []
        for index, link in enumerate(links, start=1):
            if not isinstance(link, dict):
                errors.append(f"{column} 链接第 {index} 项不是对象")
                continue
            link_text = link.get("text")
            uri = link.get("uri")
            if not nonempty(link_text) or link_text not in formula:
                errors.append(f"{column} 链接文字必须出现在公式栏原文中")
            if not isinstance(uri, str) or not uri.startswith(("http://", "https://")):
                errors.append(f"{column} 链接缺少 http(s) 目标")
            texts.append(link_text)
        if column == "C":
            for label in re.findall(r"\[([^\[\]\n]{1,80})\]", formula):
                if label not in texts:
                    errors.append(f"C 方括号证据 {label} 没有链接元数据")
        if column == "J":
            lines = [line.strip() for line in formula.splitlines() if line.strip()]
            link_texts = [link.get("text") if isinstance(link, dict) else None for link in links]
            if link_texts != lines:
                errors.append("J 必须一行一个短标签，且每行都有链接")
    for column in ("F", "H"):
        cell = cells[column]
        before = cell.get("before_formula_bar")
        after = cell.get("formula_bar")
        if not isinstance(before, str):
            errors.append(f"{column} 缺少写前公式栏")
            continue
        if mode == "append":
            if after.strip():
                errors.append(f"{column} 新增行写后必须为空")
            if before.strip() and cell.get("contamination_cleared") is not True:
                errors.append(f"{column} 写前非空必须清空并标记 contamination_cleared")
        elif mode == "recheck" and after != before:
            errors.append(f"{column} 复查不得改动")
        elif mode == "review" and column == "F" and after != before:
            errors.append("复盘不得改 F")
    return errors


def validate_run_bundle(payload: Any, phase: str = "prewrite") -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["run bundle 必须是 JSON 对象"]
    if payload.get("schema_version") != RUN_SCHEMA_VERSION:
        errors.append(f"run bundle schema_version 必须为 {RUN_SCHEMA_VERSION}")
    run_id = payload.get("run_id")
    if not nonempty(run_id):
        errors.append("run bundle 缺少 run_id")
    status = payload.get("status")
    if status not in RUN_STATUSES:
        errors.append("run bundle status 必须为 planned、complete、no_changes 或 ui_verified")
    for field in ("started_at", "query_summary"):
        if not nonempty(payload.get(field)):
            errors.append(f"run bundle 缺少 {field}")

    log_path_value = payload.get("action_log")
    log_path = Path(log_path_value) if nonempty(log_path_value) else None
    if log_path is None or not log_path.is_file():
        errors.append(f"run bundle 操作日志不存在：{log_path_value}")
        log_text = ""
    else:
        log_text = log_path.read_text(encoding="utf-8")
        if nonempty(run_id) and not re.search(rf"\b{re.escape(run_id)}\b", log_text):
            errors.append("操作日志未包含 run_id")

    items = payload.get("items")
    if not isinstance(items, list):
        errors.append("run bundle items 必须是数组")
        items = []
    if status == "no_changes":
        if items:
            errors.append("no_changes run 不得包含 items")
        if "无新增" not in log_text:
            errors.append("no_changes 操作日志必须明确写本次无新增")
    elif not items:
        errors.append("有写入计划的 run 必须包含 items")

    seen_keys: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"run item 第 {index} 项不是对象")
            continue
        key = item.get("jira_key")
        if not nonempty(key):
            errors.append(f"run item 第 {index} 项缺少 jira_key")
            continue
        if key in seen_keys:
            errors.append(f"run item jira_key 重复：{key}")
        seen_keys.add(key)
        comment_only = item.get("result_output") == "jira_comment_only"
        if phase == "comment" and not comment_only:
            errors.append(f"{key} comment 阶段 item.result_output 必须为 jira_comment_only")
        if comment_only and phase in {"final", "ui"}:
            errors.append(f"{key} jira_comment_only 不能走写表 final 或 ui")
        identity_fields = ["operator_owner_id", "target_owner_id"]
        if not comment_only:
            identity_fields.append("sheet_name")
        for field in identity_fields:
            if not nonempty(item.get(field)):
                errors.append(f"{key} run item 缺少 {field}")
        if comment_only:
            if nonempty(item.get("sheet_name")) or item.get("sheet_row") not in (None, ""):
                errors.append(f"{key} jira_comment_only 不得绑定表格行")
        elif not isinstance(item.get("sheet_row"), int) or item.get("sheet_row", 0) < 1:
            errors.append(f"{key} sheet_row 必须是正整数")

        manifest_value = item.get("manifest_path")
        manifest_path = Path(manifest_value) if nonempty(manifest_value) else None
        if manifest_path is None or not manifest_path.is_file():
            errors.append(f"{key} manifest 不存在：{manifest_value}")
        else:
            try:
                manifest = _load(manifest_path)
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{key} manifest 无法读取：{error}")
            else:
                errors.extend(f"{key} manifest：{error}" for error in validate_manifest(manifest, key))
                context = manifest.get("run_context", {})
                expected_context = {
                    "run_id": run_id,
                    "operator_owner_id": item.get("operator_owner_id"),
                    "target_owner_id": item.get("target_owner_id"),
                }
                if comment_only:
                    expected_context["result_output"] = "jira_comment_only"
                else:
                    expected_context["sheet_name"] = item.get("sheet_name")
                    expected_context["sheet_row"] = item.get("sheet_row")
                for field, expected_value in expected_context.items():
                    if context.get(field) != expected_value:
                        errors.append(f"{key} manifest run_context.{field} 与 run bundle 不一致")

        if log_path is not None:
            errors.extend(f"{key} 日志：{error}" for error in validate_log(log_path, key))
            if comment_only:
                if not re.search(rf"\b{re.escape(key)}\b", log_text):
                    errors.append(f"{key} 操作日志未列出 Jira key")
                if "未回填" not in log_text and "未写表" not in log_text:
                    errors.append(f"{key} 操作日志必须写明未写表")
            elif not re.search(rf"\b{re.escape(key)}\b.*(?:行|row)\D*{item.get('sheet_row')}", log_text, re.IGNORECASE):
                errors.append(f"{key} 操作日志未绑定写入行 {item.get('sheet_row')}")

        if phase == "ui":
            for field in ("ui_readback_path", "ui_readback_sha256"):
                if not nonempty(item.get(field)):
                    errors.append(f"{key} ui run item 缺少 {field}")
            ui_value = item.get("ui_readback_path")
            ui_path = Path(ui_value) if nonempty(ui_value) else None
            if ui_path is None or not ui_path.is_file():
                errors.append(f"{key} 界面回读文件不存在：{ui_value}")
            else:
                digest = hashlib.sha256(ui_path.read_bytes()).hexdigest()
                if digest != item.get("ui_readback_sha256"):
                    errors.append(f"{key} 界面回读 sha256 不一致")
                else:
                    try:
                        ui_payload = _load(ui_path)
                    except (OSError, json.JSONDecodeError) as error:
                        errors.append(f"{key} 界面回读无法读取：{error}")
                    else:
                        errors.extend(
                            f"{key} 界面回读：{error}"
                            for error in validate_ui_readback(
                                ui_payload,
                                jira_key=key,
                                sheet_row=item.get("sheet_row"),
                            )
                        )

        if phase == "comment" and status == "comment_verified":
            errors.extend(_comment_item_errors(item, key))

        if phase == "final":
            for field in ("readback_path", "validation_path", "readback_sha256"):
                if not nonempty(item.get(field)):
                    errors.append(f"{key} final run item 缺少 {field}")
            readback_value = item.get("readback_path")
            validation_value = item.get("validation_path")
            readback_path = Path(readback_value) if nonempty(readback_value) else None
            validation_path = Path(validation_value) if nonempty(validation_value) else None
            if readback_path is None or not readback_path.is_file():
                errors.append(f"{key} 回读文件不存在：{readback_value}")
            else:
                digest = hashlib.sha256(readback_path.read_bytes()).hexdigest()
                if digest != item.get("readback_sha256"):
                    errors.append(f"{key} 回读文件 sha256 不一致")
            if validation_path is None or not validation_path.is_file():
                errors.append(f"{key} 回读校验文件不存在：{validation_value}")
            else:
                try:
                    validation = _load(validation_path)
                except (OSError, json.JSONDecodeError) as error:
                    errors.append(f"{key} 回读校验无法读取：{error}")
                else:
                    if validation.get("ok") is not True or validation.get("errors"):
                        errors.append(f"{key} 回读校验未通过")

    if phase == "prewrite" and status != "planned":
        errors.append("prewrite 阶段 status 必须为 planned")
    if phase == "ui":
        if status != "ui_verified":
            errors.append("ui 阶段 status 必须为 ui_verified")
        if not nonempty(payload.get("completed_at")):
            errors.append("ui run 缺少 completed_at")
        if "界面回读" not in log_text or "未通过 API final" not in log_text:
            errors.append("ui 操作日志必须写明界面回读，且未通过 API final")
    if phase == "comment":
        if status not in {"comment_verified", "no_changes"}:
            errors.append("comment 阶段 status 必须为 comment_verified 或 no_changes")
        if status == "comment_verified":
            if not nonempty(payload.get("completed_at")):
                errors.append("comment run 缺少 completed_at")
            errors.extend(_comment_preflight_errors(payload, log_text))
            if "评论回读" not in log_text or "未转派" not in log_text:
                errors.append("comment 操作日志必须写明评论回读，且未转派")
    if phase == "final":
        if status == "ui_verified":
            errors.append("ui_verified 不能冒充 API final")
        if status == "comment_verified":
            errors.append("comment_verified 不能冒充 API final")
        if status not in {"complete", "no_changes"}:
            errors.append("final 阶段 status 必须为 complete 或 no_changes")
        if not nonempty(payload.get("completed_at")):
            errors.append("final run 缺少 completed_at")
        if status == "complete" and "回读校验" not in log_text:
            errors.append("complete 操作日志缺少回读校验")
    return errors



def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_object(path: Path, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = _load(path)
    except (OSError, json.JSONDecodeError) as error:
        return None, [f"{label}无法读取：{error}"]
    if not isinstance(payload, dict):
        return None, [f"{label}必须是 JSON 对象"]
    return payload, []


def _comment_item_errors(item: dict[str, Any], key: str) -> list[str]:
    errors: list[str] = []
    receipt_value = item.get("comment_receipt_path")
    readback_value = item.get("comment_readback_path")
    receipt_path = Path(receipt_value) if nonempty(receipt_value) else None
    readback_path = Path(readback_value) if nonempty(readback_value) else None
    if receipt_path is None or not receipt_path.is_file():
        errors.append(f"{key} 评论授权回执不存在：{receipt_value}")
        receipt = None
    else:
        if _sha256(receipt_path) != item.get("comment_receipt_sha256"):
            errors.append(f"{key} 评论授权回执 sha256 不一致")
        receipt, receipt_errors = _load_object(receipt_path, f"{key} 评论授权回执")
        errors.extend(receipt_errors)
    if readback_path is None or not readback_path.is_file():
        errors.append(f"{key} 评论回读不存在：{readback_value}")
        readback = None
    else:
        if _sha256(readback_path) != item.get("comment_readback_sha256"):
            errors.append(f"{key} 评论回读 sha256 不一致")
        readback, readback_errors = _load_object(readback_path, f"{key} 评论回读")
        errors.extend(readback_errors)
    if not isinstance(receipt, dict) or not isinstance(readback, dict):
        return errors
    if receipt.get("gate") != "passed" or receipt.get("jira_key") != key:
        errors.append(f"{key} 评论授权回执未通过或 Jira key 不一致")
    authorized = receipt.get("authorized_comment")
    body = readback.get("body")
    if not isinstance(authorized, str) or not isinstance(body, str) or authorized not in body:
        errors.append(f"{key} 评论回读必须包含授权正文")
    if not isinstance(body, str) or "（AI Generated）" not in body:
        errors.append(f"{key} 评论回读必须保留（AI Generated）")
    if not nonempty(readback.get("comment_id")):
        errors.append(f"{key} 评论回读缺少 comment_id")
    if readback.get("transitioned") is not False:
        errors.append(f"{key} 评论回读必须确认未转派、未关闭、未改状态")
    return errors


def _comment_preflight_errors(payload: dict[str, Any], log_text: str) -> list[str]:
    errors: list[str] = []
    value = payload.get("preflight_path")
    path = Path(value) if nonempty(value) else None
    if path is None or not path.is_file():
        return [f"comment run 缺少预检快照：{value}"]
    if _sha256(path) != payload.get("preflight_sha256"):
        errors.append("预检快照 sha256 不一致")
    preflight, load_errors = _load_object(path, "预检快照")
    errors.extend(load_errors)
    if not isinstance(preflight, dict):
        return errors
    if preflight.get("ok") is not True or preflight.get("mode") not in {"read_write", "external_write"}:
        errors.append("评论前预检未通过")
    access = preflight.get("online_access")
    if not isinstance(access, dict):
        access = {}
    for platform in ("jira", "google_drive"):
        receipt = access.get(platform)
        if not isinstance(receipt, dict) or receipt.get("required") is not True or receipt.get("fresh") is not True:
            errors.append(f"评论前预检必须要求并验证 {platform}")
    selected = set()
    for item in payload.get("items", []):
        if not isinstance(item, dict):
            continue
        manifest_value = item.get("manifest_path")
        manifest_path = Path(manifest_value) if nonempty(manifest_value) else None
        if manifest_path is None or not manifest_path.is_file():
            continue
        try:
            manifest = _load(manifest_path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(manifest, dict):
            selected.update(manifest.get("evidence_profiles") or [])
    required = {"voice": "alchemy", "visible_interaction": "mastergo"}
    for profile, platform in required.items():
        if profile not in selected:
            continue
        receipt = access.get(platform)
        if not isinstance(receipt, dict) or receipt.get("required") is not True or receipt.get("fresh") is not True:
            errors.append(f"{profile} 评论前预检必须要求并验证 {platform}")
    if "google_drive" not in log_text:
        errors.append("comment 操作日志必须记录 Google Drive 预检")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", help="run bundle JSON path；省略时从 stdin 读取")
    parser.add_argument("--phase", choices=("prewrite", "final", "ui", "comment"), default="prewrite")
    args = parser.parse_args()
    try:
        payload = _load(Path(args.bundle)) if args.bundle else json.load(sys.stdin)
    except (OSError, json.JSONDecodeError) as error:
        errors = [f"无法读取 run bundle：{error}"]
    else:
        errors = validate_run_bundle(payload, args.phase)
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
