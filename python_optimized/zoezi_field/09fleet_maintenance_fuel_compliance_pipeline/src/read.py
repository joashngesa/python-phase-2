import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def read_file(file_path):

    raw = Path(file_path)
    logger.debug("File read started | file_path=%s", raw)

    if raw.stat().st_size == 0:
        logger.warning("File is empty | file=%s", raw.name)
        raise ValueError(f"the file {raw.name} is empty")

    with open(raw, "r", encoding="utf-8") as file:
        data = json.load(file)

    logger.info(
        "File read complete | file=%s",
        raw.name,
    )

    return data
