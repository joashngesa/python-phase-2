"""
Transformed created values
    -> ordered_value = quantity_ordered × unit_cost
    -> received_value = quantity_received × unit_cost
    -> budget_variance = planned_cost - actual_cost->>ordered_value - received_value
    -> delivery_delay = actual_delivery_date - expected_delivery_date
    -> fulfillment_rate % = (received_qty / ordered_qty) * 100
    -> supplier risk score:
        delivery_risk:
        delivery_delay_days >= 7        +30
        delivery_delay_days between 3–6 +20
        delivery_delay_days between 1–2 +10
        fulfillment_risk:
        fulfilment_rate < 80%           +30
        fulfilment_rate between 95%-100%      0
        fulfillment_rate 81% - 94%      +15
        fulfillment_rate > 100          +20
"""


def calc_ordered_value(procure):

    quantity_ordered = procure.get("quantity_ordered")
    unit_cost = procure.get("unit_cost")

    return quantity_ordered * unit_cost


def calc_received_value(procure):

    quantity_received = procure.get("quantity_received")
    unit_cost = procure.get("unit_cost")

    return quantity_received * unit_cost


def calc_budget_variance(ordered_value, received_value):

    return ordered_value - received_value


def calc_delivery_delay(procure):

    actual_delivery_date = procure.get("actual_delivery_date")
    expected_delivery_date = procure.get("expected_delivery_date")

    if not actual_delivery_date or not expected_delivery_date:
        return 0

    delivery_delay = (actual_delivery_date - expected_delivery_date).days

    return max(delivery_delay, 0)


def calc_fulfillment_rate(procure):

    quantity_received = procure.get("quantity_received")
    quantity_ordered = procure.get("quantity_ordered")

    if not quantity_ordered:
        return 0.0

    return round((quantity_received / quantity_ordered) * 100, 2)


def calc_supplier_risk_score(delivery_delay, fulfillment_rate):

    risk_score = 0

    if delivery_delay >= 7:
        risk_score += 30

    elif delivery_delay >= 3:
        risk_score += 20

    elif delivery_delay >= 1:
        risk_score += 10

    if fulfillment_rate > 100:
        risk_score += 20

    elif fulfillment_rate >= 95:
        risk_score += 0

    elif fulfillment_rate >= 80:
        risk_score += 15

    else:
        risk_score += 30

    return risk_score


def calc_risk_classification(supplier_risk_score):

    if supplier_risk_score >= 60:
        return "High"

    elif supplier_risk_score >= 30:
        return "Medium"

    elif supplier_risk_score > 0:
        return "Low"

    else:
        return "None"


def transform_data(valid):

    transformed = []

    for procure in valid:

        mutated = procure.copy()

        ordered_value = calc_ordered_value(procure)
        received_value = calc_received_value(procure)
        budget_variance = calc_budget_variance(ordered_value, received_value)
        delivery_delay = calc_delivery_delay(procure)
        fulfillment_rate = calc_fulfillment_rate(procure)
        supplier_risk_score = calc_supplier_risk_score(delivery_delay, fulfillment_rate)
        risk_classification = calc_risk_classification(supplier_risk_score)

        mutated["ordered_value"] = ordered_value
        mutated["received_value"] = received_value
        mutated["budget_variance"] = budget_variance
        mutated["delivery_delay"] = delivery_delay
        mutated["fulfillment_rate"] = fulfillment_rate
        mutated["supplier_risk_score"] = supplier_risk_score
        mutated["risk_classification"] = risk_classification

        transformed.append(mutated)

    return [
        {
            "purchase_order_id": buy.get("purchase_order_id"),
            "supplier_id": buy.get("supplier_id"),
            "supplier_name": buy.get("supplier_name"),
            "product_category": buy.get("product_category"),
            "quantity_ordered": buy.get("quantity_ordered"),
            "quantity_received": buy.get("quantity_received"),
            "unit_cost": buy.get("unit_cost"),
            "approved_budget": buy.get("approved_budget"),
            "order_date": buy.get("order_date"),
            "expected_delivery_date": buy.get("expected_delivery_date"),
            "actual_delivery_date": buy.get("actual_delivery_date"),
            "delivery_status": buy.get("delivery_status"),
            "priority": buy.get("priority"),
            "ordered_value": buy.get("ordered_value"),
            "received_value": buy.get("received_value"),
            "budget_variance": buy.get("budget_variance"),
            "delivery_delay": buy.get("delivery_delay"),
            "fulfillment_rate": buy.get("fulfillment_rate"),
            "supplier_risk_score": buy.get("supplier_risk_score"),
            "risk_classification": buy.get("risk_classification"),
        }
        for buy in transformed
    ]
