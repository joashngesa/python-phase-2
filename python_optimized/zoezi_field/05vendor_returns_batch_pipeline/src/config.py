import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"

load_dotenv(ENV_VAR)

def get_path(VARIABLE_NAME):
    path_name = os.getenv(VARIABLE_NAME)

    if path_name is None or path_name.strip() == "":
        raise ValueError (f"{path_name} was not found in .env")
    
    return path_name

RAW_DIR = BASE_DIR / get_path("RAW_DIR")

VALIDS_DIR = BASE_DIR / get_path("VALIDS_DIR")
INVALIDS_DIR = BASE_DIR /get_path("INVALIDS_DIR")
TRANSFORMED_DIR = BASE_DIR / get_path("TRANSFORMED_DIR")
SUMMARY_DIR = BASE_DIR / get_path("SUMMARY_DIR")

FILE_PATTERN = get_path("FILE_PATTERN")


REQUIRED_FIELDS = [
    "return_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "product_sku",
    "product_name",
    "return_date",
    "reason",
    "quantity",
    "unit_cost",
    "status"
]

ALLOWED_STATUSES = [
    "Received",
    "Pending",
    "Rejected"
]

ALLOWED_REASONS = [
    "Damaged",
    "Customer Return",
    "Wrong Item",
    "Defective",
    "Expired"
]

INVALIDS_COLUMNS = [
    "return_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "product_sku",
    "product_name",
    "return_date",
    "reason",
    "quantity",
    "unit_cost",
    "status",
    "error_reasons"
]

VALIDS_COLUMNS = [
    "return_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "product_sku",
    "product_name",
    "return_date",
    "reason",
    "quantity",
    "unit_cost",
    "status"
]

TRANSFORMED_COLUMNS = [
    "return_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "product_sku",
    "product_name",
    "return_date",
    "reason",
    "quantity",
    "unit_cost",
    "return_value",
    "return_band",
    "status"
]

SUMMARY_COLUMNS = [
    "vendor_id",
    "vendor_name",
    "record_count",
    "total_return_value",
    "avg_return_value",
    "high_value_count",
    "medium_value_count",
    "low_value_count"
]