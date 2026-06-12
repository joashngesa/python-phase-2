
def get_valids (valids_raw):
    return [
        {
            "po_id": item.get("po_id"),
            "line_id": item.get("line_id"),
            "supplier_id": item.get("supplier_id"),
            "supplier_name": item.get("supplier_name"),
            "warehouse": item.get("warehouse"),
            "sku": item.get("sku"),
            "product": item.get("product"),
            "order_date": item.get("order_date"),
            "expected_delivery_date": item.get("expected_delivery_date"),
            "order_status": item.get("order_status"),
            "quantity_ordered": item.get("quantity_ordered"),
            "quantity_received": item.get("quantity_received"),
            "unit_cost": item.get("unit_cost")
        }
        for item in valids_raw
    ]