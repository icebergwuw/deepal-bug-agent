import logging

from analyze_bug.core.paths import get_logs_dir


def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(f"analyze_bug.{name}")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logs_dir = get_logs_dir()
    logs_dir.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(logs_dir / log_file, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
