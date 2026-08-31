def calc_ordered_value(procure):

    ordered_qty = procure.get("ordered_qty")
    unit_cost = procure.get("unit_cost")

    return ordered_qty * unit_cost


def calc_received_value(procure):

    received_qty = procure.get("received_qty")
    unit_cost = procure.get("unit_cost")

    return received_qty * unit_cost


def calc_quantity_variance(procure):

    received_qty = procure.get("received_qty")
    ordered_qty = procure.get("ordered_qty")

    return received_qty - ordered_qty


def calc_fill_rate_pct(procure):

    received_qty = procure.get("received_qty")
    ordered_qty = procure.get("ordered_qty")

    if ordered_qty == 0:
        return None

    else:
        return round((received_qty / ordered_qty) * 100, 2)


def calc_damage_rate_pct(procure):

    damaged_qty = procure.get("damaged_qty")
    received_qty = procure.get("received_qty")

    if received_qty == 0:
        return None

    else:
        return round((damaged_qty / received_qty) * 100, 2)


def calc_delivery_variance(procure):

    receipt_date = procure.get("receipt_date")
    promised_delivery_date = procure.get("promised_delivery_date")

    if receipt_date is None:
        return None

    else:
        return (receipt_date - promised_delivery_date).days


def calc_delivery_performance(delivery_variance):

    if delivery_variance is None:
        return "Not received"

    if delivery_variance > 0:
        return "Late"

    elif delivery_variance == 0:
        return "On time"

    elif delivery_variance < 0:
        return "Early"


def calc_received_performance(quantity_variance, damaged_qty):

    if quantity_variance < 0 and damaged_qty > 0:
        return "Short & damaged"

    elif damaged_qty > 0:
        return "Damaged"

    elif quantity_variance > 0:
        return "Over"

    elif quantity_variance == 0:
        return "Exact"

    elif quantity_variance < 0:
        return "Short"


def calc_compliance_status(delivery_performance, received_performance):

    if (
        delivery_performance in ("Early", "Late")
        and received_performance
        in (
            "Short",
            "Over",
            "Damaged",
            "Short & damaged",
        )
    ) or received_performance == "Short & damaged":
        return "Multiple issues"

    elif received_performance == "Damaged":
        return "Damaged_issue"

    elif received_performance in ("Short", "Over"):
        return "Quantity_issue"

    elif delivery_performance in ("Late", "Early"):
        return "Delivery_issue"

    elif delivery_performance == "On time" and received_performance == "Exact":
        return "Compliant"


def transform_data(valid):

    transformed = []

    for procure in valid:

        buy = procure.copy()

        damaged_qty = buy.get("damaged_qty")
        ordered_value = calc_ordered_value(buy)
        received_value = calc_received_value(buy)
        quantity_variance = calc_quantity_variance(buy)
        fill_rate_pct = calc_fill_rate_pct(buy)
        damaged_rate_pct = calc_damage_rate_pct(buy)
        delivery_variance = calc_delivery_variance(buy)
        delivery_performance = calc_delivery_performance(delivery_variance)
        received_performance = calc_received_performance(quantity_variance, damaged_qty)
        compliance_status = calc_compliance_status(
            delivery_performance, received_performance
        )

        buy["ordered_value"] = ordered_value
        buy["received_value"] = received_value
        buy["quantity_variance"] = quantity_variance
        buy["fill_rate_pct"] = fill_rate_pct
        buy["damaged_rate_pct"] = damaged_rate_pct
        buy["delivery_variance"] = delivery_variance
        buy["delivery_performance"] = delivery_performance
        buy["received_performance"] = received_performance
        buy["compliance_status"] = compliance_status

        transformed.append(buy)

    return transformed
