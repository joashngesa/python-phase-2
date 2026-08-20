"""
Check the json structure of the file. The contract required include:
    -> batch_id
    -> depot
    -> records
"""

from typing import Any
import logging

logger = logging.getLogger(__name__)


def extract_table(raw_file: Any) -> list[dict]:

    logger.info("File extraction initiated")

    if not isinstance(raw_file, dict):
        logger.error("File is not a dictioanry")
        raise KeyError("json payload must be dictionary")

    if raw_file["records"] is None:
        logger.error("Missing 'record' in the file")
        raise KeyError("missing 'record' in the file ")

    records = raw_file["records"]

    logger.info("File extraction completed")

    return records


def extract_depot(raw_file: str) -> str:

    logger.info("Depot extraction initiated")

    if not isinstance(raw_file, dict):
        raise KeyError("json payload must be dictionary")

    depot = raw_file.get("depot")

    if not depot:
        raise KeyError("missing 'depot' key in the file")

    logger.info("Depot extraction completed | depot=%s", depot)

    return depot


def extract_batch_id(raw_file: str) -> str:

    logger.info("Batch_id extraction initiated")

    if not isinstance(raw_file, dict):
        raise KeyError("json payload must be a dictionary")

    batch_id = raw_file.get("batch_id")

    if not batch_id:
        raise KeyError("'depot' key not found in metadata")

    logger.info("Batch_id extraction completed | batch_id=%s", batch_id)

    return batch_id
