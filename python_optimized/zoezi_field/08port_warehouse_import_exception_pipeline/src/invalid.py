from src.validator import validate_table


def get_invalid_tbl(converted_data):

    invalid = []
    valid_raw = []

    for event in converted_data:

        is_valid, reasons = validate_table(event)

        if not is_valid:
            anomaly = event.copy()
            anomaly["error_reasons"] = ": ".join(reasons)
            invalid.append(anomaly)

        else:
            valid_raw.append(event.copy())

    return invalid, valid_raw
