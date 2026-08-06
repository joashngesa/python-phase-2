from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def scan_folder(input_path, file_pattern) -> list[Path]:

    raw_path = Path(input_path)
    logger.debug("Input scan started | path=%s", raw_path)

    if not raw_path.exists():
        logger.error("Input directory does not exist | path=%s", raw_path)
        raise FileNotFoundError(f"No input folder found in {raw_path}")

    if not raw_path.is_dir():
        logger.error("Input path is not a directory | path=%s", raw_path)
        raise NotADirectoryError(f"No folder found in {raw_path}")

    files = sorted(record for record in raw_path.glob(file_pattern) if record.is_file())

    if not files:
        logger.warning(
            "Input scan completed with no matching files | path=%s | pattern=%s",
            raw_path,
            file_pattern,
        )
        raise ValueError(f"No files found matching the pattern {file_pattern}")

    logger.info(
        "Input scan completed | path=%s | files discovered=%d", raw_path, len(files)
    )
    logger.debug(
        "Discovered input files | files=%s",
        [file_path.name for file_path in files],
    )

    return files
