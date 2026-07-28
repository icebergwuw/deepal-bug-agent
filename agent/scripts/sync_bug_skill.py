#!/usr/bin/env python3
"""Check or install the Git-tracked Deepal Bug Skill consumer."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "agent/skills/deepal-product-bug-handler/SKILL.md"
DEFAULT_TARGET = Path(
    "/Users/you.wu/.codex/skills/deepal-product-bug-handler/SKILL.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument(
        "--install",
        action="store_true",
        help="用 Git 内模板覆盖安装副本；默认只校验",
    )
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    source_text = SOURCE.read_text(encoding="utf-8")
    if args.install:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE, target)

    installed = target.is_file()
    matches = installed and target.read_text(encoding="utf-8") == source_text
    print(
        json.dumps(
            {
                "ok": matches,
                "source": str(SOURCE),
                "target": str(target),
                "installed": installed,
                "matches": matches,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
