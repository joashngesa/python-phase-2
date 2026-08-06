from src.validate import validate_data
import logging

logger = logging.getLogger(__name__)


def get_invalid(converted):

    invalid = []
    valid_raw = []
    logger.debug(
        "Initial record screening | total_converted_records=%d", len(converted)
    )

    for van in converted:

        is_valid, reasons = validate_data(van)

        if not is_valid:
            anomaly = van.copy()
            anomaly["error_reasons"] = "& ".join(reasons)
            invalid.append(anomaly)

        else:
            valid_raw.append(van.copy())

    logger.info(
        "Initial record screening completed | valid_raw_records=%d | invalid_records=%d",
        len(valid_raw),
        len(invalid),
    )
    return invalid, valid_raw
