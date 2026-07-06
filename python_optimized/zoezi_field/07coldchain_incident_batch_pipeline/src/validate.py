
#incident rule
    #incident_date cannot be after generated_at date.
#Any required field is missing.
    #Any required field is blank.
    #Any conversion error exists.
    #product_category is not allowed.
    #delivery_status is not allowed.
    #carrier is not allowed.
    #required_temp_min_c is greater than required_temp_max_c.
    #xposure_minutes is less than or equal to 0.
    #incident_date is not YYYY-MM-DD.
    #incident_date is after generated_at date.

from datetime import datetime, date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_PRODUCT_CATEGORIES
from src.config import ALLOWED_DELIVERY_STATUSES
from src.config import ALLOWED_CARRIERS

def validate_data (event):

    validated = []

    for field in REQUIRED_FIELDS:
        if field not in event:
            validated.append (f"{field} is missing")

    incident_id = event.get("incident_id")
    if incident_id is None:
        validated.append ("incident_id is missing")
    elif not isinstance (incident_id, str):
        validated.append ("incident_id should be string")
    elif str(incident_id).strip() == "":
        validated.append ("incident_id is blank")
    
    shipment_id = event.get("shipment_id")
    if shipment_id is None:
        validated.append ("shipment_id is missing")
    elif not isinstance (shipment_id, str):
        validated.append ("shipment_id_id should be string")
    elif shipment_id.strip() == "":
        validated.append ("shipment_id is blank")

    warehouse_id = event.get("warehouse_id")
    if warehouse_id is None:
        validated.append ("warehouse_id is missing")
    elif not isinstance (warehouse_id, str):
        validated.append ("warehouse_id should be string")
    elif warehouse_id.strip() == "":
        validated.append ("warehouse_id is blank")

    product_category = event.get("product_category")
    if product_category is None:
        validated.append ("product_category is missing")
    elif not isinstance (product_category, str):
        validated.append ("product_category should be string")
    elif product_category.strip() == "":
        validated.append ("product_category is blank")
    elif product_category not in ALLOWED_PRODUCT_CATEGORIES:
        validated.append (f"product_category must be one of {'; '.join(ALLOWED_PRODUCT_CATEGORIES)}")

    product_name = event.get("product_name")
    if product_name is None:
        validated.append ("product_name is missing")
    elif not isinstance (product_name, str):
        validated.append ("product_name should be string")
    elif product_name.strip() == "":
        validated.append ("product_name is blank")

    required_temp_min_c = event.get("required_temp_min_c")
    required_temp_max_c = event.get("required_temp_max_c")
    if required_temp_max_c not in (None, "") and isinstance(required_temp_max_c, float):  
        if required_temp_min_c is None:
            validated.append ("required_temp_min_c is missing")
        elif not isinstance (required_temp_min_c, float):
            validated.append ("required_temp_min_c should be integer")
        elif required_temp_min_c > required_temp_max_c:
            validated.append ("the min temp required can't be > max temp required")

    if required_temp_max_c is None:
        validated.append ("required_temp_max_c is missing or blank")
    elif not isinstance (required_temp_max_c, float):
        validated.append ("required_temp_max_c should be a number")
    
    actual_temp_c = event.get("actual_temp_c")
    if actual_temp_c is None:
        validated.append ("actual_temp_c is missing or blank")
    elif not isinstance (actual_temp_c, float):
        validated.append ("actual_temp should be integer")

    incident_date = event.get("incident_date")
    processed_at_raw = event.get("processed_at")
    if incident_date is None:
        validated.append ("incident_date is missing")
    elif not isinstance (incident_date, date):
        validated.append ("incident_date should be in YYYY-MM-DD format")
    else:
        if hasattr (processed_at_raw, "date"):
            processed_at = processed_at_raw.date()
        else:
            processed_at = processed_at_raw

        if isinstance (processed_at, date) and incident_date > processed_at:
            validated.append ("incident_date can not be after generated_at date")

    exposure_minutes = event.get("exposure_minutes")
    if exposure_minutes is None:
        validated.append ("exposure_minutes is missing")
    elif not isinstance (exposure_minutes, int):
        validated.append("exposure_minutes should be a number")
    elif exposure_minutes <= 0:
        validated.append ("exposure_minutes should be > 0")

    delivery_status = event.get("delivery_status")
    if delivery_status is None:
        validated.append ("delivery_status is missing")
    elif not isinstance (delivery_status, str):
        validated.append ("delivery_status should be a string")
    elif delivery_status.strip() == "":
        validated.append ("delivery_Status is blank")
    elif delivery_status not in ALLOWED_DELIVERY_STATUSES:
        validated.append (f"delivery_status should be one of {'; '.join(ALLOWED_DELIVERY_STATUSES)}")

    
    carrier = event.get("carrier")
    if carrier is None:
        validated.append ("carrier is missing")
    elif not isinstance (carrier, str):
        validated.append ("carrier should be string")
    elif carrier.strip() == "":
        validated.append ("carrier is blank")
    elif carrier not in ALLOWED_CARRIERS:
        validated.append (f"carrier should be one of {'; '.join(ALLOWED_CARRIERS)}")

    if validated:
        return False, validated
    
    return True, []     