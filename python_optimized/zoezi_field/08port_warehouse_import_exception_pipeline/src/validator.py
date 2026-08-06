# date validation rules
# customs_release_date cannot be before arrival_date
# warehouse_eta cannot be before customs_release_date
# actual_warehouse_arrival cannot be before arrival_date
# arrival_date cannot be after generated_at date

# validation rules
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
    and adds to error reasons columns in invalid rows
    """

    anomaly = []

    for field in REQUIRED_FIELDS:
        if field not in event:
            anomaly.append(f"{field} is missing")

    # validate event_id
    event_id = event.get("event_id")
    if event_id is None:
        anomaly.append("event_id is missing")

    elif not isinstance(event_id, str):
        anomaly.append("event_id should be a string")

    elif event_id.strip() == "":
        anomaly.append("event_id is blank")

    # validate container_id
    container_id = event.get("container_id")
    if container_id is None:
        anomaly.append("container_id is missing")

    elif not isinstance(container_id, str):
        anomaly.append("container_id should be a string")

    elif container_id.strip() == "":
        anomaly.append("container_id is blank")

    # validate port
    port = event.get("port")
    if port is None:
        anomaly.append("port is missing")

    elif not isinstance(port, str):
        anomaly.append("port should be string")

    elif port.strip() == "":
        anomaly.append("port is blank")

    elif port not in ALLOWED_PORTS:
        anomaly.append("port missing from the required port list")

    # validate warehouse_id
    warehouse_id = event.get("warehouse_id")
    if warehouse_id is None:
        anomaly.append("warehouse_id is missing")

    elif not isinstance(warehouse_id, str):
        anomaly.append("warehouse_id should be string")

    elif warehouse_id.strip() == "":
        anomaly.append("warehouse_id is blank")

    # validate supplier_name
    supplier = event.get("supplier_name")
    if supplier is None:
        anomaly.append("supplier_name is missing")

    if not isinstance(supplier, str):
        anomaly.append("supplier_name should be string")

    if supplier.strip() == "":
        anomaly.append("supplier_name is blank")

    # validate product_category
    product_category = event.get("product_category")
    if product_category is None:
        anomaly.append("product_category is missing")

    elif not isinstance(product_category, str):
        anomaly.append("product_category should be string")

    elif product_category.strip() == "":
        anomaly.append("product_category is blank")

    elif product_category not in ALLOWED_PRODUCT_CATEGORIES:
        anomaly.append("product_category must be in the allowed list")

    # validate container_type
    container_type = event.get("container_type")
    if container_type is None:
        anomaly.append("container_type is missing")

    elif not isinstance(container_type, str):
        anomaly.append("container_type should be string")

    elif container_type.strip() == "":
        anomaly.append("container_type is blank")

    elif container_type not in ALLOWED_CONTAINER_TYPES:
        anomaly.append("container_type must be in the allowed list")

    # validate arrival date
    arrival_date = event.get("arrival_date")
    if arrival_date is None:
        anomaly.append("arrival_date is missing")

    elif not isinstance(arrival_date, date):
        anomaly.append("arrival date must be valid date")

    # customs_release_date validation
    customs_release_date = event.get("customs_release_date")
    if customs_release_date is None:
        anomaly.append("customs_release_date is missing")

    elif not isinstance(customs_release_date, date):
        anomaly.append("customs_release_date must be valid date")
