from src.config import REQUIRED_FIELD
from src.config import ALLOWED_DELIVERY_STATUS
from src.config import ALLOWED_PRIORITY
from datetime import datetime, date

"""
-> This is a helper function for validating data in the pipeline
Numeric business rules
    quantity_ordered > 0
    quantity_received >= 0
    unit_cost > 0
    approved_budget > 0
Date validation rules
    expected_delivery_date >= order_date
    if delivery_status == "Delivered" then actual_delivery_date
        actual_delivery_date >= order_date
"""


def validate_table(procure):

    malformed = []

    for field in REQUIRED_FIELD:
        if field not in procure:
            malformed.append(f"{field} is missing")

    # validate purchase_order_id
    purchase_order_id = procure.get("purchase_order_id")
    if purchase_order_id is None:
        malformed.append("purchase_order_id is missing")

    elif not isinstance(purchase_order_id, str):
        malformed.append("purchase_order_id should be string")

    elif purchase_order_id.strip() == "":
        malformed.append("purchase_order_id is blank")

    # validate supplier_id
    supplier_id = procure.get("supplier_id")
    if supplier_id is None:
        malformed.append("supplier_id is missing")

    elif not isinstance(supplier_id, str):
        malformed.append("supplier_id should be string")

    elif supplier_id.strip() == "":
        malformed.append("supplier_id is blank")

    # validate supplier_name
    supplier_name = procure.get("supplier_name")
    if supplier_name is None:
        malformed.append("supplier_name is missing")

    elif not isinstance(supplier_name, str):
        malformed.append("supplier_name should be string")

    elif supplier_name.strip() == "":
        malformed.append("supplier_name is blank")

    # validate product_category
    product_category = procure.get("product_category")
    if product_category is None:
        malformed.append("product_category is missing")

    elif not isinstance(product_category, str):
        malformed.append("product_category should be string")

    elif product_category.strip() == "":
        malformed.append("product_category is blank")

    # validate quantity_ordered
    quantity_ordered = procure.get("quantity_ordered")
    if quantity_ordered is None:
        malformed.append("quantity_ordered is missing")

    elif not isinstance(quantity_ordered, int):
        malformed.append("quantity_ordered should be integer")

    elif quantity_ordered <= 0:
        malformed.append("quantity_ordered should be >= 0")

    # validate quantity_received
    quantity_received = procure.get("quantity_received")
    if quantity_received is None:
        malformed.append("quantity_received is missing")

    elif not isinstance(quantity_received, int):
        malformed.append("quantity_received should be integer")

    elif quantity_received < 0:
        malformed.append("quantity_received should be >= 0")

    # validate unit_cost
    unit_cost = procure.get("unit_cost")
    if unit_cost is None:
        malformed.append("unit_cost is missing")

    elif not isinstance(unit_cost, float):
        malformed.append("unit_cost should be float")

    elif unit_cost <= 0:
        malformed.append("unit_cost should be >= 0")

    # validate approved_budget
    approved_budget = procure.get("approved_budget")
    if approved_budget is None:
        malformed.append("approved_budget is missing")

    elif not isinstance(approved_budget, float):
        malformed.append("approved_budget should be float")

    elif approved_budget <= 0:
        malformed.append("approved_budget should be >= 0")

    # validate order_date
    order_date = procure.get("order_date")
    order_date_check = False
    if order_date is None:
        malformed.append("order_date is missing")

    elif not isinstance(order_date, date):
        malformed.append("order_date should be in date format")

    else:
        order_date_check = True

    # validate expected_delivery_date
    expected_delivery_date = procure.get("expected_delivery_date")
    if expected_delivery_date is None:
        malformed.append("expected_delivery_date is missing")

    elif not isinstance(expected_delivery_date, date):
        malformed.append("expected_delivery_date should be in date format")

    elif order_date_check and expected_delivery_date < order_date:
        malformed.append(
            "expected_delivery_date should be after or same day as order_date"
        )

    # validate delivery_status
    delivery_status = procure.get("delivery_status")
    delivery_status_check = False
    if delivery_status is None:
        malformed.append("delivery_status is missing")

    elif not isinstance(delivery_status, str):
        malformed.append("delivery_status should be string")

    elif delivery_status.strip() == "":
        malformed.append("delivery_status is blank")

    elif delivery_status not in ALLOWED_DELIVERY_STATUS:
        malformed.append("delivery_status should be in the delivery status list")

    else:
        delivery_status_check = True

    # validate actual_delivery_date
    actual_delivery_date = procure.get("actual_delivery_date")
    if actual_delivery_date is None:
        if delivery_status_check and delivery_status == "Delivered":
            malformed.append(
                "'delivered' delivery_status should have actual_delivery_date"
            )

    elif not isinstance(actual_delivery_date, date):
        malformed.append("actual_delivery_date should be in date format")

    elif order_date_check and actual_delivery_date < order_date:
        malformed.append("actual_delivery_date should be same as or after order_date")

    # validate priority
    priority = procure.get("priority")
    if priority is None:
        malformed.append("priority is missing")

    elif not isinstance(priority, str):
        malformed.append("priority should be string")

    elif priority.strip() == "":
        malformed.append("priority is empty")

    elif priority not in ALLOWED_PRIORITY:
        malformed.append(f"priority must be one of {' '.join(ALLOWED_PRIORITY)}")

    # return summary
    if malformed:
        return None, malformed

    else:
        return True, []
