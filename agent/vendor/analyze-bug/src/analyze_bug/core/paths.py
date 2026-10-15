import os
from pathlib import Path


APP_NAME = "analyze-bug"
LEGACY_GEMINI_ROOT = Path.home() / ".gemini"
LEGACY_CONFIG_FILE = LEGACY_GEMINI_ROOT / "configs" / "analyze-bug.env"
LEGACY_COMMAND_FILE = LEGACY_GEMINI_ROOT / "commands" / "analyze-bug.toml"
LEGACY_COMMAND_DIR = LEGACY_GEMINI_ROOT / "commands" / "analyze-bug"


def is_windows() -> bool:
    return os.name == "nt"


def _env_path(name: str, fallback: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else fallback


def get_config_dir() -> Path:
    if is_windows():
        return _env_path("APPDATA", Path.home() / "AppData" / "Roaming") / APP_NAME
    return _env_path("XDG_CONFIG_HOME", Path.home() / ".config") / APP_NAME


def get_state_dir() -> Path:
    if is_windows():
        return _env_path("LOCALAPPDATA", Path.home() / "AppData" / "Local") / APP_NAME
    return _env_path("XDG_STATE_HOME", Path.home() / ".local" / "state") / APP_NAME


def get_data_dir() -> Path:
    if is_windows():
        return _env_path("LOCALAPPDATA", Path.home() / "AppData" / "Local") / APP_NAME
    return _env_path("XDG_DATA_HOME", Path.home() / ".local" / "share") / APP_NAME


def get_install_root() -> Path:
    return get_data_dir() / "runtime"


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def get_source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_resources_dir() -> Path:
    return get_source_root() / "resources"


def get_resource_file(name: str) -> Path:
    return get_resources_dir() / name


def get_logs_dir() -> Path:
    return get_state_dir() / "logs"


def get_config_file() -> Path:
    return get_config_dir() / "credentials.env"


def get_user_bin_dir() -> Path:
    return Path.home() / ".local" / "bin"


def get_skill_dir(platform: str) -> Path:
    if platform == "codex":
        return Path.home() / ".codex" / "skills" / "analyze-bug"
    if platform == "gemini":
        return Path.home() / ".agents" / "skills" / "analyze-bug"
    raise ValueError(f"Unsupported platform: {platform}")


def get_skill_dirs(platform: str) -> list[Path]:
    if platform == "codex":
        return [get_skill_dir(platform)]
    if platform == "gemini":
        return [Path.home() / ".agents" / "skills" / "analyze-bug"]
    raise ValueError(f"Unsupported platform: {platform}")


def get_legacy_skill_dirs(platform: str) -> list[Path]:
    if platform == "codex":
        return []
    if platform == "gemini":
        return [Path.home() / ".gemini" / "skills" / "analyze-bug"]
    raise ValueError(f"Unsupported platform: {platform}")


def iter_legacy_config_files() -> list[Path]:
    return [LEGACY_CONFIG_FILE]
