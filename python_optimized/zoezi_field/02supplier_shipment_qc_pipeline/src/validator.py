
required_fields = [
    "shipment_id",
    "supplier_id",
    "supplier_name",
    "carrier",
    "origin_country",
    "destination_country",
    "shipment_date",
    "delivery_status",
    "units",
    "unit_cost"
]

allowed_statuses = ["Delivered", "In Transit", "Delayed", "Cancelled"]

def validate_data(vendor):

    for column in required_fields:
        if column not in vendor:
            return False, f" the column {column}is missing"
        
    shipment_id = vendor.get("shipment_id")
    supplier_id = vendor.get("supplier_id")
    supplier_name = vendor.get("supplier_name")
    carrier = vendor.get("carrier")
    origin_country = vendor.get("origin_country")
    destination_country = vendor.get("destination_country")
        #in the coming lessons, we should practice on how to handle dates in python, at the moment i have no idea😄😄
    shipment_date = vendor.get("shipment_date")
    delivery_status = vendor.get("delivery_status")
    units = vendor.get("units")
    unit_cost = vendor.get("unit_cost") 

    if shipment_id is None:
        return False, "shipment_id absent"
    if not shipment_id.strip():
        return False, "shipment_id is blank"
    if not isinstance (shipment_id, str):
        return False, "shipment_id should be a string"
    if supplier_id is None:
        return False, "supplier_id absent"
    if not supplier_id.strip():
        return False, "supplier_id is blank"
    if not isinstance (supplier_id, str):
        return False, "supplier_id should be a string"
    if supplier_name is None:
        return False, "supplier_name absent"
    if not supplier_name.strip():
        return False, "supplier_name is blank"
    if not isinstance (supplier_name, str):
        return False, "supplier_name should be a string"
    if carrier is None:
        return False, "carrier is absent"
    if not carrier.strip():
        return False, "carrier is blank"
    if not isinstance (carrier, str):
        return False, "carrier should be a string"
    if origin_country is None:
        return False, "origin_country is blank"
    if not origin_country.strip():
        return False, "origin_country is blank"
    if not isinstance (origin_country, str):
        return False, "origin_country should be a string"
    if destination_country is None:
        return False, "destination_country absent"
    if not destination_country.strip():
        return False, "destination_country blank"
    if not isinstance (destination_country, str):
        return False, "destination_country should be string"
    if delivery_status is None:
        return False, "delivery_status absent"
    if not delivery_status.strip():
        return False, "delivery_status blank"
    if delivery_status not in allowed_statuses:
        return False, "delivery_status must be one of Delivered,In Transit,Delayed,Cancelled"
    if units is None:
        return False, "units is absent or incorrect"
    if units <= 0:
        return False, "units should be > than zero"
    if unit_cost is None:
        return False, "unit_cost absent or incorrect"
    if unit_cost <= 0:
        return False, "unit_cost should be > than zero"
        
    return True, None
       
    
    
        