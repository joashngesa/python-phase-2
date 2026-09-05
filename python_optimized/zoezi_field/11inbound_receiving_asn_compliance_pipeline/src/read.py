import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_json_file(file_path):

    raw_path = Path(file_path)
    logger.info("Read file initiated | file=%s", raw_path.name)

    if raw_path.stat().st_size == 0:
        logger.warning("File empty | file=%s", raw_path.name)
        raise ValueError(f"{file_path} is empty")

    with raw_path.open("r", encoding="utf-8") as file:
        raw_file = json.load(file)

    if not isinstance(raw_file, list):
        logger.warning("File is expected to be a list | file=%s", raw_path.name)
        raise TypeError(f"{raw_path.name} is expecting a list")

    logger.info("File read completed | file=%s", raw_path.name)

    return raw_file
