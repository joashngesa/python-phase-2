

def get_valids(valids_raw):

    return [
        {
    "return_id": item.get("return_id"),
    "vendor_id": item.get("vendor_id"),
    "vendor_name": item.get("vendor_name"),
    "warehouse": item.get("warehouse"),
    "product_sku": item.get("product_sku"),
    "product_name": item.get("product_name"),
    "return_date":item.get("return_date"),
    "reason": item.get("reason"),
    "quantity": item.get("quantity"),
    "unit_cost": item.get("unit_cost"),
    "status": item.get("status")
        }
        for item in valids_raw
    ]