# Duplicates: inspection_id + vehicle_id + inspection_date

import logging

logger = logging.getLogger(__name__)


def get_duplicates_valid(valid_raw):

    logger.debug("Record deduplication started | valid_raw=%d", len(valid_raw))
    valid = []
    duplicates = []
    seen_dups = set()

    for van in valid_raw:

        inspection_id = van.get("inspection_id")
        vehicle_id = van.get("vehicle_id")
        inspection_date = van.get("inspection_date")
        key_dups = (inspection_id, vehicle_id, inspection_date)

        if key_dups in seen_dups:
            clone = van.copy()
            clone["error_reasons"] = "inspection_id, vehicle_id + inspection_date"
            duplicates.append(clone)

        else:
            seen_dups.add(key_dups)
            valid.append(van.copy())

    logger.info(
        "Record deduplication completed | unique_valid_records=%d | duplicate_records=%d",
        len(valid),
        len(duplicates),
    )
    return duplicates, valid
