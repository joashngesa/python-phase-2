# transformation rules:
# customs_clearance_days = customs_release_date - arrival_date
# warehouse_delays = actual_warehouse_arrival - warehouse_eta()
# If actual arrival is earlier than ETA, this can be 0
# value_band;
# High Value: declared_value_usd >= 50000
# medium_value_usd >= 15000
# Low Value: below 15000
# weight_band
# Heavy: container_weight_kg >= 20000
# medium: >= 10000
# Light: below 10000
# exception types:
# Customs Hold:
#    inspection_status is "Held" or "Inspection Required"
# Delivery Delay:
#   warehouse_delay_days > 0
# Rejected:
#    inspection_status is "Rejected"
# No Exception:
#    none of the above
# risk_score:
# +40 if inspection_status == "Rejected"
# +25 if inspection_status in ["Held", "Inspection Required"]
# +20 if warehouse_delay_days >= 3
# +10 if warehouse_delay_days in [1, 2]
# +15 if declared_value_usd >= 50000
# +10 if container_weight_kg >= 20000
# risk_level
# High Risk: risk_score >= 60
# Medium Risk: risk_score >= 30
# Low Risk: risk_score > 0
# No Risk: risk_score == 0


def calc_customs_clearance_days(event):

    customs_release_date = event.get("customs_release_date")
    arrival_date = event.get("arrival_date")

    return (customs_release_date - arrival_date).days


def get_warehouse_delays(event):

    actual_warehouse_arrival = event.get("actual_warehouse_arrival")
    warehouse_eta = event.get("warehouse_eta")

    wh_delays = (actual_warehouse_arrival - warehouse_eta).days

    return max(wh_delays, 0)


def get_value_band(event):

    declared_value = event.get("declared_value_usd")

    if declared_value >= 50000:
        return "High_value"

    elif declared_value >= 15000:
        return "Medium_value"

    else:
        return "Low_value"


def get_weight_band(event):

    container_weight = event.get("container_weight_kg")

    if container_weight >= 20000:
        return "Heavy"

    elif container_weight >= 10000:
        return "Medium"

    else:
        return "Light"


def get_exception_types(inspection_status, warehouse_delay_days):

    if inspection_status in {"Held", "Inspection Required"}:
        return "Customs Hold"

    elif inspection_status == "Rejected":
        return "Rejected"

    elif warehouse_delay_days > 0:
        return "Delivery Delay"

    else:
        return "No Exception"


def get_risk_score(
    inspection_status, warehouse_delay_days, declared_value, container_weight
):

    risk_score = 0

    if inspection_status == "Rejected":
        risk_score += 40

    elif inspection_status in {"Held", "Inspection Required"}:
        risk_score += 25

    if warehouse_delay_days >= 3:
        risk_score += 20

    elif warehouse_delay_days in {1, 2}:
        risk_score += 10

    if declared_value >= 50000:
        risk_score += 15

    if container_weight >= 20000:
        risk_score += 10

    return risk_score


def get_risk_level(risk_score):

    if risk_score >= 60:
        return "High Risk"

    elif risk_score >= 30:
        return "Medium Risk"

    elif risk_score > 0:
        return "Low risk"

    else:
        return "No Risk"


def transform_data(valid):

    transformed = []

    for event in valid:

        transfigure = event.copy()

        inspection_status = event["inspection_status"]
        ctms_clearance_days = calc_customs_clearance_days(event)
        wh_delays = get_warehouse_delays(event)
        risk_score = get_risk_score(
            inspection_status=event["inspection_status"],
            warehouse_delay_days=wh_delays,
            declared_value=event["declared_value_usd"],
            container_weight=event["container_weight_kg"],
        )

        transfigure["customs_clearance_days"] = ctms_clearance_days
        transfigure["warehouse_delays_days"] = wh_delays
        transfigure["value_band"] = get_value_band(event)
        transfigure["weight_band"] = get_weight_band(event)
        transfigure["exception_types"] = get_exception_types(
            inspection_status, wh_delays
        )
        transfigure["risk_score"] = risk_score
        transfigure["risk_level"] = get_risk_level(risk_score)

        transformed.append(transfigure)

    return [
        {
            "event_id": event.get("event_id"),
            "container_id": event.get("container_id"),
            "port": event.get("port"),
            "warehouse_id": event.get("warehouse_id"),
            "supplier_name": event.get("supplier_name"),
            "product_category": event.get("product_category"),
            "container_type": event.get("container_type"),
            "arrival_date": event.get("arrival_date"),
            "customs_release_date": event.get("customs_release_date"),
            "warehouse_eta": event.get("warehouse_eta"),
            "actual_warehouse_arrival": event.get("actual_warehouse_arrival"),
            "declared_value_usd": event.get("declared_value_usd"),
            "container_weight_kg": event.get("container_weight_kg"),
            "inspection_status": event.get("inspection_status"),
            "transport_mode": event.get("transport_mode"),
            "customs_clearance_days": event.get("customs_clearance_days"),
            "warehouse_delays_days": event.get("warehouse_delays_days"),
            "value_band": event.get("value_band"),
            "weight_band": event.get("weight_band"),
            "exception_types": event.get("exception_types"),
            "risk_score": event.get("risk_score"),
            "risk_level": event.get("risk_level"),
        }
        for event in transformed
    ]
