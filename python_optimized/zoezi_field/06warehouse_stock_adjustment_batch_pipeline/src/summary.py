
#Expected output:
    #"warehouse_id",
    #"warehouse_name",
    #"record_count",
    #"total_positive_impact",
    #"total_negative_impact",
    #"net_inventory_value_impact",
    #"increase_count",
    #"decrease_count",
    #"high_impact_count",
    #"medium_impact_count",
    #"low_impact_count"

#Business logic    
    #total_positive_impact = sum of impacts greater than 0
    #total_negative_impact = sum of impacts less than 0
    #net_inventory_value_impact = total positive + total negative
    #increase_count = count where direction is Increase
    #decrease_count = count where direction is Decrease
    #impact band counts by High/Medium/Low

def warehouse_summary (transformed):

    summary = {}

    for stock in transformed:

        warehouse_id = stock.get("warehouse_id")
        warehouse_name = stock.get("warehouse_name")
        qty_change = stock.get("quantity_change")
        impact_direction = stock.get("impact_direction")
        inventory_value_impact =stock.get("inventory_value_impact")
        impact_band = stock.get("impact_band")
        source_file = stock.get("source_file")
        processed_at = stock.get("processed_at")

        if warehouse_id not in summary:
            summary[warehouse_id] = {
                "warehouse_id": warehouse_id,
                "warehouse_name": warehouse_name,
                "record_count": 0,
                "total_positive_impact": 0,
                "total_negative_impact": 0,
                "net_inventory_value_impact": 0,
                "increase_count": 0,
                "decrease_count": 0,
                "high_impact_count": 0,
                "medium_impact_count": 0,
                "low_impact_count": 0,
                "source_file": source_file,
                "processed_at": processed_at
            }

        summary[warehouse_id]["record_count"] += 1
        if qty_change > 0:
            summary[warehouse_id]["total_positive_impact"] += qty_change
        if qty_change < 0:
            summary[warehouse_id]["total_negative_impact"] += qty_change
        
        summary[warehouse_id]["net_inventory_value_impact"] += inventory_value_impact
        if impact_direction.lower() == "increase":
            summary[warehouse_id]["increase_count"] += 1
        if impact_direction.lower() == "deacrease":
            summary[warehouse_id]["decrease_count"] += 1

        if impact_band.lower() == "high":
            summary[warehouse_id]["high_impact_count"] += 1

        if impact_band.lower() == "medium":
            summary[warehouse_id]["medium_impact_count"] += 1

        if impact_band.lower() == "low":
            summary[warehouse_id]["low_impact_count"]

        
    return list (summary.values())