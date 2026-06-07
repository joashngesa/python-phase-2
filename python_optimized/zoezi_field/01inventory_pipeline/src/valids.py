
def get_valids(valids_raw):
    return [
        {
            "sku": stock.get("sku"),
            "product": stock.get("product"),
            "warehouse": stock.get("warehouse"),
            "quantity": stock.get("quantity"),
            "unit_cost": stock.get("unit_cost")
        }
        for stock in valids_raw
    ]