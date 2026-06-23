
from src.validator import validate_data

def get_invalid(converted):

    invalids = []
    valids_raw = []

    for item in converted:
        is_valid, reason = validate_data(item)

        if not is_valid:
            invalid_data = item.copy()
            invalid_data["error_reasons"] = ": ".join(reason)
            invalids.append(invalid_data)
        else:
            valids_raw.append(item.copy())

    
    return invalids, valids_raw











