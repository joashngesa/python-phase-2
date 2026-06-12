
#transformation output
    #ordered_value = quantity_ordered * unit_cost
    #received_value = quantity_received * unit_cost
    #shortage_qty = quantity_ordered - quantity_received
    #receipt_rate = quantity_received / quantity_ordered
    #fulfillment_status
        #Cancelled order_status       → Cancelled
        #quantity_received == 0       → Not Received
        #quantity_received < ordered  → Short Received
        #$quantity_received == ordered → Fully Received

def ordered_value(item):
    return item.get("quantity_ordered") * item.get("unit_cost")


def received_value(item):
    return item.get("quantity_received") * item.get("unit_cost")


def shortage_qty(item):
    return item.get("quantity_ordered") - item.get("quantity_received")


def receipt_rate(item):
    return item.get("quantity_received") / item.get("quantity_ordered")


def fulfillment_status(item):
    status = item.get("order_status")
    qty_ordered = item.get("quantity_ordered")
    qty_received = item.get("quantity_received")


    if status.lower() == "cancelled":
        return "Cancelled"
    if qty_received == 0:
        return "Not received"
    if qty_received < qty_ordered:
        return "short received"
    if qty_received == qty_ordered:
        return "fully received"
    

def transform_data(valids):
    return [
        {
            "ordered_value": ordered_value(item),
            "received_value": received_value(item),
            "shortage_quantity": shortage_qty(item),
            "receipt_rate": receipt_rate(item),
            "fulfillment_status": fulfillment_status(item)
        }
        for item in valids
    ]
     
