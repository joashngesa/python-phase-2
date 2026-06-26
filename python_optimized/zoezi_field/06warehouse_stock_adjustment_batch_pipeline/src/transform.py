
#Transformation
    #inventory_value_impact = quantity_change * unit_cost
    #impact_direction:
        #inventory_value_impact > 0   -> Increase
        #inventory_value_impact < 0   -> Decrease
    #impact band
        #abs(impact) >= 500  -> High
        #abs(impact) >= 100  -> Medium
        #else                -> Low

def impact_direction (inventory_value_impact):

    if inventory_value_impact > 0:
        return "Increase"
    if inventory_value_impact < 0:
        return "Deacrease"


def impact_band(inventory_value_impact):

    if abs(inventory_value_impact) >= 500:
        return "High"
    if abs(inventory_value_impact) >= 100:
        return "Medium"
    else:
        return "Low"


def transform_data (valids):

    return [
        {
    "adjustment_id": stock.get("adjustment_id"),
    "warehouse_id": stock.get("warehouse_id"),
    "warehouse_name": stock.get("warehouse_name"),
    "sku": stock.get("sku"),
    "product_name": stock.get("product_name"),
    "adjustment_date": stock.get("adjustment_date"),
    "adjustment_type": stock.get("adjustment_type"),
    "quantity_change": stock.get("quantity_change"),
    "unit_cost": stock.get("unit_cost"),
    "approved_by": stock.get("approved_by"),
    "status": stock.get("status"),
    "inventory_value_impact": (ivi := (stock.get("quantity_change") * stock.get("unit_cost"))),
    "impact_direction": impact_direction(ivi),
    "impact_band": impact_band(ivi),
    "source_file": stock.get("source_file"),
    "processed_at": stock.get("processed_at")
        }
        for stock in valids
    ]