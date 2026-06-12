import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"

load_dotenv (ENV_VAR)

def get_path (VARIABLE_NAME):

    path = os.getenv (VARIABLE_NAME)
    return path

INPUT_PATH = BASE_DIR / get_path("INPUT_PATH")

VALIDS_PATH = BASE_DIR / get_path("VALIDS_PATH")
TRANSFORMED_PATH = BASE_DIR / get_path("TRANSFORMED_PATH")
INVALIDS_PATH = BASE_DIR / get_path("INVALIDS_PATH")
SUPPLIERS_PATH = BASE_DIR / get_path("SUPPLIERS_PATH")
DEPO_PATH = BASE_DIR / get_path("DEPO_PATH")

REQUIRED_FIELDS = [
    "po_id",
    "line_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "product",
    "order_date",
    "expected_delivery_date",
    "order_status",
    "quantity_ordered",
    "quantity_received",
    "unit_cost"
]

ALLOWED_STATUS = [
    "Open",
    "Received",
    "Partially Received",
    "Cancelled"
]

OUTPUT_DELIMITER = "|"

VALIDS_COLUMNS = [
    "po_id",
    "line_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "product",
    "order_date",
    "expected_delivery_date",
    "order_status",
    "quantity_ordered",
    "quantity_received",
    "unit_cost"
]

INVALIDS_COLUMN = [
    "po_id",
    "line_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "product",
    "order_date",
    "expected_delivery_date",
    "order_status",
    "quantity_ordered",
    "quantity_received",
    "unit_cost",
    "error_reasons"
]

TRANSFORMED_COLUMN = [
    "ordered_value",
    "received_value",
    "shortage_quantity",
    "receipt_rate",
    "fulfillment_status"
]

SUPPLIERS_COLUMN = [
    "supplier_id",
    "supplier_name",
    "valid_line_count",
    "total_ordered_qty",
    "total_received_qty",
    "total_ordered_value",
    "total_received_value",
    "total_shortage_qty",
    "avg_receipt_rate"
]

DEPO_COLUMN = [
    "warehouse",
    "valid_line_count",
    "total_ordered_qty",
    "total_received_qty",
    "total_ordered_value",
    "total_received_value",
    "total_shortage_qty"
]