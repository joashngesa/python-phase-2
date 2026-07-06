
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"

load_dotenv(ENV_VAR)

def get_env_variable (VARIABLE_NAME):

    env_variable = os.getenv (VARIABLE_NAME)

    if env_variable is None or env_variable.strip() == "" :
        raise (f"⚠️ The variable {VARIABLE_NAME} is not found in .env 🚨")
    
    return env_variable

RAW_DIR =BASE_DIR / get_env_variable ("RAW_DIR")

INVALIDS_DIR = BASE_DIR / get_env_variable ("INVALIDS_DIR")
VALIDS_DIR = BASE_DIR / get_env_variable ("VALIDS_DIR")
SUMMARIES_DIR = BASE_DIR / get_env_variable ("SUMMARIES_DIR")
TRANSFORMED_DIR = BASE_DIR /    get_env_variable ("TRANSFORMED_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable ("QUARANTINE_DIR")

FILE_PATTERN = get_env_variable ("FILE_PATTERN") 

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
    "carrier"
]

ALLOWED_PRODUCT_CATEGORIES = [
    "Vaccines",
    "Fresh Produce",
    "Frozen Seafood",
    "Insulin",
    "Dairy",
    "Specialty Foods"
]

ALLOWED_DELIVERY_STATUSES = [
    "Delivered",
    "In Transit",
    "Delayed",
    "Rejected",
    "Returned"
]

ALLOWED_CARRIERS = [
    "ArcticMove",
    "FrostLine",
    "PolarFreight",
    "ColdRoute",
    "GlacierExpress"
]

LOSS_MULTIPLIERS = {
    "Vaccines": 120,
    "Insulin": 95,
    "Frozen Seafood": 60,
    "Fresh Produce": 35,
    "Dairy": 25,
    "Specialty Foods": 45
}