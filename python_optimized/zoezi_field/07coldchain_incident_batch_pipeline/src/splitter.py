
from src.validate import validate_data

def get_valids_invalids (converted):

    valids = []
    invalids = []

    for event in converted:
        is_valid, reasons = validate_data(event)

        if not is_valid:
            invalid_data = event.copy()
            invalid_data["error_reasons"] = ": ".join(reasons)
            invalids.append(invalid_data)
        
        else:
            valids.append(event.copy())

    return invalids, valids