
from datetime import datetime, date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_STATUSES
from src.config import ALLOWED_REASONS

#validation rules
    #Any required field is missing.
    #Any required field is blank.
    #quantity is None.
    #unit_cost is None.
    #quantity <= 0.
    #unit_cost <= 0.
    #status is not in allowed_statuses.
    #reason is not in allowed_reasons.
    #return_date is not a real date in YYYY-MM-DD format.


def validate_data(item):

    reasons = []
    for column in REQUIRED_FIELDS:
        if column not in item:
            reasons.append(f"the field {column} is missing")
    
    #return_id
    return_id = item.get("return_id")
    if return_id is  None:
        reasons.append("return_id is missing")
    elif not isinstance (return_id, str):
        reasons.append ("return_id should be string")
    elif return_id.strip() == "":
        reasons.append ("return_id is blank")

    #vendor_id
    vendor_id = item.get("vendor_id")
    if vendor_id is None:
        reasons.append ("vendor_id is missing")
    elif not isinstance (vendor_id, str):
        reasons.append ("vendor_id should be string")
    elif vendor_id.strip() == "":
        reasons.append ("vendor_id is blank")

    #vendor_name
    vendor = item.get("vendor_name")
    if vendor is None:
        reasons.append ("vendor_name is missing")
    elif not isinstance (vendor, str):
        reasons.append ("vendor_name should be string")
    elif vendor.strip() == "":
        reasons.append ("vendor_name is blank")

    #warehouse
    w_hse = item.get("warehouse")
    if w_hse is None:
        reasons.append ("warehouse is missing")
    elif not isinstance (w_hse, str):
        reasons.append ("warehouse should be integer")
    elif w_hse.strip() == "":
        reasons.append ("warehouse is blank")

    #product_sku
    sku = item.get("product_sku")
    if sku is None:
        reasons.append ("product_sku is missing")
    elif not isinstance (sku, str):
        reasons.append ("product_sku should be string")
    elif sku.strip() == "":
        reasons.append ("product_sku is blank")

    #product_name
    product = item.get("product_name")
    if product is None:
        reasons.append ("product_name is missing")
    elif not isinstance (product, str):
        reasons.append ("product_name should be string")
    elif product.strip() == "":
        reasons.append ("product_name is blank")

    #return_date
    r_date = item.get("return_date")
    if r_date is None:
        reasons.append ("return_date is missing")
    elif not isinstance (r_date, date):
        reasons.append ("return date should be in date format")

    #reason
    reason = item.get("reason")
    if reason is None:
        reasons.append ("reasons is missing")
    elif not isinstance (reason, str):
        reasons.append ("reason should be string")
    elif reason.strip() == "":
        reasons.append ("reasons is blank")
    elif reason.strip() not in ALLOWED_REASONS:
        reasons.append (f"Reasons must be one of {', '.join(ALLOWED_REASONS)}")

    #quantity
    qty = item.get("quantity")
    if qty is None:
        reasons.append ("quantity is missing")
    elif not isinstance (qty, int):
        reasons.append ("reasons should be string")
    elif qty <= 0:
        reasons.append ("quantity should be greater than zero")

    #unit_cost
    unit_cost = item.get("unit_cost")
    if unit_cost is None:
        reasons.append ("unit_cost is missing")
    elif not isinstance (unit_cost, float):
        reasons.append ("unit_cost should be float")
    elif unit_cost <= 0:
        reasons.append ("unit_cost should be greater than zero")

    #status
    status = item.get("status")
    if status is None:
        reasons.append ("status is missing")
    elif not isinstance (status, str):
        reasons.append ("status should be string")
    elif status.strip() == "":
        reasons.append ("status is blank")
    elif status.strip() not in ALLOWED_STATUSES:
        reasons.append (f"status must be one of {', '.join(ALLOWED_STATUSES)}")
    
    if reasons:
        return False, reasons
    
    return True, []