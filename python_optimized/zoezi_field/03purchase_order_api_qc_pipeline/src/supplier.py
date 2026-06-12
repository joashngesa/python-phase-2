
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

def supplier_summary(processed):

    suppliers_sum = {}

    for vendor in processed:

        supplier_id = vendor.get("supplier_id")
        supplier_name = vendor.get("supplier_name")
        ordered_qty = vendor.get("ordered_qty")
        received_qty = vendor.get("received_qty")
        ordered_value = vendor.get("ordered_value")
        received_value = vendor.get("received_value")
        shortage_qty = vendor.get("shortage_qty")

        if supplier_id not in suppliers_sum:
            suppliers_sum[supplier_id] = {
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "valid_line_count": 0,
                "total_ordered_qty": 0,
                "total_received_qty": 0,
                "total_ordered_value": 0,
                "total_received_value": 0,
                "total_shortage_qty": 0,
                "avg_receipt_rate": 0
            }

        suppliers_sum[supplier_id]["valid_line_count"] += 1
        suppliers_sum[supplier_id]["total_ordered_qty"] += ordered_qty
        suppliers_sum[supplier_id]["total_received_qty"] += received_qty
        suppliers_sum[supplier_id]["total_ordered_value"] += ordered_value
        suppliers_sum[supplier_id]["total_received_value"] += received_value
        suppliers_sum[supplier_id]["total_shortage_qty"] += shortage_qty

    for stock in suppliers_sum:
        data = suppliers_sum[stock]
        if data["total_ordered_qty"] > 0:
            data["avg_receipt_rate"] = round(data["total_received_qty"] / data["total_ordered_qty"],2)
        else:
            data["avg_receipt_rate"] == 0.0
    
    return list (suppliers_sum.values())