# from transformed files,summarize by:
# port
# product_category
# exception_type
# risk_level

# columns:
# port
# product_category
# exception_type
# risk_level
# container_count
# total_declared_value_usd
# total_container_weight_kg
# avg_customs_clearance_days
# avg_warehouse_delay_days


def summarize_table(transformed):

    summary = {}

    for event in transformed:

        port = event.get("port")
        product_category = event.get("product_category")
        exception_type = event.get("exception_type")
        risk_level = event.get("risk_level")
        container_id = event.get("container_id")
        declared_value = event.get("declared_value_usd")
        container_weight = event.get("container_weight_kg")
        customs_clearance_days = event.get("customs_clearance_days")
        wh_delays_days = event.get("warehouse_delays_days")

        sum_keys = (port, product_category, exception_type, risk_level)

        if sum_keys not in summary:
            summary[sum_keys] = {
                "port": port,
                "product_category": product_category,
                "exception_type": exception_type,
                "risk_level": risk_level,
                "container_count": 0,
                "total_declared_value_usd": 0,
                "total_container_weight_kg": 0,
                "tot_c_clearance_days": 0,
                "tot_wh_delays_days": 0,
                "avg_customs_clearance_days": 0,
                "avg_warehouse_delay_days": 0,
            }

        summary[sum_keys]["container_count"] += 1
        summary[sum_keys]["total_declared_value_usd"] += declared_value
        summary[sum_keys]["total_container_weight_kg"] += container_weight
        summary[sum_keys]["tot_c_clearance_days"] += customs_clearance_days
        summary[sum_keys]["tot_wh_delays_days"] += wh_delays_days

    group_summary = []

    for content in summary.values():

        count = content["container_count"]

        group_summary.append(
            {
                "port": content["port"],
                "product_category": content["product_category"],
                "exception_type": content["exception_type"],
                "risk_level": content["risk_level"],
                "container_count": content["container_count"],
                "total_declared_value_usd": content["total_declared_value_usd"],
                "total_container_weight_kg": content["total_container_weight_kg"],
                "avg_customs_clearance_days": round(
                    content["tot_c_clearance_days"] / count, 2
                ),
                "avg_warehouse_delay_days": round(
                    content["tot_wh_delays_days"] / count, 2
                ),
            }
        )

    return group_summary
