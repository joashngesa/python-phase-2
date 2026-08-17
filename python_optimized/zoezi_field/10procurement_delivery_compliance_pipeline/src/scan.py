import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def scan_folder(raw_input_dir: Path, file_pattern: str) -> list[Path]:

    raw_path = Path(raw_input_dir)
    logger.debug("Input scan started | path=%s", raw_path)

    if not raw_path.exists():
        logger.error("Input directory absent | path=%s", raw_path)
        raise FileNotFoundError(f"input folder not found in {raw_path}")

    if not raw_path.is_dir:
        logger.error("Input path is not a directory | path=%s", raw_path)
        raise NotADirectoryError(f"{raw_path} is not a directory")

    files = sorted(record for record in raw_path.glob(file_pattern) if record.is_file())

    if not files:
        logger.error(
            "Input scan completed with no matching files | path=%s | pattern=%s",
            raw_path,
            file_pattern,
        )
        raise ValueError(f"No files found matching {file_pattern}")

    logger.info(
        "Input scan completed | path=%s | files_discovered=%d", raw_path, len(files)
    )
    logger.debug("Discovered input files | files=%s", [file for file in files])

    return files
