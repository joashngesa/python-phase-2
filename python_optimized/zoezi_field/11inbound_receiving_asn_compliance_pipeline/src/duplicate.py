import logging

logger = logging.getLogger(__name__)


def get_duplicates(valid):

    duplicates = []
    seen_id = set()
    logger.info("Duplicate detection initiated")

    for procure in valid:

        receipt_id = procure.get("receipt_id")

        if receipt_id in seen_id:
            buy = procure.copy()
            buy["duplicates"] = "duplicate receipt_id"
            duplicates.append(buy)

        else:
            seen_id.add(receipt_id)

    logger.info("Duplicate detection completed | duplicates_count=%d", len(duplicates))

    return duplicates
