#!/usr/bin/env python3
"""Validate the preloaded operator-to-module source registry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


COLUMN = re.compile(r"^[A-Z]+$")


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be an object"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    owners = data.get("owners")
    if not isinstance(owners, list) or not owners:
        return errors + ["owners must be a non-empty array"]

    ids: set[str] = set()
    names: set[str] = set()
    for owner_index, owner in enumerate(owners):
        prefix = f"owners[{owner_index}]"
        if not isinstance(owner, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("owner_id", "display_name", "spreadsheet_id", "workbook_title"):
            if not text(owner.get(field)):
                errors.append(f"{prefix}.{field} must be non-empty text")
        owner_id = owner.get("owner_id")
        display_name = owner.get("display_name")
        if isinstance(owner_id, str):
            if owner_id in ids:
                errors.append(f"duplicate owner_id: {owner_id}")
            ids.add(owner_id)
        if isinstance(display_name, str):
            if display_name in names:
                errors.append(f"duplicate display_name: {display_name}")
            names.add(display_name)

        sheets = owner.get("module_sheets")
        if not isinstance(sheets, list) or not sheets:
            errors.append(f"{prefix}.module_sheets must be a non-empty array")
            continue
        sheet_keys: set[tuple[str, str]] = set()
        for sheet_index, sheet in enumerate(sheets):
            sprefix = f"{prefix}.module_sheets[{sheet_index}]"
            if not isinstance(sheet, dict):
                errors.append(f"{sprefix} must be an object")
                continue
            for field in ("sheet_name", "gid"):
                if not text(sheet.get(field)):
                    errors.append(f"{sprefix}.{field} must be non-empty text")
            for field in ("module_column", "ue_column"):
                value = sheet.get(field)
                if not text(value) or not COLUMN.fullmatch(value):
                    errors.append(f"{sprefix}.{field} must be an A1 column name")
            key = (str(sheet.get("sheet_name")), str(sheet.get("gid")))
            if key in sheet_keys:
                errors.append(f"duplicate sheet mapping for {owner_id}: {key}")
            sheet_keys.add(key)
            modules = sheet.get("modules")
            if not isinstance(modules, list) or not modules:
                errors.append(f"{sprefix}.modules must be a non-empty array")
            elif any(not text(module) for module in modules):
                errors.append(f"{sprefix}.modules must contain non-empty text")
            elif len(modules) != len(set(modules)):
                errors.append(f"{sprefix}.modules contains duplicates")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid registry: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
