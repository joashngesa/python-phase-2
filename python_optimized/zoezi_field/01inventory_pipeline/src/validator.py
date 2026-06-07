
raw_columns = ["sku","product","warehouse","quantity","unit_cost"]

def validator(stock):

    error_reason = stock.get("error_reason")
    if error_reason:
        return False, "parse error: rows do not have exactly 5 fields"

    for column in raw_columns:
        if column not in stock:
            return False, f"the column{column} is missing"
        
    sku = stock.get("sku")
    product = stock.get("product")
    warehouse = stock.get("warehouse")
    quantity = stock.get("quantity")
    unit_cost = stock.get("unit_cost")

    if sku is None:
        return False, "sku is missing"
    if not sku.strip():
        return False, "sku ia blank"
    if not isinstance (sku, str):
        return False, "sku needs to needs to be a string"
    if product is None:
        return False, "product is missing"
    if not product.strip():
        return False, "product is blank"
    if not isinstance (product, str):
        return False, "product needs to be a string"
    if warehouse is None:
        return False, "warehouse is missing"
    if not warehouse.strip():
        return False, "warehouse is blank"
    if not isinstance (warehouse, str):
        return False, "warehouse needs to be a string"
    if  quantity is None:
        return False, "quantity  is missing"
    if quantity < 0:
        return False, "quantity needs to be >= 0"
    if unit_cost is None:
        return False, "unit_cost is missing"
    if unit_cost <= 0:
        return False, "unit_cost should be greater than 0"
    
    return True, None