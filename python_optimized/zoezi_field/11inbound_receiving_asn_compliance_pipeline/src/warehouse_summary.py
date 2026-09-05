import logging

logger = logging.getLogger(__name__)


def warehouse_synopsis(transformed):

    whse_summary = {}
    logger.info("Warehouse summary initiated")

    for procure in transformed:

        warehouse = procure.get("warehouse")
        ordered_qty = procure.get("ordered_qty")
        received_qty = procure.get("received_qty")
        damaged_qty = procure.get("damaged_qty")
        delivery_performance = procure.get("delivery_performance")

        if warehouse not in whse_summary:
            whse_summary[warehouse] = {
                "warehouse": warehouse,
                "receipts_count": 0,
                "tot_ordered_qty": 0,
                "tot_received_qty": 0,
                "tot_damaged_qty": 0,
                "fill_rate_pct": 0,
                "damage_rate_pct": 0,
                "late_receipts": 0,
            }

        record = whse_summary[warehouse]

        record["receipts_count"] += 1
        record["tot_ordered_qty"] += ordered_qty
        record["tot_received_qty"] += received_qty
        record["tot_damaged_qty"] += damaged_qty

        if delivery_performance == "Late":
            record["late_receipts"] += 1

    for buy in whse_summary.values():

        if buy["tot_ordered_qty"] > 0:
            buy["fill_rate_pct"] = round(
                (buy["tot_received_qty"] / buy["tot_ordered_qty"]) * 100, 2
            )

        else:
            buy["fill_rate_pct"] = None

        if buy["tot_received_qty"] > 0:
            buy["damage_rate_pct"] = round(
                (buy["tot_damaged_qty"] / buy["tot_received_qty"]) * 100, 2
            )

        else:
            buy["damage_rate_pct"] = None

    summary = list(whse_summary.values())

    logger.info("Warehouse summary completed | warehouse_digest_count=%d", len(summary))

    return summary
