from src.validate import validate_data


def get_valid_invalids(converted):

    valid = []
    invalids = []

    for event in converted:
        is_valid, reasons = validate_data(event)

        if not is_valid:
            invalid_data = event.copy()
            invalid_data["error_reasons"] = ": ".join(reasons)
            invalids.append(invalid_data)

        else:
            valid.append(event.copy())

    return invalids, valid
