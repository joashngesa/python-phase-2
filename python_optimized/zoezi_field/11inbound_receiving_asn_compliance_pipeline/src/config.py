import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variables(ENVIRONMENT_VARIABLE):

    env_var = os.getenv(ENVIRONMENT_VARIABLE)

    if env_var is None or env_var.strip() == "":
        raise ValueError(f"{ENVIRONMENT_VARIABLE} not found in .env.config")

    return env_var


INPUT_DIR = BASE_DIR / get_env_variables("INPUT_DIR")
VALID_DIR = BASE_DIR / get_env_variables("VALID_DIR")
INVALID_DIR = BASE_DIR / get_env_variables("INVALID_DIR")
DUPLICATES_DIR = BASE_DIR / get_env_variables("DUPLICATES_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variables("QUARANTINE_DIR")
SUMMARIES_DIR = BASE_DIR / get_env_variables("SUMMARIES_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variables("TRANSFORMED_DIR")
RUN_SUMMARIES_DIR = BASE_DIR / get_env_variables("RUN_SUMMARIES_DIR")

LOG_FOLDER = BASE_DIR / "logs"
LOG_FILE = LOG_FOLDER / "inbounds_pipeline.log"

OUTPUT_DELIMITER = "|"
PIPELINE_NAME = "Inbound_receiving_asn_compliance_pipeline"

FILE_PATTERN = get_env_variables("FILE_PATTERN")

REQUIRED_FIELDS = [
    "receipt_id",
    "purchase_order_id",
    "asn_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "ordered_qty",
    "shipped_qty",
    "received_qty",
    "unit_cost",
    "order_date",
    "promised_delivery_date",
    "ship_date",
    "receipt_status",
]

ALLOWED_RECEIPT_STATUS = [
    "Received",
    "Partial",
    "Rejected",
]

VALID_COLUMNS = [
    "receipt_id",
    "purchase_order_id",
    "asn_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "ordered_qty",
    "shipped_qty",
    "received_qty",
    "damaged_qty",
    "unit_cost",
    "order_date",
    "promised_delivery_date",
    "ship_date",
    "receipt_date",
    "receipt_status",
    "carrier",
    "dock_door",
    "notes",
]

INVALID_COLUMNS = [
    "receipt_id",
    "purchase_order_id",
    "asn_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "ordered_qty",
    "shipped_qty",
    "received_qty",
    "damaged_qty",
    "unit_cost",
    "order_date",
    "promised_delivery_date",
    "ship_date",
    "receipt_date",
    "receipt_status",
    "carrier",
    "dock_door",
    "notes",
    "error_reasons",
]

DUPLICATES_COLUMNS = [
    "receipt_id",
    "purchase_order_id",
    "asn_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "ordered_qty",
    "shipped_qty",
    "received_qty",
    "damaged_qty",
    "unit_cost",
    "order_date",
    "promised_delivery_date",
    "ship_date",
    "receipt_date",
    "receipt_status",
    "carrier",
    "dock_door",
    "notes",
    "duplicates",
]

TRANSFORMED_COLUMNS = [
    "receipt_id",
    "purchase_order_id",
    "asn_id",
    "supplier_id",
    "supplier_name",
    "warehouse",
    "sku",
    "ordered_qty",
    "shipped_qty",
    "received_qty",
    "damaged_qty",
    "unit_cost",
    "order_date",
    "promised_delivery_date",
    "ship_date",
    "receipt_date",
    "receipt_status",
    "carrier",
    "dock_door",
    "notes",
    "ordered_value",
    "received_value",
    "quantity_variance",
    "fill_rate_pct",
    "damaged_rate_pct",
    "delivery_variance",
    "delivery_performance",
    "received_performance",
    "compliance_status",
]

SUPPLIER_DIGEST_COLUMNS = [
    "supplier_id",
    "supplier_name",
    "receipt_count",
    "tot_ordered_qty",
    "tot_received_qty",
    "tot_ordered_value",
    "tot_received_value",
    "tot_damaged_qty",
    "average_fill_rate_pct",
    "damage_rate_pct",
    "late_receipt_count",
    "compliant_receipt_count",
]

WAREHOUSE_DIGEST_COLUMNS = [
    "warehouse",
    "receipts_count",
    "tot_ordered_qty",
    "tot_received_qty",
    "tot_damaged_qty",
    "fill_rate_pct",
    "damage_rate_pct",
    "late_receipts",
]

FILE_METRICS_COLUMN = [
    "run_id",
    "file_name",
    "status",
    "raw_count",
    "valid_count",
    "invalid_count",
    "duplicate_count",
    "transformed_count",
    "supplier_digest_count",
    "warehouse_digest_count",
    "error_type",
    "error_message",
    "duration",
]

PIPELINE_METRICS_COLUMN = [
    "run_id",
    "total_files",
    "succesful_files",
    "failed_files",
    "pipeline_status",
    "total_raw_records",
    "total_valid_records",
    "total_invalid_records",
    "total_duplicates_records",
    "total_transformed_records",
    "total_summary_count",
]
