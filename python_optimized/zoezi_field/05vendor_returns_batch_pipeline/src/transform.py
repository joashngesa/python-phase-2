#get return value
#return band:
    #return_value >= 500  -> High
    #return_value >= 100  -> Medium
    #else                 -> Low

def calc_return_band(return_value):

    if return_value >= 500:
        return "High"
    if return_value >= 100:
        return "Medium"
    else:
        return "low"
    
def transform_data(valids):

    return [
        {
    "return_id": item.get("return_id"),
    "vendor_id": item.get("vendor_id"),
    "vendor_name": item.get("vendor_name"),
    "warehouse": item.get("warehouse"),
    "product_sku": item.get("product_sku"),
    "product_name": item.get("product_name"),
    "return_date":item.get("return_date"),
    "reason": item.get("reason"),
    "quantity": item.get("quantity"),
    "unit_cost": item.get("unit_cost"),
    #used walrus operator to calculate the column simultaneously
    "return_value": (rv := (item.get("quantity") * item.get("unit_cost"))),
    "return_band": calc_return_band(rv),
    "status": item.get("status")
        }
        for item in valids
    ]
