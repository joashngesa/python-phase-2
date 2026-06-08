
from src.validator import validate_data

def split_table(converted):

    invalids = []
    valids = []
    duplicates = set()

    for vendor in converted:
        is_valid, reason = validate_data(vendor)

        if not is_valid:
            invalid_data = vendor.copy()
            invalid_data["error_reason"] = reason
            invalids.append(invalid_data)
            continue

        shipment_id = vendor.get("shipment_id")
        supplier_id = vendor.get("supplier_id")
        keys = (supplier_id, shipment_id)

        if keys in duplicates:
            invalid_data = vendor.copy()
            invalid_data["error_reason"] = "duplicate shipment_id & supplier_id"
            invalids.append(invalid_data)

        else:
            duplicates.add(keys)
            valids.append(vendor.copy())

    return invalids, valids