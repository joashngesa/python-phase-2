import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"

load_dotenv(ENV_VAR)

def get_path(VARIABLE_NAME):
    file_path = os.getenv(VARIABLE_NAME)
    return file_path

INPUT_PATH = BASE_DIR / get_path("INPUT_PATH")

INVALIDS_PATH = BASE_DIR / get_path("INVALIDS_PATH")
VALIDS_PATH = BASE_DIR / get_path("VALIDS_PATH")
TRANSFORMED_PATH = BASE_DIR / get_path("TRANSFORMED_PATH")
VENDORS_PATH = BASE_DIR / get_path("VENDORS_PATH")
REASONS_PATH = BASE_DIR / get_path("REASONS_PATH")
OUTPUT_SUMMARY_PATH = BASE_DIR / get_path("OUTPUT_SUMMARY_PATH") 

RETURN_DATE_ALLOWED_STATUS = ["Received", "Rejected", "Closed"]

REQUIRED_FIELDS = [
    "return_id",
    "line_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "sku",
    "product",
    "return_date",
    "received_date",
    "return_reason",
    "return_status",
    "quantity_returned",
    "quantity_accepted",
    "unit_cost"
]

ALLOWED_REASONS = [
    "Damaged",
    "Wrong Item",
    "Quality Issue",
    "Overstock"
]

ALLOWED_STATUSES = [
    "Pending",
    "Received",
    "Rejected",
    "Closed"
]

INVALIDS_COLUMNS = [
    "return_id",
    "line_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "sku",
    "product",
    "return_date",
    "received_date",
    "return_reason",
    "return_status",
    "quantity_returned",
    "quantity_accepted",
    "unit_cost",
    "error_reasons"
]

VALIDS_COLUMNS = [
    "return_id",
    "line_id",
    "vendor_id",
    "vendor_name",
    "warehouse",
    "sku",
    "product",
    "return_date",
    "received_date",
    "return_reason",
    "return_status",
    "quantity_returned",
    "quantity_accepted",
    "unit_cost"
]

TRANSFORMED_COLUMNS = [
    "return value",
    "accepted value",
    "rejected quantity",
    "acceptance rate",
    "processing days",
    "resolution status"
]

VENDORS_COLUMNS = [
                "vendor_id",
                "vendor_name",
                "valid_line_count",
                "total_returned_qty",
                "total_accepted_qty",
                "total_rejected_qty",
                "total_return_value",
                "total_accepted_value",
                "avg_acceptance_rate"
            ]

OUTPUT_SUMMARY_COLUMNS = [
    "source",
    "status",
    "generated_at",
    "record_count",
    "batch_id",
    "extracted_record_count",
    "valids_record_count",
    "invalids_record_count",
    "transformed_record_count",
    "vendors_record_count",
    "reasons_record_count"
]