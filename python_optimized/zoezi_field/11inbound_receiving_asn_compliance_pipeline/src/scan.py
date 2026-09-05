from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def scan_folder(input_folder: Path, file_pattern: str):

    input_dir = Path(input_folder)
    logger.debug("Input scanning initiated | path=%s", input_dir)

    if not input_dir.exists():
        logger.critical("Input directory absent | path=%s", input_dir)
        raise FileNotFoundError(f"{input_dir} is not found")

    if not input_dir.is_dir():
        logger.error("Input path has no directory | path=%s", input_dir)
        raise NotADirectoryError(f"{input_dir} is not a directory")

    records = sorted(file for file in input_dir.glob(file_pattern) if file.is_file())

    if not records:
        logger.error(
            "Input scanning completed with no matching files | path=%s | pattern=%s",
            input_dir,
            file_pattern,
        )
        raise ValueError(f"no files matching {file_pattern}")

    logger.debug(
        "Input scanning completed | files_discovered=%d | files=%s",
        len(records),
        [file for file in records],
    )
    return records
