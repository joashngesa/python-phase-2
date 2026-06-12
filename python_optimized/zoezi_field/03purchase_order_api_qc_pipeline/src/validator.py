
from datetime import datetime, date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_STATUS

def inspect_data(item):

    reasons = []

    for field in REQUIRED_FIELDS:
        if field not in item:
            reasons.append(f"the column {field} is missing")
        
    po_id = item.get("po_id")
    line_id = item.get("line_id")
    supplier_id = item.get("supplier_id")
    supplier_name = item.get("supplier_name")
    warehouse = item.get("warehouse")
    sku = item.get("sku")
    product = item.get("product")
    order_date = item.get("order_date")
    xptd_delivery_date = item.get("expected_delivery_date")
    order_status = item.get("order_status")
    qty_ordered = item.get("quantity_ordered")
    qty_received = item.get("quantity_received")
    unit_cost = item.get("unit_cost")

        #validate po_id
    if po_id is None:
        reasons.append("po_id is missing")
    elif not isinstance (po_id, str):
        reasons.append("po_id should be a string")
    elif not po_id.strip():
        reasons.append("po_id is blank")

        #validate line_id
            #line_id must be greater than 0
    if line_id is None:
        reasons.append("line_id is missing")
    elif not isinstance(line_id, int):
        reasons.append("line_id should be integer")
    elif line_id <= 0:
        reasons.append("line_id must be greater than zero")

        #validate supplier_id
    if supplier_id is None:
        reasons.append("supplier_id is missing")
    elif not isinstance (supplier_id, str):
        reasons.append("supplier_id should be string")
    elif not supplier_id.strip():
        reasons.append("supplier_id is blank")

        #supplier_name validation
    if supplier_name is None:
        reasons.append("supplier_name is missing")
    elif not isinstance (supplier_name, str):
        reasons.append ("supplier_name should be string")
    elif not supplier_name.strip():
        reasons.append ("supplier_name is blank")

        #warehouse validation
    if warehouse is None:
        reasons.append ("warehouse is missing")
    elif not isinstance (warehouse, str):
        reasons.append ("warehouse should be string")
    elif not warehouse.strip():
        reasons.append ("warehouse is blank")

        #sku validation
    if sku is None:
        reasons.append ("sku is missing")
    elif not isinstance (sku, str):
        reasons.append ("sku should be string")

        #product validation
    if product is None:
        reasons.append ("product is missing")
    elif not isinstance (product, str):
        reasons.append ("product should be string")
    elif not product.strip():
        reasons.append ("product is blank")

        #order_date validation
    if order_date is None:
        reasons.append ("order_date is absent or invalid")
    elif not isinstance (order_date, date):
        reasons.append ("invalid order_date format")

        #expected_delivery_date validation
    if xptd_delivery_date is None:
        reasons.append ("expected_delivery_date is absent or invalid")
    elif not isinstance (xptd_delivery_date, date):
        reasons. append ("invalid expected_delivery_date format")

        #order_status validation
    if order_status is None:
        reasons.append ("order_status is missing")
    elif not isinstance (order_status, str):
        reasons.append ("order_status should be string")
    elif not order_status.strip():
        reasons.append ("order_status is blank")
    elif order_status not in ALLOWED_STATUS:
        reasons.append (f"allowed_status must be one of {', '.join(ALLOWED_STATUS)}")


    #quantity_ordered must be greater than 0
        #quantity ordered validation
    if qty_ordered is None:
        reasons.append ("quantity_ordered is missing or invalid")
    elif qty_ordered <= 0:
        reasons.append ("quantity_ordered must be greater than zero")

    #quantity_received must be greater than or equal to 0
    #quantity_received cannot be greater than quantity_ordered
        #quantity_received validation
    if qty_received is None:
        reasons.append("quantity_received is missing or invalid")
    elif qty_received < 0:
        reasons.append("quantity_received must be >= 0")
    elif qty_received is not None and qty_ordered is not None and  qty_received > qty_ordered:
        reasons.append ("quantity_received cannot be greater than quantity_ordered")

    #unit_cost must be greater than 0
    #unit_cost validation
    if unit_cost is None:
        reasons.append ("unit_cost is missing or invalid")
    elif unit_cost <= 0:
        reasons.append ("unit_cost must be greater than zero")

    if reasons:
        return False, reasons
    
    return True, []