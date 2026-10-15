import argparse
import shutil
from pathlib import Path

from analyze_bug.core.skills import render_skill


PACKAGE_FILES = [
    "pyproject.toml",
    "uv.lock",
    "README.md",
    "install.sh",
    "install.ps1",
    "src/resources",
]
SOURCE_PACKAGES = ["analyze_bug"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def stage_distribution(output_dir: Path) -> Path:
    source_root = project_root()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for relative in PACKAGE_FILES:
        src = source_root / relative
        if src.exists():
            dest = output_dir / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(
                    src,
                    dest,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.pyd"),
                )
            else:
                shutil.copy2(src, dest)

    (output_dir / "src").mkdir(parents=True, exist_ok=True)
    for package_name in SOURCE_PACKAGES:
        shutil.copytree(
            source_root / "src" / package_name,
            output_dir / "src" / package_name,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.pyd"),
        )

    for platform in ("codex", "gemini"):
        skill_dir = output_dir / "skills" / platform / "analyze-bug"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(render_skill(platform), encoding="utf-8")

    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    stage_distribution(Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
