from src.validate import validate_table


def get_invalid_valid_raw(converted):

    invalid = []
    valid_raw = []

    for procure in converted:

        is_valid, reasons = validate_table(procure)

        if not is_valid:
            buy = procure.copy()
            buy["error_reasons"] = "& ".join(reasons)
            invalid.append(buy)

        else:
            valid_raw.append(procure.copy())

    return invalid, valid_raw
