
def get_valids(raw_valids):
    return [
        {
            "return_id": revert.get("return_id"),
            "line_id": revert.get("line_id"),
            "vendor_id": revert.get("vendor_id"),
            "vendor_name": revert.get("vendor_name"),
            "warehouse": revert.get("warehouse"),
            "sku": revert.get("sku"),
            "product": revert.get("product"),
            "return_date": revert.get("return_date"),
            "received_date": revert.get("received_date"),
            "return_reason": revert.get("return_reason"),
            "return_status": revert.get("return_status"),
            "quantity_returned": revert.get("quantity_returned"),
            "quantity_accepted": revert.get("quantity_accepted"),
            "unit_cost": revert.get("unit_cost")
        }
        for revert in raw_valids
    ]