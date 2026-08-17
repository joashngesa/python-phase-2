import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_file(raw_path):

    file_path = Path(raw_path)
    logger.info("File read started | file=%s", file_path.name)
    if file_path.stat().st_size == 0:
        logger.warning("Empty file | file=%s", file_path.name)
        raise ValueError(f"the file {file_path.name} is empty")

    with open(file_path, "r", encoding="utf-8") as file:
        raw = json.load(file)

    logger.info("File read complete | file=%s", file_path.name)

    return raw
