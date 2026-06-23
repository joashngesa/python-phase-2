

from datetime import datetime, date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_REASONS
from src.config import ALLOWED_STATUSES
from src.config import RETURN_DATE_ALLOWED_STATUS

def data_validation(revert):
    
    reasons = []

    for field in REQUIRED_FIELDS:
        if field not in revert:
            reasons.append(F"The column {field} is missing")

        #validate return_id
    return_id = revert.get("return_id")
    if return_id is None:
        reasons.append("the return_id is missing")
    elif not isinstance (return_id, str):
        reasons.append("the return_id should be string")
    elif not return_id.strip():
        reasons.append("the return_id is blank")

        #validate line_id
    line_id = revert.get("line_id")
    if line_id is None:
        reasons.append ("line_id is missing")
    elif not isinstance (line_id, int):
        reasons.append ("line_id is not integer")
    elif line_id <= 0:
        reasons.append ("line_id should be greater than zero")

        #validate vendor_id
    vendor_id = revert.get("vendor_id")
    if vendor_id is None:
        reasons.append ("vendor_id is missing")
    elif not isinstance (vendor_id, str):
        reasons.append ("vendor_id should be string")
    elif not vendor_id.strip():
        reasons.append ("vendor_is is blank")

        #validate vendor_name
    v_name = revert.get("vendor_name")
    if v_name is None:
        reasons.append ("vendor_name is missing")
    elif not isinstance (v_name, str):
        reasons.append ("vendor_name should be string")
    elif not v_name.strip():
        reasons.append ("vendor_name is blank")

        #validate warehouse
    w_house = revert.get("warehouse")
    if w_house is None:
        reasons.append ("warehouse is missing")
    elif not isinstance (w_house, str):
        reasons.append  ("warehouse should be string")
    elif not w_house.strip():
        reasons.append ("warehouse is blank")

        #validate sku
    sku = revert.get("sku")
    if sku is None:
        reasons.append ("sku is missing")
    elif not isinstance (sku, str):
        reasons.append ("sku should be string")
    elif not sku.strip():
        reasons.append ("sku is blank")

        #validate product
    product = revert.get("product")
    if product is None:
        reasons.append ("product is missing")
    elif not isinstance (product, str):
        reasons.append ("product should be string")
    elif not product.strip():
        reasons.append ("product is blank")

    ##Date rules
    #return_date must be a valid YYYY-MM-DD date
    #received_date must be a valid YYYY-MM-DD date if present
    #received_date cannot be earlier than return_date

        #validate return_date
    return_date = revert.get("return_date")
    return_date_valid = False
    if return_date is None:
        reasons.append ("return_date is missing")
    elif not isinstance (return_date, date):
        reasons.append ("return_date should be in date format")
    else:
        return_date_valid = True

        #validation of received_date
    received_date = revert.get("received_date")
    return_status = revert.get("return_status")
    if return_status in RETURN_DATE_ALLOWED_STATUS:
        if received_date is None:
            reasons.append (f"received_date is missing but is required when the return_status is one of {', '.join(RETURN_DATE_ALLOWED_STATUS)}")
        elif not isinstance (received_date, date):
            reasons.append ("received_date should be in date format")
        elif return_date_valid and received_date < return_date:
            reasons.append ("received_date can not be earlier than return_date")
    elif return_status == "Pending":
        if received_date not in (None, ""):
            reasons.append ("received_date must be none or blank when return_status is pending")
    else:
        if received_date not in (None, "") and not isinstance (received_date, date):
            reasons.append ("received_date should be in date format") 

        #validation of return reason
    return_reason = revert.get("return_reason")
    if return_reason is None:
        reasons.append ("return_reason is missng")
    elif not isinstance (return_reason, str):
        reasons.append ("return_reason should be string")
    elif not return_reason.strip():
        reasons.append ("return_reason is blank")
    elif return_reason not in ALLOWED_REASONS:
        reasons.append (f"return_reason must be one of {', '.join(ALLOWED_REASONS)}") 

        #validate return_status
    if return_status is None:
        reasons.append ("return_status is missing")
    elif not isinstance (return_status, str):
        reasons.append ("return_status should be string")
    elif not return_status.strip():
        reasons.append ("return_status is blank")
    elif return_status not in ALLOWED_STATUSES:
        reasons.append (f"return_status must be one of {', '.join(ALLOWED_STATUSES)}")

    ##Numeric rules
    #line_id > 0
    #quantity_returned > 0
    #quantity_accepted >= 0
    #quantity_accepted <= quantity_returned
    #unit_cost > 0

        #validate quantity_returned
    qty_returned = revert.get("quantity_returned")
    if qty_returned is None:
        reasons.append ("quantity_returned is missing")
    elif not isinstance (qty_returned, int):
        reasons.append ("quantity_returned should be integer")
    elif qty_returned <= 0:
        reasons.append ("quantity_returned should be greater than zero")

        #validate quantity_accepted
    qty_accepted = revert.get("quantity_accepted")
    if qty_accepted is None:
        reasons.append ("quantity_accepted is missing")
    elif not isinstance (qty_accepted, int):
        reasons.append ("quantity_accpeted should be integer")
    elif qty_accepted < 0:
        reasons.append ("quantity_accpeted should be greater or equal to zero")
    elif qty_accepted > qty_returned:
        reasons.append ("quantity_accepted should be less than or equal to quantity_returned")

        #validate unit_cost
    unit_cost = revert.get("unit_cost")
    if unit_cost is None:
        reasons.append ("unit_cost is missing")
    elif not isinstance (unit_cost, float):
        reasons.append ("unit_cost should be float")
    elif unit_cost <= 0:
        reasons.append ("unit_cost should be greater than zero")

    if reasons:
        return False, reasons
    
    return True, []