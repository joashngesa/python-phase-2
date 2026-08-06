import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def logging_configuration(
    log_file: Path | str,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> None:
    """
    - configure application for the pipeline
    - Console level:
        INFO & above
    - File level:
        DEBUG & above
    """
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        fmt=("%(asctime)s | %(levelname)-8s | " "%(name)s | %(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # prevent duplicate handlers if configuration is called again by closing existing handlers
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
