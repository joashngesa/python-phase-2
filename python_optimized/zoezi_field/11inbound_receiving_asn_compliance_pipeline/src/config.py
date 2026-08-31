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
