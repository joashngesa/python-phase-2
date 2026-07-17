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
