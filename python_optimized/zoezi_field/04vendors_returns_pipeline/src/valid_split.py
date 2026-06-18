
from src.validator import data_validation

def get_invalids(converted):

    invalids = []
    valids_raw = []
    duplicates = set()

    for revert in converted:
        is_valid, reasons = data_validation(revert)

        if not is_valid:
            invalid_data = revert.copy()
            invalid_data["error_reasons"] = ": ".join(reasons)
            invalids.append (invalid_data)
            continue

        return_id = revert.get("return_id")
        line_id = revert.get("line_id")
        keys = (return_id, line_id)

        if keys in duplicates:
            invalid_data = revert.copy()
            invalid_data["error_reasons"] = "duplicate return_id & line_id"
            invalids.append (invalid_data)

        else:
            duplicates.add (keys)
            valids_raw.append (revert.copy())

    return invalids, valids_raw    