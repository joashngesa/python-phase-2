# 🚦validation rules
# Any required field is missing.
# Any required field is blank.
# Any conversion error exists.
# port is not allowed.
# product_category is not allowed.
# container_type is not allowed.
# inspection_status is not allowed.
# transport_mode is not allowed.
# declared_value_usd <= 0.
# container_weight_kg <= 0.
# Any date field has invalid format.
# customs_release_date < arrival_date.
# warehouse_eta < customs_release_date.
# actual_warehouse_arrival < arrival_date.
# arrival_date > generated_at date.

from datetime import datetime, date

from src.config import REQUIRED_FIELDS
from src.config import ALLOWED_PORTS
from src.config import ALLOWED_PRODUCT_CATEGORIES
from src.config import ALLOWED_CONTAINER_TYPES
from src.config import ALLOWED_INSPECTION_STATUSES
from src.config import ALLOWED_TRANSPORT_MODES


def validate_table(event):
    """
    this is a helper function of invalid & valid_raw modules, it
    inspects the table table with the prescribed validation rules
    and adds to error reasons columns on invalid table
    """

    anomaly = []

    for field in REQUIRED_FIELDS:
        if field not in event:
            anomaly.append(f"{field} is missing")

    # validate event_id
    event_id = event.get("event_id")
    if event_id is None:
        anomaly.append("event_id is missing / blank")

    elif not isinstance(event_id, str):
        anomaly.append("event_id should be a string")

    elif event_id.strip() == "":
        anomaly.append("event_id is blank")

    # validate container_id
    container_id = event.get("container_id")
    if container_id is None:
        anomaly.append("container_id is missing/ blank")

    elif not isinstance(container_id, str):
        anomaly.append("container_id should be a string")

    elif container_id.strip() == "":
        anomaly.append("container_id is blank")

    # validate port
    port = event.get("port")
    if port is None:
        anomaly.append("port is missing / blank")

    elif not isinstance(port, str):
        anomaly.append("port should be string")

    elif port.strip() == "":
        anomaly.append("port is blank")

    elif port not in ALLOWED_PORTS:
        anomaly.append("port missing from the required port list")

    # validate warehouse_id
    warehouse_id = event.get("warehouse_id")
    if warehouse_id is None:
        anomaly.append("warehouse_id is missing / blank")

    elif not isinstance(warehouse_id, str):
        anomaly.append("warehouse_id should be string")

    elif warehouse_id.strip() == "":
        anomaly.append("warehouse_id is blank")

    # validate supplier_name
    supplier = event.get("supplier_name")
    if supplier is None:
        anomaly.append("supplier_name is missing / blank")

    elif not isinstance(supplier, str):
        anomaly.append("supplier_name should be string")

    elif supplier.strip() == "":
        anomaly.append("supplier_name is blank")

    # validate product_category
    product_category = event.get("product_category")
    if product_category is None:
        anomaly.append("product_category is missing / blank")

    elif not isinstance(product_category, str):
        anomaly.append("product_category should be string")

    elif product_category.strip() == "":
        anomaly.append("product_category is blank")

    elif product_category not in ALLOWED_PRODUCT_CATEGORIES:
        anomaly.append("product_category must be in the allowed list")

    # validate container_type
    container_type = event.get("container_type")
    if container_type is None:
        anomaly.append("container_type is missing / blank")

    elif not isinstance(container_type, str):
        anomaly.append("container_type should be string")

    elif container_type.strip() == "":
        anomaly.append("container_type is blank")

    elif container_type not in ALLOWED_CONTAINER_TYPES:
        anomaly.append("container_type must be in the allowed list")

    # validate arrival_date
    arrival_date = event.get("arrival_date")
    generate_date = event.get("processed_at")
    arrival_date_check = False
    if arrival_date is None:
        anomaly.append("arrival_date is missing / blank")

    elif not isinstance(arrival_date, date):
        anomaly.append("arrival_date must be valid date")

    elif generate_date is None:
        anomaly.append("the generated date is missing or blank")

    elif not isinstance(generate_date, (datetime, date)):
        anomaly.append("processed_at must be valid datetime or time")

    else:
        if isinstance(generate_date, datetime):
            processed_at = generate_date.date()

        else:
            processed_at = generate_date

        if arrival_date > processed_at:
            anomaly.append("the arrival_date can not be after the processing date")

        else:
            arrival_date_check = True

    # validate customs_release_date
    customs_release_date = event.get("customs_release_date")
    customs_date_check = False
    if customs_release_date is None:
        anomaly.append("customs_release_date is missing / blank")

    elif not isinstance(customs_release_date, date):
        anomaly.append("customs_release_date should be a valid date")

    elif arrival_date_check and customs_release_date < arrival_date:
        anomaly.append("customs_release_date can not be before arrival_date")

    else:
        customs_date_check = True

    # validate warehouse_eta
    warehouse_eta = event.get("warehouse_eta")
    warehouse_eta_check = False
    if warehouse_eta is None:
        anomaly.append("warehouse_eta is missing or blank")

    elif not isinstance(warehouse_eta, date):
        anomaly.append("warehouse_eta should be valid date")

    elif customs_date_check and warehouse_eta < customs_release_date:
        anomaly.append("warehouse_eta can not be before customs_release_date")

    else:
        warehouse_eta_check = True

    # validate actual_warehouse_arrival
    warehouse_arrival = event.get("actual_warehouse_arrival")
    if warehouse_arrival is None:
        anomaly.append("actual_warehouse_arrival is missing or blank")

    elif not isinstance(warehouse_arrival, date):
        anomaly.append("actual_warehouse_arrival should be valid date")

    elif arrival_date_check and warehouse_arrival < arrival_date:
        anomaly.append("actual_warehouse_arrival can not be before arrival_date")

    # validate declared_value_usd
    declared_value = event.get("declared_value_usd")
    if declared_value is None:
        anomaly.append("declared_value_usd is missing/blank")

    elif not isinstance(declared_value, float):
        anomaly.append("declared_value_usd should be float")

    elif declared_value <= 0:
        anomaly.append("declared_value_usd should be > 0")

    # validate container_weight_kg
    container_weight = event.get("container_weight_kg")
    if container_weight is None:
        anomaly.append("container_weight_kg is missing/blank")

    elif not isinstance(container_weight, float):
        anomaly.append("container_weight_kg should be float")

    elif container_weight <= 0:
        anomaly.append("container_weight_kg should be > 0")

    # validate inspection_status
    inspection_status = event.get("inspection_status")
    if inspection_status is None:
        anomaly.append("inspection_status is missing")

    elif not isinstance(inspection_status, str):
        anomaly.append("inspection_status should be a string")

    elif inspection_status.strip() == "":
        anomaly.append("inspection_status is blank")

    elif inspection_status not in ALLOWED_INSPECTION_STATUSES:
        anomaly.append("inspection_status must be in the inspection_status list")

    # validate transport_mode
    transport_mode = event.get("transport_mode")
    if transport_mode is None:
        anomaly.append("transport_mode is missing")

    elif not isinstance(transport_mode, str):
        anomaly.append("transport_mode should be string")

    elif transport_mode.strip() == "":
        anomaly.append("transport_mode is blank")

    elif transport_mode not in ALLOWED_TRANSPORT_MODES:
        anomaly.append("transport_mode must be in the transport_mode list")

    if anomaly:
        return False, anomaly

    return True, []
