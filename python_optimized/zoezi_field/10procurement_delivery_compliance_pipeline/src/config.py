from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variable(VARIABLE_NAME):

    env_variable = os.getenv(VARIABLE_NAME)

    if env_variable is None or env_variable.strip() == "":
        raise ValueError(f"the variable {VARIABLE_NAME} is not found in .env.config")

    return env_variable


INPUT_DIR = BASE_DIR / get_env_variable("INPUT_DIR")
VALID_DIR = BASE_DIR / get_env_variable("VALID_DIR")
INVALID_DIR = BASE_DIR / get_env_variable("INVALID_DIR")
DUPLICATES_DIR = BASE_DIR / get_env_variable("DUPLICATES_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable("QUARANTINE_DIR")
RUN_SUMMARY_DIR = BASE_DIR / get_env_variable("RUN_SUMMARY_DIR")
SUMMARY_DIR = BASE_DIR / get_env_variable("SUMMARY_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "procurement_pipeline.log"

FILE_PATTERN = get_env_variable("FILE_PATTERN")
PIPELINE_NAME = "procurement_delivery_compliance pipeline"

REQUIRED_FIELD = [
    "purchase_order_id",
    "supplier_id",
    "supplier_name",
    "product_category",
    "quantity_ordered",
    "unit_cost",
    "approved_budget",
    "order_date",
    "expected_delivery_date",
    "delivery_status",
    "priority",
]

ALLOWED_DELIVERY_STATUS = [
    "Delivered",
    "In Transit",
    "Delayed",
    "Cancelled",
]

ALLOWED_PRIORITY = [
    "Low",
    "Medium",
    "High",
    "Critical",
]
