from datetime import datetime, date
from src.config import EXPECTED_FIELDS
from src.config import ALLOWED_INSPECTION_CONDITIONS
from src.config import ALLOWED_VEHICLE_TYPES
from src.config import ALLOWED_VEHICLE_STATUSES

"""
validation rules:
    odometer_km >= 0
    fuel_litres >= 0
    fuel_cost_cad >= 0
    engine_temperature_c must be between -40 and 150
Buisness validation rules
    when fuel_litres == 0 then fuel_cost_cad must also equal 0
    when defect_reported is True then status can not be "available"
    when brake_condition == "Critical" then vehicle status must be "Maintenance Required"/ "Out of Service"
    when tire_condition == "Critical" then vehicle status must be "Maintenance Required"/ "Out of Service"
    when engine_temperature_c > 110 then vehicle status can not remain available
"""


def validate_data(van):
    """
    this is a helper function that validates schema_structure, data types and business logic of the data.
    """
    peculiar = []

    for field in EXPECTED_FIELDS:
        if field not in van:
            peculiar.append(f"{field} is missing")

    # validate inspection_id
    inspection_id = van.get("inspection_id")
    if inspection_id is None:
        peculiar.append("inspection_id is missing")

    elif not isinstance(inspection_id, str):
        peculiar.append("inspection_id should be string")

    elif inspection_id.strip() == "":
        peculiar.append("inspection_id is blank")

    # validate vehicle_id
    vehicle_id = van.get("vehicle_id")
    if vehicle_id is None:
        peculiar.append("vehicle_id is missing")

    elif not isinstance(vehicle_id, str):
        peculiar.append("vehicle_id should be string")

    elif vehicle_id.strip() == "":
        peculiar.append("vehicle_id is blank")

    # validate inspection_date
    inspection_date = van.get("inspection_date")
    if inspection_date is None:
        peculiar.append("inspection_date is missing or blank")

    elif not isinstance(inspection_date, date):
        peculiar.append("inspection_date should be YYYY-MM-DD format")

    # validate vehicle_type
    vehicle_type = van.get("vehicle_type")
    if vehicle_type is None:
        peculiar.append("vehicle_type is missing")

    elif not isinstance(vehicle_type, str):
        peculiar.append("vehicle_type should be string")

    elif vehicle_type.strip() == "":
        peculiar.append("vehicle_type is blank")

    elif vehicle_type not in ALLOWED_VEHICLE_TYPES:
        peculiar.append("vehicle_type should be in the vehicle_type list")

    # validate odometer_km
    odometer_km = van.get("odometer_km")
    if odometer_km is None:
        peculiar.append("odometer_km is missing")

    elif not isinstance(odometer_km, int):
        peculiar.append("odometer_km should be integer")

    elif odometer_km < 0:
        peculiar.append("odometer_km should be >= 0")

    # validate fuel_cost_cad
    fuel_cost_cad = van.get("fuel_cost_cad")
    fuel_cost_check = False
    if fuel_cost_cad is None:
        peculiar.append("fuel_cost_cad is missing")

    elif not isinstance(fuel_cost_cad, float):
        peculiar.append("fuel_cost_cad should be float")

    elif fuel_cost_cad < 0:
        peculiar.append("fuel_cost_cad should be >= 0")

    else:
        fuel_cost_check = True

    # validate fuel_litres
    fuel_litres = van.get("fuel_litres")
    fuel_lt_check = False
    if fuel_litres is None:
        peculiar.append("fuel_litres is missing")

    elif not isinstance(fuel_litres, float):
        peculiar.append("fuel_litres should be float")

    elif fuel_litres < 0:
        peculiar.append("fuel_litres should be >= 0")

    elif fuel_cost_check and fuel_litres == 0 and fuel_cost_cad != 0:
        peculiar.append("when fuel_litres is 0, fuel_cost must be 0 ")

    else:
        fuel_lt_check = True

    # validate vehicle_status
    vehicle_status = van.get("vehicle_status")
    status_check = False
    if vehicle_status is None:
        peculiar.append("vehicle_status is missing")

    elif not isinstance(vehicle_status, str):
        peculiar.append("vehicle_status should be a string")

    elif vehicle_status.strip() == "":
        peculiar.append("vehicle_status is blank")

    elif vehicle_status not in ALLOWED_VEHICLE_STATUSES:
        peculiar.append("vehicle_status should be in the statuses list")

    else:
        status_check = True

    # validate engine_temperature_c
    eng_temperature = van.get("engine_temperature_c")
    if eng_temperature is None:
        peculiar.append("engine_temperature_c is missing")

    elif not isinstance(eng_temperature, float):
        peculiar.append("engine_temperature_c should be string ")

    elif not -40 <= eng_temperature <= 150:
        peculiar.append("engine_temperature_c must be between -40 & 150")

    elif eng_temperature > 110 and vehicle_status == "Available":
        peculiar.append(
            "when engine_temperature_c > 110, vehicle_status must not be available"
        )

    # validate brake_condition
    brake_condition = van.get("brake_condition")
    if brake_condition is None:
        peculiar.append("brake_condition is missing")

    elif not isinstance(brake_condition, str):
        peculiar.append("brake_condition should be string")

    elif brake_condition.strip() == "":
        peculiar.append("brake_condition is blank")

    elif brake_condition not in ALLOWED_INSPECTION_CONDITIONS:
        peculiar.append(
            f"brake_condition must be one of {' '.join(ALLOWED_INSPECTION_CONDITIONS)}"
        )

    elif (
        status_check
        and brake_condition == "Critical"
        and vehicle_status not in ("Maintenance Required", "Out of Service")
    ):
        peculiar.append(
            "when brakes is critical, status must be maintenance / out of service"
        )

    # validate tire_condition
    tire_condition = van.get("tire_condition")
    if tire_condition is None:
        peculiar.append("tire_condition is missing")

    elif not isinstance(tire_condition, str):
        peculiar.append("tire_condition should be a string")

    elif tire_condition.strip() == "":
        peculiar.append("tire_condition is blank")

    elif tire_condition not in ALLOWED_INSPECTION_CONDITIONS:
        peculiar.append(
            f"tire condition must be one of {' '.join(ALLOWED_INSPECTION_CONDITIONS)}"
        )

    elif (
        status_check
        and tire_condition == "Critical"
        and vehicle_status not in ("Maintenance Required", "Out of Service")
    ):
        peculiar.append(
            "when tire is critical, status must be maintenance / out of service"
        )

    # validate defect_reported
    defect_reported = van.get("defect_reported")
    if defect_reported is None:
        peculiar.append("defect_reported is missing")

    elif not isinstance(defect_reported, bool):
        peculiar.append("defect_reported should be a boolean value")

    elif status_check and defect_reported is True and vehicle_status == "Available":
        peculiar.append("if defect is reported, status can not be available")

    # return summary
    if peculiar:
        return False, peculiar
    else:
        return True, []
