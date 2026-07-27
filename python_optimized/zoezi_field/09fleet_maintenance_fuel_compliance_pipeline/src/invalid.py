from src.validate import validate_data


def get_invalid(converted):

    invalid = []
    valid_raw = []

    for van in converted:

        is_valid, reasons = validate_data(van)

        if not is_valid:
            anomaly = van.copy()
            anomaly["error_reasons"] = "& ".join(reasons)
            invalid.append(anomaly)

        else:
            valid_raw.append(van.copy())

    return invalid, valid_raw
