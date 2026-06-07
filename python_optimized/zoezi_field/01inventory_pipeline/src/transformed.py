
def get_inventory_value(stock):

    return stock.get("quantity") * stock.get("unit_cost")



def transform_data(valids):
    return [
        {
            "sku": stock.get("sku"),
            "product": stock.get("product"),
            "warehouse": stock.get("warehouse"),
            "quantity": stock.get("quantity"),
            "unit_cost": stock.get("unit_cost"),
            "inventory_value": get_inventory_value(stock)
        }
        for stock in valids
    ]