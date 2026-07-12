from src.config import LOSS_MULTIPLIERS

# Temp_breach_type
# "Below Range" if actual_temp_c < required_temp_min_c
# "Above Range" if actual_temp_c > required_temp_max_c
# "No Breach"   if actual_temp_c is within range
# temp_deviation_c -
# Calculate how far outside the allowed range the temperature was
# High Risk:
# temp_deviation_c > 3 OR exposure_minutes >= 120
# Medium Risk:
# temp_deviation_c > 1 OR exposure_minutes >= 60
# Low Risk:
# temp_deviation_c > 0 OR exposure_minutes > 0
# No Breach:
# temp_deviation_c == 0
# estimated_loss_value = temp_deviation_c * exposure_minutes * category_multiplier


def temp_breach_type(actual_temp, required_temp_min, required_temp_max):
    """
    Temp_breach_type calculation criteria:
    "Below Range" if actual_temp_c < required_temp_min_c
    "Above Range" if actual_temp_c > required_temp_max_c
    "No Breach"   if actual_temp_c is within range
    """

    if actual_temp < required_temp_min:
        return "below range"
    elif actual_temp > required_temp_max:
        return "above range"
    else:
        return "no breach"


def temp_deviation(actual_temp, required_temp_min, required_temp_max):
    """
    Calculate how far outside the allowed range the temperature was
    """

    if actual_temp < required_temp_min:
        return required_temp_min - actual_temp

    elif actual_temp > required_temp_max:
        return actual_temp - required_temp_max

    else:
        return 0.0


def risk_level(temp_dev, exposure_minutes):

    if temp_dev > 3 or exposure_minutes >= 120:
        return "high_risk"

    elif temp_dev > 1 or exposure_minutes >= 60:
        return "medium_risk"

    elif temp_dev > 0 or exposure_minutes > 0:
        return "low risk"
    elif temp_dev == 0:
        return "no_breach"


# estimated_loss_value = temp_deviation_c * exposure_minutes * category_multiplier
# return (temp_dev * exposure_minutes * category_multiplier)


def transform_data(valids):

    transformed_tbl = []

    for event in valids:

        actual_temp = event.get("actual_temp_c")
        required_temp_min = event.get("required_temp_min_c")
        required_temp_max = event.get("required_temp_max_c")
        category = event.get("product_category")
        exposure_minutes = event.get("exposure_minutes")
        temp_dev = temp_deviation(actual_temp, required_temp_min, required_temp_max)

        breach_type = temp_breach_type(
            actual_temp, required_temp_min, required_temp_max
        )
        t_dev = temp_deviation(actual_temp, required_temp_min, required_temp_max)
        risk = risk_level(temp_dev, exposure_minutes)

        category_multiplier = LOSS_MULTIPLIERS.get(category, 0)
        loss_value = round(temp_dev * exposure_minutes * category_multiplier, 2)

        transformed = {
            "incident_id": event.get("incident_id"),
            "shipment_id": event.get("shipment_id"),
            "warehouse_id": event.get("warehouse_id"),
            "product_category": category,
            "product_name": event.get("product_name"),
            "required_temp_min_c": required_temp_min,
            "required_temp_max_c": required_temp_max,
            "actual_temp": actual_temp,
            "exposure_minutes": exposure_minutes,
            "incident_date": event.get("incident_date"),
            "delivery_status": event.get("delivery_status"),
            "carrier": event.get("carrier"),
            "temp_breach_type": breach_type,
            "temperature_deviation_c": t_dev,
            "risk_level": risk,
            "estimated_loss_value": loss_value,
        }

        transformed_tbl.append(transformed)

    return transformed_tbl
