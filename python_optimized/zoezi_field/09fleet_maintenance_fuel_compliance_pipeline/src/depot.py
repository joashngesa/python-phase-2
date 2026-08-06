"""
Summarize transformed records by:
    depot
    vehicle_type
    maintenance_risk_level
expected columns:
    depot
    vehicle_type
    maintenance_risk_level
    vehicle_count
    total_fuel_litres
    total_fuel_cost_cad
    average_fuel_price_per_litre
    average_engine_temperature_c
    defect_count
    unavailable_vehicle_count
"""

import logging

logger = logging.getLogger(__name__)


def get_depot_summary(transformed):

    logger.debug("Depot generation started | transformed_count=%d", len(transformed))
    summary = {}

    for van in transformed:

        motor = van.copy()

        depot = motor.get("depot")
        vehicle_type = motor.get("vehicle_type")
        maintenance_risk_level = motor.get("maintenance_risk")
        fuel_litres = motor.get("fuel_litres")
        fuel_cost_cad = motor.get("fuel_cost_cad")
        engine_temperature_c = motor.get("engine_temperature_c")
        defect_reported = motor.get("defect_reported")
        operational_readiness = motor.get("operational_readiness")

        group = (vehicle_type, maintenance_risk_level)
        if group not in summary:
            summary[group] = {
                "depot": depot,
                "vehicle_type": vehicle_type,
                "maintenance_risk_level": maintenance_risk_level,
                "vehicle_count": 0,
                "total_fuel_litres": 0,
                "total_fuel_cost_cad": 0,
                "average_fuel_price_per_litre": 0,
                "total_engine_temperature_c": 0,
                "average_engine_temperature_c": 0,
                "defect_count": 0,
                "unavailable_vehicle_count": 0,
            }

        data = summary[group]

        data["vehicle_count"] += 1
        data["total_fuel_litres"] += fuel_litres
        data["total_fuel_cost_cad"] += fuel_cost_cad
        data["total_engine_temperature_c"] += engine_temperature_c

        if defect_reported is True:
            data["defect_count"] += 1

        if operational_readiness == "Unavailable":
            data["unavailable_vehicle_count"] += 1

    for value in summary.values():

        if value["total_fuel_litres"] > 0:
            value["average_fuel_price_per_litre"] = round(
                value["total_fuel_cost_cad"] / value["total_fuel_litres"], 2
            )

        else:
            value["average_fuel_price_per_litre"] = 0.0

        if value["vehicle_count"] > 0:
            value["average_engine_temperature_c"] = round(
                value["total_engine_temperature_c"] / value["vehicle_count"], 2
            )

        else:
            value["average_engine_temperature_c"] = 0.0

        del value["total_engine_temperature_c"]

    depot_sum = list(summary.values())
    logger.info(
        "Depot generation completed | transformed_count=%d | depot_summary=%d",
        len(transformed),
        len(depot_sum),
    )

    return depot_sum
