from src.validate import validate_data


def get_invalid_valid(converted):

    invalid = []
    valid = []

    for procure in converted:

        is_valid, reasons = validate_data(procure)

        if not is_valid:
            purchase = procure.copy()
            purchase["error_reasons"] = " & ".join(reasons)
            invalid.append(purchase)

        else:
            valid.append(procure.copy())

    return invalid, valid
