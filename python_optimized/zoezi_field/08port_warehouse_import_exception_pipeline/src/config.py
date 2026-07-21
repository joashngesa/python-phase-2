import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variable(VARIABLE_NAME):
    """
    used to retrieve the environment variables saved in .env.config
    """
    var_name = os.getenv(VARIABLE_NAME)

    if var_name is None or var_name.strip() == "":
        raise ValueError(
            f"⁉️ the variable {VARIABLE_NAME} is not found in .env.config ⚠️"
        )

    return var_name


INPUT_DIR = BASE_DIR / get_env_variable("INPUT_DIR")

VALID_DIR = BASE_DIR / get_env_variable("VALID_DIR")
INVALID_DIR = BASE_DIR / get_env_variable("INVALID_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable("QUARANTINE_DIR")
FILE_SUMMARY_DIR = BASE_DIR / get_env_variable("FILE_SUMMARY_DIR")
RUN_SUMMARY_DIR = BASE_DIR / get_env_variable("RUN_SUMMARY_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")

FILE_PATTERN = get_env_variable("FILE_PATTERN")
OUTPUT_DELIMITER = "|"

REQUIRED_FIELDS = [
    "event_id",
    "container_id",
    "port",
    "warehouse_id",
    "supplier_name",
    "product_category",
    "container_type",
    "arrival_date",
    "customs_release_date",
    "warehouse_eta",
    "actual_warehouse_arrival",
    "declared_value_usd",
    "container_weight_kg",
    "inspection_status",
    "transport_mode",
]

ALLOWED_PORTS = ["Vancouver", "Halifax", "Montreal", "Prince Rupert"]

ALLOWED_PRODUCT_CATEGORIES = [
    "Electronics",
    "Auto Parts",
    "Apparel",
    "Food Ingredients",
    "Medical Supplies",
    "Industrial Equipment",
]

ALLOWED_CONTAINER_TYPES = ["Dry", "Reefer", "Open Top", "Flat Rack"]

ALLOWED_INSPECTION_STATUSES = ["Released", "Held", "Inspection Required", "Rejected"]

ALLOWED_TRANSPORT_MODES = ["Rail", "Truck", "Intermodal"]

VALID_COLUMNS = [
    "event_id",
    "container_id",
    "port",
    "warehouse_id",
    "supplier_name",
    "product_category",
    "container_type",
    "arrival_date",
    "customs_release_date",
    "warehouse_eta",
    "actual_warehouse_arrival",
    "declared_value_usd",
    "container_weight_kg",
    "inspection_status",
    "transport_mode",
    "processed_at",
    "source_file",
]

INVALID_COLUMNS = [
    "event_id",
    "container_id",
    "port",
    "warehouse_id",
    "supplier_name",
    "product_category",
    "container_type",
    "arrival_date",
    "customs_release_date",
    "warehouse_eta",
    "actual_warehouse_arrival",
    "declared_value_usd",
    "container_weight_kg",
    "inspection_status",
    "transport_mode",
    "processed_at",
    "source_file",
    "error_reasons",
]

DUPLICATES_COLUMNS = [
    "event_id",
    "container_id",
    "port",
    "warehouse_id",
    "supplier_name",
    "product_category",
    "container_type",
    "arrival_date",
    "customs_release_date",
    "warehouse_eta",
    "actual_warehouse_arrival",
    "declared_value_usd",
    "container_weight_kg",
    "inspection_status",
    "transport_mode",
    "processed_at",
    "source_file",
    "error_reasons",
]

TRANSFORMED_COLUMNS = [
    "event_id",
    "container_id",
    "port",
    "warehouse_id",
    "supplier_name",
    "product_category",
    "container_type",
    "arrival_date",
    "customs_release_date",
    "warehouse_eta",
    "actual_warehouse_arrival",
    "declared_value_usd",
    "container_weight_kg",
    "inspection_status",
    "transport_mode",
    "processed_at",
    "source_file",
    "customs_clearance_days",
    "warehouse_delays_days",
    "value_band",
    "weight_band",
    "exception_types",
    "risk_score",
    "risk_level",
]

FILE_METRICS_COLUMNS = [
    "file_name",
    "port",
    "batch_id",
    "processing_status",
    "raw_count",
    "valid_count",
    "invalid_count",
    "duplicate_count",
    "transformed_count",
    "error_type",
    "error_message",
]

TBL_SUMMARY_COLUMNS = [
    "port",
    "product_category",
    "exception_type",
    "risk_level",
    "container_count",
    "total_declared_value_usd",
    "total_container_weight_kg",
    "avg_customs_clearance_days",
    "avg_warehouse_delay_days",
]

PIPELINE_METRICS_COLUMNS = [
    "total_files",
    "successful_files",
    "failed_files",
    "total_raw_records",
    "total_valid_records",
    "total_invalid_records",
    "total_duplicate_records",
    "total_transformed_records",
]
