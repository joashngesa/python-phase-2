
from src.validator import inspect_data

def get_invalid(converted):

    invalids = []
    valids_raw = []
    duplicates = set()

    for item in converted:
        is_valid, reasons = inspect_data(item)

        if not is_valid:
            inaccurate = item.copy()
            inaccurate["error_reasons"] = ": ".join(reasons)
            invalids.append(inaccurate)
            continue

        po_id = item.get("po_id")
        line_id = item.get("line_id")
        keys = (po_id, line_id)

        if keys in duplicates:
            inaccurate = item.copy()
            inaccurate["error_reasons"] = "duplicate po_id & line_id"
            invalids.append(inaccurate)
        
        else:
            duplicates.add(keys)
            valids_raw.append(item.copy())

    return invalids, valids_raw