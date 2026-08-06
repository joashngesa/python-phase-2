import logging
from typing import Any

logger = logging.getLogger(__name__)


def _find_table(json: Any) -> list[dict] | None:
    """
    -> Recursively searches for an empty list of dictionaries
    -> This helper function does not log every failure in inspected
        branch because branch failure does not mean complete extraction failed
    """
    if isinstance(json, list):
        if json and all(isinstance(record, dict) for record in json):
            return json

        return None

    if isinstance(json, dict):
        for record in json.values():
            table = _find_table(record)

            if table is not None:
                return table

    return None


def extract_json(raw_data: Any) -> list[dict]:

    logging.debug("Table extraction started")

    record = _find_table(raw_data)

    if record is None:
        logging.warning("No valid table found in json payload")
        raise ValueError("could not find a valid list of dictionaries")

    logger.info("Table extraction completed | raw_record_count=%d", len(record))

    return record


def extract_depot(raw_data) -> str:

    logger.debug("Depot extraction started")

    if not isinstance(raw_data, dict):
        raise KeyError("json payload must be dictionary")

    metadata = raw_data.get("metadata")
    if not isinstance(metadata, dict):
        raise KeyError("missing / invalid 'metadata' dictionary")

    depot = metadata.get("depot")
    if not depot:
        raise KeyError("Missing 'depot' key inside metadata")

    logger.info("Depot extraction completed | depot=%s", depot)

    return depot


def extract_batch_id(raw_data):

    logger.debug("Batch_id extraction started")

    if not isinstance(raw_data, dict):
        raise KeyError("json payload must be dictionary")

    metadata = raw_data.get("metadata")
    if not isinstance(metadata, dict):
        raise KeyError("missing / invalid 'metadata' dictionary")

    batch_id = metadata.get("batch_id")
    if not batch_id:
        raise KeyError("missing 'batch_id' inside metadata")

    logger.info("Batch_id extraction completed | batch_id=%s", batch_id)

    return batch_id
