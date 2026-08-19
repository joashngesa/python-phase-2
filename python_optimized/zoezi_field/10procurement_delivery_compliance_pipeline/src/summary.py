"""
Summarize by:
    depot
    supplier_id
    supplier_name
    product_category
Columns expected:
    purchase_order_count
    total_quantity_ordered
    total_quantity_received
    total_ordered_value
    total_received_value
    average_delivery_delay_days
    average_fulfilment_rate
    over_budget_order_count
    high_risk_order_count
"""

import logging

logger = logging.getLogger(__name__)


def summarize_table(transformed):

    logger.info("Table summary initiated")
    summary = {}

    for procure in transformed:

        supplier_id = procure.get("supplier_id")
        supplier_name = procure.get("supplier_name")
        product_category = procure.get("product_category")
        purchase_order_id = procure.get("purchase_order_id")
        quantity_ordered = procure.get("quantity_ordered")
        quantity_received = procure.get("quantity_received")
        ordered_value = procure.get("ordered_value")
        received_value = procure.get("received_value")
        delivery_delay = procure.get("delivery_delay")
        budget_variance = procure.get("budget_variance")
        risk_classification = procure.get("risk_classification")

        group = (supplier_id, supplier_name, product_category)

        if group not in summary:
            summary[group] = {
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "product_category": product_category,
                "purchase_order_count": 0,
                "total_quantity_ordered": 0,
                "total_quantity_received": 0,
                "total_ordered_value": 0,
                "total_received_value": 0,
                "total_delivery_days": 0,
                "delivery_delay_count": 0,
                "average_delivery_delay_days": 0,
                "unfulfilled_order_count": 0,
                "high_risk_order_count": 0,
            }

        data = summary[group]

        data["purchase_order_count"] += 1
        data["total_quantity_ordered"] += quantity_ordered
        data["total_quantity_received"] += quantity_received
        data["total_ordered_value"] += ordered_value
        data["total_received_value"] += received_value
        data["total_delivery_days"] += delivery_delay

        if delivery_delay > 0:
            data["delivery_delay_count"] += 1

        if budget_variance > 0:
            data["unfulfilled_order_count"] += 1

        if risk_classification == "High":
            data["high_risk_order_count"] += 1

    for buy in summary.values():

        if buy["delivery_delay_count"] > 0:
            buy["average_delivery_delay_days"] = round(
                buy["total_delivery_days"] / buy["delivery_delay_count"], 2
            )

        else:
            buy["average_delivery_delay_days"] = 0

        del buy["total_delivery_days"]
        del buy["delivery_delay_count"]

    table_summary = list(summary.values())
    logger.info("Table summary completed | summary_count=%d", len(table_summary))

    return table_summary
