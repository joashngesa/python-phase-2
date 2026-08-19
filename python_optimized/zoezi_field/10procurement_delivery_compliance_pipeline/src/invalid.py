from src.validate import validate_table
import logging

logger = logging.getLogger(__name__)


def get_invalid_valid_raw(converted):

    invalid = []
    valid_raw = []
    logger.info(
        "Initial record screening initiated | total_converted_records=%d",
        len(converted),
    )

    for procure in converted:

        is_valid, reasons = validate_table(procure)

        if not is_valid:
            buy = procure.copy()
            buy["error_reasons"] = "& ".join(reasons)
            invalid.append(buy)

        else:
            valid_raw.append(procure.copy())

    logger.info("Initial record screening completed | invalid_count=%d", len(invalid))

    return invalid, valid_raw
