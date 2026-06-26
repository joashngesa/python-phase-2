import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"

load_dotenv(ENV_VAR)

def get_env_variable(VARIABLE_NAME):

    ENV_VARIABLE = os.getenv (VARIABLE_NAME)

    if ENV_VARIABLE is None or ENV_VARIABLE.strip() == "":
        raise ValueError (f"🚨 The {VARIABLE_NAME} was not found in .env")
    
    return ENV_VARIABLE
    
RAW_DIR = BASE_DIR / get_env_variable("RAW_DIR")
VALIDS_DIR = BASE_DIR / get_env_variable("VALIDS_DIR")
INVALIDS_DIR = BASE_DIR / get_env_variable("INVALIDS_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")
SUMMARY_DIR = BASE_DIR / get_env_variable("SUMMARY_DIR")
ARCHIVE_DIR = BASE_DIR / get_env_variable("ARCHIVE_DIR")
REJECTED_DIR = BASE_DIR / get_env_variable("REJECTED_DIR")

FILE_PATTERN = get_env_variable("FILE_PATTERN")

REQUIRED_FIELDS = [
    "adjustment_id",
    "warehouse_id",
    "warehouse_name",
    "sku",
    "product_name",
    "adjustment_date",
    "adjustment_type",
    "quantity_change",
    "unit_cost",
    "approved_by",
    "status"
]

ALLOWED_STATUSES = [
    "Approved",
    "Pending Review",
    "Rejected"
]

ALLOWED_ADJUSTMENT_TYPES = [
    "Damage",
    "Cycle Count",
    "Shrinkage",
    "Found Inventory",
    "Return To Stock"
]

VALIDS_COLUMN = [
    "adjustment_id",
    "warehouse_id",
    "warehouse_name",
    "sku",
    "product_name",
    "adjustment_date",
    "adjustment_type",
    "quantity_change",
    "unit_cost",
    "approved_by",
    "status",
    "source_file",
    "processed_at"
]

INVALIDS_COLUMN = [
    "adjustment_id",
    "warehouse_id",
    "warehouse_name",
    "sku",
    "product_name",
    "adjustment_date",
    "adjustment_type",
    "quantity_change",
    "unit_cost",
    "approved_by",
    "status",
    "source_file",
    "processed_at",
    "error_reasons"
]

TRANSFORMED_COLUMN = [
    "adjustment_id",
    "warehouse_id",
    "warehouse_name",
    "sku",
    "product_name",
    "adjustment_date",
    "adjustment_type",
    "quantity_change",
    "unit_cost",
    "approved_by",
    "status",
    "inventory_value_impact",
    "impact_direction",
    "impact_band",
    "source_file",
    "processed_at"
]

SUMMARY_COLUMNS = [
    "warehouse_id",
    "warehouse_name",
    "record_count",
    "total_positive_impact",
    "total_negative_impact",
    "net_inventory_value_impact",
    "increase_count",
    "decrease_count",
    "high_impact_count",
    "medium_impact_count",
    "low_impact_count",
    "source_file",
    "processed_at"
]