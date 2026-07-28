#!/usr/bin/env python3
"""Validate the active Bug rule architecture without modifying the workspace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "agent/rules-version.md",
    "agent/evidence-contract.md",
    "agent/output-contract.md",
    "agent/workflows/bug.md",
    "agent/workflows/review.md",
    "agent/sheet-contract.md",
    "agent/context.md",
    "agent/bug-owners/registry.yaml",
)

AUTHORITY_REFERENCES = (
    "agent/evidence-contract.md",
    "agent/output-contract.md",
    "agent/workflows/bug.md",
    "agent/workflows/review.md",
    "agent/sheet-contract.md",
    "agent/bug-owners/registry.yaml",
    "agent/rules-version.md",
)

COMPATIBILITY_FILES = (
    "agent/workflow.md",
    "agent/meeting-feedback-workflow.md",
    "agent/sheet-template.md",
    "agent/sheet-style.md",
    "agent/bug-index.md",
    "agent/li-xin-bug-index.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path, skill: Path) -> list[str]:
    errors: list[str] = []

    if not (root / ".git").is_dir():
        errors.append("工作区尚未初始化 Git 仓库")

    gitignore_path = root / ".gitignore"
    if not gitignore_path.is_file():
        errors.append("缺少 .gitignore")
    else:
        gitignore = read(gitignore_path)
        for pattern in (".env", ".mastergo/", ".DS_Store", "__pycache__/"):
            if pattern not in gitignore:
                errors.append(f".gitignore 缺少安全模式：{pattern}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少权威文件：{relative}")

    version_path = root / "agent/rules-version.md"
    version_text = read(version_path) if version_path.exists() else ""
    match = re.search(r"^- 当前版本：`([^`]+)`$", version_text, re.MULTILINE)
    if not match:
        errors.append("rules-version.md 缺少唯一当前版本")

    agents_text = read(root / "AGENTS.md")
    for reference in AUTHORITY_REFERENCES:
        if reference not in agents_text:
            errors.append(f"AGENTS.md 未登记权威入口：{reference}")

    for relative in (
        "AGENTS.md",
        "agent/evidence-contract.md",
        "agent/output-contract.md",
        "agent/workflows/bug.md",
        "agent/sheet-contract.md",
    ):
        text = read(root / relative)
        if re.search(r"(?:当前规则版本|规则版本)：`v\d", text):
            errors.append(f"{relative} 重复维护了具体版本号")

    for relative in COMPATIBILITY_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"缺少兼容入口：{relative}")
            continue
        text = read(path)
        if "只保留旧路径兼容" not in text:
            errors.append(f"兼容入口含义不明确：{relative}")

    skill_text = read(skill)
    for reference in (
        "agent/evidence-contract.md",
        "agent/output-contract.md",
        "agent/sheet-contract.md",
        "agent/workflows/bug.md",
    ):
        if reference not in skill_text:
            errors.append(f"Skill 未加载权威入口：{reference}")
    for old_heading in (
        "## Execute The Bug Flow",
        "## Query External Evidence",
        "## Return Concise Results",
    ):
        if old_heading in skill_text:
            errors.append(f"Skill 仍复制业务规则：{old_heading}")

    sheet_script = read(root / "agent/scripts/bug_sheet_contract.py")
    if "def linked_formula" in sheet_script:
        errors.append("写表脚本仍包含旧多 HYPERLINK 生成器")
    if "link_list_cell(links)" not in sheet_script:
        errors.append("写表脚本未使用富文本链接列表")

    dashboard_token = "Dashboard.jspa?selectPageId=17302"
    if dashboard_token not in read(root / "agent/context.md"):
        errors.append("context.md 缺少 Bug 清单 Dashboard 17302")
    if "Jira Dashboard 17302" not in read(root / "agent/workflows/bug.md"):
        errors.append("Bug 流程未定义 Bug 清单入口")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Bug workspace root",
    )
    parser.add_argument(
        "--skill",
        default="/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md",
        help="Skill entrypoint",
    )
    args = parser.parse_args()

    errors = validate(Path(args.root).resolve(), Path(args.skill).resolve())
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
