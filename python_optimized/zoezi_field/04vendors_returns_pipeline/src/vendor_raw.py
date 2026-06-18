

def vendor_table(valids):
    return [
        {
            "vendor_id": revert.get("vendor_id"),
            "vendor_name": revert.get("vendor_name"),
            "qty_returned": revert.get("quantity_returned"),
            "qty_accepted": revert.get("quantity_accepted"),
            "qty_rejected": revert.get("quantity_returned") - revert.get("quantity_accepted"),
            "return_value": revert.get("quantity_returned") * revert.get("unit_cost"),
            "accepted_value": revert.get("quantity_accepted") * revert.get("unit_cost"),
        }
        for revert in valids
    ]