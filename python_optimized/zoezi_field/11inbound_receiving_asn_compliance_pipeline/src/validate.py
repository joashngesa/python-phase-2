"""
the below might be absent without invalidating the records:
    carrier
    dock_door
    notes
    receipt_date-> if receipt_status == Received, this seizes to be optional
Quantity validation:
    ordered_qty > 0
    shipped_qty >= 0
    received_qty >= 0
    damaged_qty >= 0
    damaged_qty <= received_qty
    unit_cost > 0
Date validation
    order_date <= ship_date
    ship_date <= receipt_date
    order_date <= promised_delivery_date
"""

from datetime import date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_RECEIPT_STATUS


def validate_data(procure):

    reason = []

    for field in REQUIRED_FIELDS:
        if field not in procure:
            reason.append(f"{field} column is missing")

    # receipt_id validation
    receipt_id = procure.get("receipt_id")
    if receipt_id is None:
        reason.append("receipt_id is missing")

    elif not isinstance(receipt_id, str):
        reason.append("receipt_id should be string")

    elif receipt_id.strip() == "":
        reason.append(f"receipt_id should be blank")

    # purchase_order_id validation
    purchase_order_id = procure.get("purchase_order_id")
    if purchase_order_id is None:
        reason.append("purchase_order_id is missing")

    elif not isinstance(purchase_order_id, str):
        reason.append("purchase_order_id should be string")

    elif purchase_order_id.strip() == "":
        reason.append("purchase_order_id is blank")

    # validate asn_id
    asn_id = procure.get("asn_id")
    if asn_id is None:
        reason.append("asn_id is missing")

    elif not isinstance(asn_id, str):
        reason.append("asn_id should be string")

    elif asn_id.strip() == "":
        reason.append("asn_id is blank")

    # validate supplier_id
    supplier_id = procure.get("supplier_id")
    if supplier_id is None:
        reason.append("supplier_id is missing")

    elif not isinstance(supplier_id, str):
        reason.append("supplier_id should be string")

    elif supplier_id.strip() == "":
        reason.append("supplier_id is blank")

    # validate supplier_name
    supplier_name = procure.get("supplier_name")
    if supplier_name is None:
        reason.append("supplier_name is missing")

    elif not isinstance(supplier_name, str):
        reason.append("supplier_name should be string")

    elif supplier_name.strip() == "":
        reason.append("supplier_name is blank")

    # validate warehouse
    warehouse = procure.get("warehouse")
    if warehouse is None:
        reason.append("warehouse is missing")

    elif not isinstance(warehouse, str):
        reason.append("warehouse should be string")

    elif warehouse.strip() == "":
        reason.append("warehouse is blank")

    # validate sku
    sku = procure.get("sku")
    if sku is None:
        reason.append("sku is missing")

    elif not isinstance(sku, str):
        reason.append("sku should be string")

    elif sku.strip() == "":
        reason.append("sku is blank")

    # validate ordered_qty
    ordered_qty = procure.get("ordered_qty")
    if ordered_qty is None:
        reason.append("ordered_qty is missing")

    elif not isinstance(ordered_qty, int):
        reason.append("ordered_qty should be integer")

    elif ordered_qty <= 0:
        reason.append("ordered_qty should not be <= 0")

    # validate shipped_qty
    shipped_qty = procure.get("shipped_qty")
    if shipped_qty is None:
        reason.append("shipped_qty is missing")

    elif not isinstance(shipped_qty, int):
        reason.append("shipped_qty should be integer")

    elif shipped_qty < 0:
        reason.append("shipped_qty should not be < 0")

    # validate received_qty
    received_qty = procure.get("received_qty")
    received_qty_check = False
    if received_qty is None:
        reason.append("received_qty is missing")

    elif not isinstance(received_qty, int):
        reason.append("received_qty should be integer")

    elif received_qty < 0:
        reason.append("received_qty should not be < 0")

    else:
        received_qty_check = True

    # validate damaged_qty
    damaged_qty = procure.get("damaged_qty")
    if damaged_qty is None:
        reason.append("damaged_qty is missing")

    elif not isinstance(damaged_qty, int):
        reason.append("damaged_qty should be integer")

    elif damaged_qty < 0:
        reason.append("damaged_qty should not be < 0")

    elif received_qty_check and damaged_qty > received_qty:
        reason.append("damaged_qty should not be > than received_qty")

    # validate unit_cost
    unit_cost = procure.get("unit_cost")
    if unit_cost is None:
        reason.append("unit_cost is missing")

    elif not isinstance(unit_cost, float):
        reason.append("unit_cost should be float")

    elif unit_cost <= 0:
        reason.append("unit_cost > 0 should not be <= 0")

    # validate receipt_status
    receipt_status = procure.get("receipt_status")
    receipt_status_check = False
    if receipt_status is None:
        reason.append("receipt_status is missing")

    elif not isinstance(receipt_status, str):
        reason.append("receipt_status should be string")

    elif receipt_status.strip() == "":
        reason.append("receipt_status is blank")

    elif receipt_status not in ALLOWED_RECEIPT_STATUS:
        reason.append(
            f"receipt_status must be one of {';'.join(ALLOWED_RECEIPT_STATUS)}"
        )

    else:
        receipt_status_check = True

    # validate receipt_date
    receipt_date = procure.get("receipt_date")
    receipt_date_check = False
    if receipt_status_check and receipt_status == "Received":
        if receipt_date is None:
            reason.append("receipt_date required when receipt_status is received")

        elif not isinstance(receipt_date, date):
            reason.append("receipt_date should be in date format")

        else:
            receipt_date_check = True

    # validate ship_date
    ship_date = procure.get("ship_date")
    ship_date_check = False
    if ship_date is None:
        reason.append("ship_date is missing")

    elif not isinstance(ship_date, date):
        reason.append("ship_date should be in date format")

    elif receipt_date_check and ship_date > receipt_date:
        reason.append("ship_date should be same/before receipt_date")

    else:
        ship_date_check = True

    # validate promised_delivery_date
    promised_delivery_date = procure.get("promised_delivery_date")
    promised_delivery_date_check = False
    if promised_delivery_date is None:
        reason.append("promised_delivery_date is missing")

    elif not isinstance(promised_delivery_date, date):
        reason.append("promised_delivery_date should be in date format")

    else:
        promised_delivery_date_check = True

    # validate order_date
    order_date = procure.get("order_date")
    if order_date is None:
        reason.append("order_date is missing")

    elif not isinstance(order_date, date):
        reason.append("promised_delivery_date should be in date format")

    elif ship_date_check and order_date > ship_date:
        reason.append("order_date should be before/ same as ship_date")

    elif promised_delivery_date_check and order_date > promised_delivery_date:
        reason.append("order_date should be before/ same as ship_date")

    # return summary
    if reason:
        return None, reason

    else:
        return True, []
