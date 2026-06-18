

    #vendor_id
    #vendor_name
    #valid_line_count
    #total_returned_qty
    #total_accepted_qty
    #total_rejected_qty
    #total_return_value
    #total_accepted_value
    #avg_acceptance_rate
def vendor_summary(vendor_tbl):

    vendors = {}

    for stockist in vendor_tbl:

        vendor_id = stockist.get("vendor_id")
        vendor_name = stockist.get("vendor_name")
        qty_returned = stockist.get("qty_returned")
        qty_accepted = stockist.get("qty_accepted")
        qty_rejected = stockist.get("qty_rejected")
        return_value = stockist.get("return_value")
        accepted_value = stockist.get("accepted_value")

        if vendor_id not in vendors:
            vendors[vendor_id] = {
                "vendor_id": vendor_id,
                "vendor_name": vendor_name,
                "valid_line_count": 0,
                "total_returned_qty": 0,
                "total_accepted_qty": 0,
                "total_rejected_qty": 0,
                "total_return_value": 0,
                "total_accepted_value": 0,
                "avg_acceptance_rate": 0
            }

        vendors[vendor_id]["valid_line_count"] += 1
        vendors[vendor_id]["total_returned_qty"] += qty_returned
        vendors[vendor_id]["total_accepted_qty"] += qty_accepted
        vendors[vendor_id]["total_rejected_qty"] += qty_rejected
        vendors[vendor_id]["total_return_value"] += return_value
        vendors[vendor_id]["total_accepted_value"] += accepted_value

    for depo in vendors:
        distro = vendors[vendor_id]

        if distro["total_returned_qty"] > 0:
            distro["avg_acceptance_rate"] = distro["total_accepted_qty"] / distro["total_returned_qty"]
        else:
                distro["avg_acceptance_rate"] == 0.0

            
    return list(vendors.values())