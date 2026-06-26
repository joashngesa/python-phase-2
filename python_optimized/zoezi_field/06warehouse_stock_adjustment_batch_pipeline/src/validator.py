
from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_STATUSES
from src.config import ALLOWED_ADJUSTMENT_TYPES

from datetime import datetime, date

#A record is invalid if:
    #Any required field is missing.
    #Any required field is blank.
    #quantity_change is None.
    #unit_cost is None.
    #quantity_change == 0.
    #unit_cost <= 0.
    #adjustment_date is None.
    #adjustment_type is not allowed.
    #status is not allowed.
    #approved_by is blank when status is Approved.

def validate_data(stock):

    validated = []

    for column in REQUIRED_FIELDS:
        
        if column not in stock:
            validated.append (f"{column} is missing")
        
    #adjustment_id validation
    adjustment_id = stock.get("adjustment_id")

    if adjustment_id is None:
        validated.append ("adjustment_id is missing")
    elif not isinstance (adjustment_id, str):
        validated.append ("adjustment_id should be string")
    elif adjustment_id.strip() == "":
        validated.append ("adjustment_id is blank")
    
    #warehouse_id validation
    whse_id = stock.get("warehouse_id")

    if whse_id is None:
        validated.append ("warehouse_id is missing")
    elif not isinstance (whse_id, str):
        validated.append ("warehouse_id should be string")
    elif whse_id.strip() == "":
        validated.append ("warehouse_id is blank")
    
    #warehouse_name validation
    whse_name = stock.get("warehouse_name")

    if whse_name is None:
        validated.append ("warehouse_name is missing")
    elif not isinstance (whse_name, str):
        validated.append ("warehouse_name should be string")
    elif whse_name.strip() == "":
        validated.append ("warehouse_name is blank")
    
    #sku validation
    sku = stock.get("sku")

    if sku is None:
        validated.append ("sku is missing")
    elif not isinstance (sku, str):
        validated.append ("sku should be string")
    elif sku.strip() == "":
        validated.append ("sku is blank")
    
    #product_name
    product_name = stock.get("product_name")

    if product_name is None:
        validated.append ("product_name is missing")
    elif not isinstance (product_name, str):
        validated.append ("product_name should be string")
    elif product_name.strip() == "":
        validated.append ("product_name is blank")
    
    #adjustment_date validation
    adj_date = stock.get("adjustment_date")

    if adj_date is None:
        validated.append ("adjustment_date is missing")
    elif not isinstance (adj_date, date):
        validated.append ("invalid adjustment_date format")
    
    #adjustment_type validation
    adj_type = stock.get("adjustment_type")

    if adj_type is None:
        validated.append ("adjustment_type is missing")
    elif not isinstance (adj_type, str):
        validated.append ("adjustment_type should be string")
    elif adj_type.strip() == "":
        validated.append ("adjustment_type is blank")
    elif adj_type not in ALLOWED_ADJUSTMENT_TYPES:
        validated.append (f"Adjustment_type should be one of {', '.join(ALLOWED_ADJUSTMENT_TYPES)}")
    

    #quantity change validation
    qty_change = stock.get("quantity_change")

    if qty_change is None:
        validated.append ("quantity_change is missing")
    elif not isinstance (qty_change, int):
        validated.append ("quantity_change should be integer")
    elif qty_change == 0:
        validated.append ("quantity_change should not be equal to 0")
    
    #unit_cost validation
    unit_cost = stock.get("unit_cost")

    if unit_cost is None:
        validated.append ("unit_cost is missing")
    elif not isinstance (unit_cost, (float, int)):
        validated.append ("unit_cost should be a number")
    elif unit_cost <= 0:
        validated.append ("unit_cost should be greater than 0")
    

    #status validation
    status = stock.get("status")
    if status is None:
        validated.append ("status is missing")
    elif not isinstance (status, str):
        validated.append ("status should be string")
    elif status.strip() == "":
        validated.append ("status is blank")
    elif status not in ALLOWED_STATUSES:
        validated.append (f"Status should be one of {', '.join(ALLOWED_STATUSES)}")

    #approved_by validation
    #invalid if --approved_by is blank when status is Approved.
    approved_by = stock.get("approved_by")
    
    if isinstance (status, str) and status.strip().lower() == "approved":
        if approved_by is None:
            validated.append ("approved_by is missing when status is not approved")
        elif not isinstance (approved_by, str):
            validated.append ("approved by should be string")
        elif approved_by.strip() == "":
            validated.append ("approved by is blank") 
        
    
    if validated:
        return False, validated
    
    return True, []