import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variable(VARIABLE_NAME):

    env_variable = os.getenv(VARIABLE_NAME)

    if env_variable is None or env_variable.strip() == "":
        raise (f"⚠️ The variable {VARIABLE_NAME} is not found in .env 🚨")

    return env_variable


RAW_DIR = BASE_DIR / get_env_variable("RAW_DIR")

INVALIDS_DIR = BASE_DIR / get_env_variable("INVALIDS_DIR")
VALIDS_DIR = BASE_DIR / get_env_variable("VALIDS_DIR")
SUMMARIES_DIR = BASE_DIR / get_env_variable("SUMMARIES_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable("QUARANTINE_DIR")

FILE_PATTERN = get_env_variable("FILE_PATTERN")

OUTPUT_DELIMITER = "|"

REQUIRED_FIELDS = [
    "incident_id",
    "shipment_id",
    "warehouse_id",
    "product_category",
    "product_name",
    "required_temp_min_c",
    "required_temp_max_c",
    "actual_temp_c",
    "exposure_minutes",
    "incident_date",
    "delivery_status",
    "carrier",
]

ALLOWED_PRODUCT_CATEGORIES = [
    "Vaccines",
    "Fresh Produce",
    "Frozen Seafood",
    "Insulin",
    "Dairy",
    "Specialty Foods",
]

ALLOWED_DELIVERY_STATUSES = [
    "Delivered",
    "In Transit",
    "Delayed",
    "Rejected",
    "Returned",
]

ALLOWED_CARRIERS = [
    "ArcticMove",
    "FrostLine",
    "PolarFreight",
    "ColdRoute",
    "GlacierExpress",
]

LOSS_MULTIPLIERS = {
    "Vaccines": 120,
    "Insulin": 95,
    "Frozen Seafood": 60,
    "Fresh Produce": 35,
    "Dairy": 25,
    "Specialty Foods": 45,
}

VALID_COLUMNS = [
    "incident_id",
    "shipment_id",
    "warehouse_id",
    "product_category",
    "product_name",
    "required_temp_min_c",
    "required_temp_max_c",
    "actual_temp_c",
    "exposure_minutes",
    "incident_date",
    "delivery_status",
    "carrier",
    "processed_at",
    "source_file",
]

INVALID_COLUMNS = [
    "incident_id",
    "shipment_id",
    "warehouse_id",
    "product_category",
    "product_name",
    "required_temp_min_c",
    "required_temp_max_c",
    "actual_temp_c",
    "exposure_minutes",
    "incident_date",
    "delivery_status",
    "carrier",
    "processed_at",
    "source_file",
    "error_reasons",
]

TRANSFORMED_COLUMNS = [
    "incident_id",
    "shipment_id",
    "warehouse_id",
    "product_category",
    "product_name",
    "required_temp_min_c",
    "required_temp_max_c",
    "actual_temp",
    "exposure_minutes",
    "incident_date",
    "delivery_status",
    "carrier",
    "temp_breach_type",
    "temperature_deviation_c",
    "risk_level",
    "estimated_loss_value",
]

OUTPUT_COLUMNS = [
    "file_name",
    "status",
    "raw_count",
    "valid_count",
    "invalid_count",
    "transformed_count",
    "error_type",
    "error_message",
]

RUN_SUMMARY_COLUMNS = [
    "batch_status",
    "files_discovered",
    "files_succeeded",
    "files_failed",
    "total_raw_count",
    "total_valid_count",
    "total_invalid_count",
    "total_transformed_count",
]
