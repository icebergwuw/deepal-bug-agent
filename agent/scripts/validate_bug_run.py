#!/usr/bin/env python3
"""Validate one complete Bug run before and after an online sheet write."""

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
RUN_STATUSES = {"planned", "complete", "no_changes"}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
        errors.append("run bundle status 必须为 planned、complete 或 no_changes")
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
        for field in ("operator_owner_id", "target_owner_id", "sheet_name"):
            if not nonempty(item.get(field)):
                errors.append(f"{key} run item 缺少 {field}")
        if not isinstance(item.get("sheet_row"), int) or item.get("sheet_row", 0) < 1:
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
                    "sheet_name": item.get("sheet_name"),
                    "sheet_row": item.get("sheet_row"),
                }
                for field, expected_value in expected_context.items():
                    if context.get(field) != expected_value:
                        errors.append(f"{key} manifest run_context.{field} 与 run bundle 不一致")

        if log_path is not None:
            errors.extend(f"{key} 日志：{error}" for error in validate_log(log_path, key))
            if not re.search(rf"\b{re.escape(key)}\b.*(?:行|row)\D*{item.get('sheet_row')}", log_text, re.IGNORECASE):
                errors.append(f"{key} 操作日志未绑定写入行 {item.get('sheet_row')}")

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
    if phase == "final":
        if status not in {"complete", "no_changes"}:
            errors.append("final 阶段 status 必须为 complete 或 no_changes")
        if not nonempty(payload.get("completed_at")):
            errors.append("final run 缺少 completed_at")
        if status == "complete" and "回读校验" not in log_text:
            errors.append("complete 操作日志缺少回读校验")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", help="run bundle JSON path；省略时从 stdin 读取")
    parser.add_argument("--phase", choices=("prewrite", "final"), default="prewrite")
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
