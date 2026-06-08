
#shipment_value = units * unit_cost
#route = origin_country + " → " + destination_country
#risk_level

#Risk rules:
    #Delayed      → High
    #In Transit   → Medium
    #Delivered    → Low
    #Cancelled    → High

def shipment_value(vendor):
    return vendor.get("units") * vendor.get("unit_cost")

def get_route(vendor):
    origin = vendor.get("origin_country","unknown")
    destination = vendor.get("destination_country","unknown")
    return f"{origin} → {destination}"

def risk_level(vendor):

    status = vendor.get("delivery_status").lower()

    if status in ["delayed","cancelled"]:
        return "High"
    elif status == "in transit":
        return "medium"
    elif status.lower() == "delivered":
        return "low"
    
    return "unknown"

def transform_data(valids):

    return [
        {
            "shipment_id": vendor.get("shipment_id"),
            "carrier": vendor.get("carrier"),
            "units": vendor.get("units"),
            "unit_cost": vendor.get("unit_cost"),
            "shipment_value": shipment_value(vendor),
            "route": get_route(vendor),
            "risk_level": risk_level(vendor)
        }
        for vendor in valids
    ]