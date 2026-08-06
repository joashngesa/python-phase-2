"""
1. fuel_price_per_litre = fuel_cost_cad / fuel_litres
    when fuel litres == 0, return none
2. maintenance risk:
    critical:
        brake_condition == "Critical"
        tire_condition == "Critical"
        engine_temperature_c > 110
        vehicle_status == "Out of Service"
    high:
        defect_reported is True
        vehicle_status == "Maintenance Required"
    medium:
        brake_condition == "Monitor"
        tire_condition == "Monitor"
        engine_temperature_c between 100 and 110
    else:
        low
3. fuel activity classification:
    No Fuel Recorded (fl == 0)
    Normal Fuel Activity (fl 1-100)
    High Fuel Purchase (fl > 100)
4. operational readiness
    Ready -->{vs: available}/ {dr: false} / {mr: medium, low}
    Restricted --> {vs:in-service, maintenance_required} / {mr: high}
    Unavailable --> {vs: maint_req, out of serv} /{mr: critical}
    -->Derive this from vehicle status, defect state, and maintenance risk.
"""

import logging

logger = logging.getLogger(__name__)


def get_fuel_price(van):
    """
    ->fuel_price_per_litre = fuel_cost_cad / fuel_litres
    ->when fuel litres == 0, return none
    """
    fuel_cost_cad = van.get("fuel_cost_cad")
    fuel_litres = van.get("fuel_litres")

    if not fuel_litres or fuel_litres == 0:
        return None

    else:
        return round(fuel_cost_cad / fuel_litres, 3)


def get_maintenance_risk(
    engine_temperature_c,
    brake_condition,
    tire_condition,
    defect_reported,
    vehicle_status,
):

    if (
        brake_condition == "Critical"
        or tire_condition == "Critical"
        or engine_temperature_c > 110
        or vehicle_status == "Out of Service"
    ):
        return "Critical"

    elif defect_reported is True or vehicle_status == "Maintenance Required":
        return "High"

    elif (
        brake_condition == "Monitor"
        or tire_condition == "Monitor"
        or 100 <= engine_temperature_c <= 110
    ):
        return "Medium"

    else:
        return "Low"


def get_fuel_activity_classification(fuel_litres):

    if not fuel_litres or fuel_litres == 0:
        return "No fuel recorded"

    elif 0 < fuel_litres <= 100:
        return "Normal fuel activity"

    else:
        return "High fuel purchase"


def get_operational_readiness(vehicle_status, defect_reported, maintenance_risk):

    if (
        vehicle_status == "Available"
        and defect_reported is False
        and maintenance_risk in ("Medium", "Low")
    ):
        return "Ready"

    elif (
        vehicle_status in ("In Service", "Maintenance Required")
        and maintenance_risk == "High"
    ):
        return "Restricted"

    else:
        return "Unavailable"


def transform_data(valid):

    logger.debug("Transformation started | valid_record=%d", len(valid))
    transformed = []

    for van in valid:

        transmute = van.copy()

        fuel_price_per_litre = get_fuel_price(transmute)
        fuel_litres = transmute["fuel_litres"]
        engine_temperature_c = transmute["engine_temperature_c"]
        brake_condition = transmute["brake_condition"]
        tire_condition = transmute["tire_condition"]
        defect_reported = transmute["defect_reported"]
        vehicle_status = transmute["vehicle_status"]
        maintenance_risk = get_maintenance_risk(
            engine_temperature_c,
            brake_condition,
            tire_condition,
            defect_reported,
            vehicle_status,
        )
        fuel_activity_classification = get_fuel_activity_classification(fuel_litres)
        operational_readiness = get_operational_readiness(
            vehicle_status, defect_reported, maintenance_risk
        )

        transmute["fuel_price_per_litre"] = fuel_price_per_litre
        transmute["maintenance_risk"] = maintenance_risk
        transmute["fuel_activity_classification"] = fuel_activity_classification
        transmute["operational_readiness"] = operational_readiness

        transformed.append(transmute)

    transformed_data = [
        {
            "inspection_id": vehicle.get("inspection_id"),
            "vehicle_id": vehicle.get("vehicle_id"),
            "inspection_date": vehicle.get("inspection_date"),
            "vehicle_type": vehicle.get("vehicle_type"),
            "odometer_km": vehicle.get("odometer_km"),
            "fuel_litres": vehicle.get("fuel_litres"),
            "fuel_cost_cad": vehicle.get("fuel_cost_cad"),
            "engine_temperature_c": vehicle.get("engine_temperature_c"),
            "brake_condition": vehicle.get("brake_condition"),
            "tire_condition": vehicle.get("tire_condition"),
            "defect_reported": vehicle.get("defect_reported"),
            "vehicle_status": vehicle.get("vehicle_status"),
            "fuel_price_per_litre": vehicle.get("fuel_price_per_litre"),
            "maintenance_risk": vehicle.get("maintenance_risk"),
            "fuel_activity_classification": vehicle.get("fuel_activity_classification"),
            "operational_readiness": vehicle.get("operational_readiness"),
            "depot": vehicle.get("depot"),
        }
        for vehicle in transformed
    ]

    logger.info(
        "Transformation completed | valid_record=%d | transformed_count=%d",
        len(valid),
        len(transformed_data),
    )

    return transformed_data
