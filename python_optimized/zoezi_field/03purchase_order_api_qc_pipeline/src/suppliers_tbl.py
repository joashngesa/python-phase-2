#Output
    #supplier_id
    #supplier_name
    #valid_line_count
    #total_ordered_qty
    #total_received_qty
    #total_ordered_value
    #total_received_value
    #total_shortage_qty
    #avg_receipt_rate

def processed_data(valids):
    return [
        {
            "supplier_id": item.get("supplier_id"),
            "supplier_name": item.get("supplier_name"),
            "ordered_qty": item.get("quantity_ordered"),
            "received_qty": item.get("quantity_received"),
            "ordered_value": item.get("quantity_ordered") * item.get("unit_cost"),
            "received_value": item.get("quantity_received") * item.get("unit_cost"),
            "shortage_qty": item.get("quantity_ordered") - item.get("quantity_received")
        }
        for item in valids
    ]