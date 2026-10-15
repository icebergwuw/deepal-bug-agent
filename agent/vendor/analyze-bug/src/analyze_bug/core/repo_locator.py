from __future__ import annotations

import os
from pathlib import Path

from analyze_bug.core.config import get_online_dialogue_root


def detect_online_dialogue_root(cwd: str | Path | None = None) -> Path | None:
    configured = get_online_dialogue_root()
    candidates: list[Path] = []

    if configured:
        candidates.append(Path(configured).expanduser())

    current = Path(cwd or os.getcwd()).expanduser().resolve()
    candidates.append(current)
    candidates.append(current.parent / "online-dialogue")
    candidates.append(Path.home() / "Code" / "online-dialogue")

    for candidate in candidates:
        if _looks_like_online_dialogue(candidate):
            return candidate.resolve()
    return None


def _looks_like_online_dialogue(path: Path) -> bool:
    if not path.exists() or not path.is_dir():
        return False

    markers = [
        path / "AGENTS.md",
        path / "dialogue-common" / "src" / "main" / "resources" / "config" / "dialogScenarioBase.json",
    ]
    return all(marker.exists() for marker in markers)
