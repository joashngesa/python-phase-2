#Output
    #carrier
    #shipment_count
    #total_units
    #total_shipment_value
    #avg_shipment_value

def report(transformed):

    summary = {}

    for vendor in transformed:

        carrier = vendor.get("carrier")
        shipment_id = vendor.get("shipment_id")
        units = vendor.get("units")
        shipment_value = vendor.get("shipment_value")

        if carrier not in summary:
            summary[carrier] = {
                "carrier": carrier,
                "shipment_count": 0,
                "total_units": 0,
                "total_shipment_value": 0,
                "avg_shipment_value": 0
            }

        summary[carrier]["shipment_count"] += 1
        summary[carrier]["total_units"] += units
        summary[carrier]["total_shipment_value"] += shipment_value

        for stockist in summary:
            data = summary[stockist]
            data["avg_shipment_value"] = round(data["total_shipment_value"] / data["shipment_count"],2)

    
    return list (summary.values())
