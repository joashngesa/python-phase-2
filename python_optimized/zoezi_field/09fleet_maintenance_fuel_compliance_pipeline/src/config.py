import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variable(VARIABLE_NAME):

    env_variable = os.getenv(VARIABLE_NAME)

    if env_variable is None or env_variable.strip() == "":
        raise ValueError(f"⛔ The variable {VARIABLE_NAME} is not found in .env.config")

    return env_variable


INPUT_DIR = BASE_DIR / get_env_variable("INPUT_DIR")
VALID_DIR = BASE_DIR / get_env_variable("VALID_DIR")
INVALID_DIR = BASE_DIR / get_env_variable("INVALID_DIR")
DUPLICATES_DIR = BASE_DIR / get_env_variable("DUPLICATES_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable("QUARANTINE_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")
RUN_SUMMARY_DIR = BASE_DIR / get_env_variable("RUN_SUMMARY_DIR")
DEPOT_SUMMARY_DIR = BASE_DIR / get_env_variable("DEPOT_SUMMARY_DIR")

FILE_PATTERN = get_env_variable("FILE_PATTERN")
OUTPUT_DELIMITER = "|"

EXPECTED_FIELDS = [
    "inspection_id",
    "vehicle_id",
    "vehicle_type",
    "brake_condition",
    "tire_condition",
    "vehicle_status",
]

ALLOWED_VEHICLE_TYPES = [
    "Delivery Van",
    "Box Truck",
    "Refrigerated Truck",
    "Tractor Trailer",
    "Service Vehicle",
]

ALLOWED_INSPECTION_CONDITIONS = [
    "Good",
    "Monitor",
    "Critical",
]

ALLOWED_VEHICLE_STATUSES = [
    "Available",
    "In Service",
    "Maintenance Required",
    "Out of Service",
]

VALID_COLUMNS = [
    "inspection_id",
    "vehicle_id",
    "inspection_date",
    "vehicle_type",
    "odometer_km",
    "fuel_litres",
    "fuel_cost_cad",
    "engine_temperature_c",
    "brake_condition",
    "tire_condition",
    "defect_reported",
    "vehicle_status",
    "generated_at",
    "source_file",
]

INVALID_COLUMNS = [
    "inspection_id",
    "vehicle_id",
    "inspection_date",
    "vehicle_type",
    "odometer_km",
    "fuel_litres",
    "fuel_cost_cad",
    "engine_temperature_c",
    "brake_condition",
    "tire_condition",
    "defect_reported",
    "vehicle_status",
    "generated_at",
    "source_file",
    "error_reasons",
]

DUPLICATE_COLUMNS = [
    "inspection_id",
    "vehicle_id",
    "inspection_date",
    "vehicle_type",
    "odometer_km",
    "fuel_litres",
    "fuel_cost_cad",
    "engine_temperature_c",
    "brake_condition",
    "tire_condition",
    "defect_reported",
    "vehicle_status",
    "generated_at",
    "source_file",
    "error_reasons",
]

TRANSFORMED_COLUMNS = [
    "inspection_id",
    "vehicle_id",
    "inspection_date",
    "vehicle_type",
    "odometer_km",
    "fuel_litres",
    "fuel_cost_cad",
    "engine_temperature_c",
    "brake_condition",
    "tire_condition",
    "defect_reported",
    "vehicle_status",
    "fuel_price_per_litre",
    "maintenance_risk",
    "fuel_activity_classification",
    "operational_readiness",
    "depot",
]

DEPOT_SUMMARY_COLUMNS = [
    "depot",
    "vehicle_type",
    "maintenance_risk_level",
    "vehicle_count",
    "total_fuel_litres",
    "total_fuel_cost_cad",
    "average_fuel_price_per_litre",
    "average_engine_temperature_c",
    "defect_count",
    "unavailable_vehicle_count",
]

FILE_METRICS_COLUMN = [
    "file_name",
    "depot",
    "batch_id",
    "processing_status",
    "raw_count",
    "valid_count",
    "invalid_count",
    "duplicate_count",
    "transformed_count",
    "depot_summary_count",
    "error_type",
    "error_message",
]

PIPELINE_METRICS_COLUMN = [
    "total_files",
    "successful_files",
    "failed_files",
    "total_raw_records",
    "total_valid_records",
    "total_invalid_records",
    "total_duplicate_records",
    "total_transformed_records",
    "total_depot_summary_count",
]
