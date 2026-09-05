from src.validate import validate_data
import logging

logger = logging.getLogger(__name__)


def get_invalid_valid(converted):

    invalid = []
    valid = []
    logger.info("Validation initiated | total_converted_records=%d", len(converted))

    for procure in converted:

        is_valid, reasons = validate_data(procure)

        if not is_valid:
            purchase = procure.copy()
            purchase["error_reasons"] = " & ".join(reasons)
            invalid.append(purchase)

        else:
            valid.append(procure.copy())

    logger.info(
        "Validation completed | valid_count=%d | invalid_count=%d",
        len(valid),
        len(invalid),
    )

    return invalid, valid
