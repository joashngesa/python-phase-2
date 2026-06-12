#Output
    #warehouse
    #valid_line_count
    #total_ordered_qty
    #total_received_qty
    #total_ordered_value
    #total_received_value
    #total_shortage_qty

def warehouse_summary(w_house):

    warehouse_sum = {}

    for vendor in w_house:

        warehouse = vendor.get("warehouse")
        ordered_qty = vendor.get("ordered_qty")
        received_qty = vendor.get("received_qty")
        ordered_value = vendor.get("ordered_value")
        received_value = vendor.get("received_value")
        shortage_qty = vendor.get("shortage_qty")

        if warehouse not in warehouse_sum:
            warehouse_sum[warehouse] = {
                "warehouse": warehouse,
                "valid_line_count": 0,
                "total_ordered_qty": 0,
                "total_received_qty": 0,
                "total_ordered_value": 0,
                "total_received_value": 0,
                "total_shortage_qty": 0
            }

        warehouse_sum[warehouse]["valid_line_count"] += 1
        warehouse_sum[warehouse]["total_ordered_qty"] += ordered_qty
        warehouse_sum[warehouse]["total_received_qty"] += received_qty
        warehouse_sum[warehouse]["total_ordered_value"] += ordered_value
        warehouse_sum[warehouse]["total_received_value"] += received_value
        warehouse_sum[warehouse]["total_shortage_qty"] += shortage_qty

    return list (warehouse_sum.values())