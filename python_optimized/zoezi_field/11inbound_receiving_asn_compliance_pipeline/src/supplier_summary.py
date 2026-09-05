import logging

logger = logging.getLogger(__name__)


def supplier_summary(transformed):

    summary = {}
    logger.info("Supplier summary initiated")

    for procure in transformed:

        supplier_id = procure.get("supplier_id")
        supplier_name = procure.get("supplier_name")
        # use of 0 incase value is none
        ordered_qty = procure.get("ordered_qty") or 0
        received_qty = procure.get("received_qty") or 0
        damaged_qty = procure.get("damaged_qty") or 0
        ordered_value = procure.get("ordered_value") or 0
        received_value = procure.get("received_value") or 0
        delivery_performance = procure.get("delivery_performance")
        compliance_status = procure.get("compliance_status")
        group = (supplier_id, supplier_name)
        if group not in summary:
            summary[group] = {
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "receipt_count": 0,
                "tot_ordered_qty": 0,
                "tot_received_qty": 0,
                "tot_ordered_value": 0,
                "tot_received_value": 0,
                "tot_damaged_qty": 0,
                "average_fill_rate_pct": 0,
                "damage_rate_pct": 0,
                "late_receipt_count": 0,
                "compliant_receipt_count": 0,
            }

        record = summary[group]

        record["receipt_count"] += 1
        record["tot_ordered_qty"] += ordered_qty
        record["tot_received_qty"] += received_qty
        record["tot_ordered_value"] += ordered_value
        record["tot_received_value"] += received_value
        record["tot_damaged_qty"] += damaged_qty

        if delivery_performance == "Late":
            record["late_receipt_count"] += 1

        if compliance_status == "Compliant":
            record["compliant_receipt_count"] += 1

    for buy in summary.values():

        # fill rate %
        if buy["tot_ordered_qty"] > 0:
            buy["average_fill_rate_pct"] = round(
                (buy["tot_received_qty"] / buy["tot_ordered_qty"]) * 100, 2
            )

        else:
            buy["average_fill_rate_pct"] = None

        # damage_rate %
        if buy["tot_received_qty"] > 0:
            buy["damage_rate_pct"] = round(
                (buy["tot_damaged_qty"] / buy["tot_received_qty"]) * 100, 2
            )

        else:
            buy["damage_rate_pct"] = None

    suppliers_tbl = list(summary.values())

    logger.info(
        "Supplier summary completed | supplier_digest_count=%d", len(suppliers_tbl)
    )
    return suppliers_tbl
