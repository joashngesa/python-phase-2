#Output
    #warehouse
    #valid_line_count
    #total_ordered_qty
    #total_received_qty
    #total_ordered_value
    #total_received_value
    #total_shortage_qty

def warehouse(valids):
    return [
        {
            "warehouse": depo.get("warehouse"),
            "ordered_qty": depo.get("quantity_ordered"),
            "received_qty": depo.get("quantity_received"),
            "ordered_value": depo.get("quantity_ordered") * depo.get("unit_cost"),
            "received_value": depo.get("quantity_received") * depo.get("unit_cost"),
            "shortage_qty": depo.get("quantity_ordered") - depo.get("quantity_received")
        }
        for depo in valids
    ]
