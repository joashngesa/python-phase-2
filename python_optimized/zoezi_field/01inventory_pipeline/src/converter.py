
def convert_data(raw):
    
    converted = []

    for stock in raw:
        adjusted = stock.copy()
        conversion_errors = {}

        quantity = adjusted["quantity"]

        if quantity == "":
            adjusted["quantity"] = None

        else:
            try:
                adjusted["quantity"] = int(quantity)

            except ValueError:
                adjusted["quantity"] = None
                conversion_errors["quantity"] = "quantity must be integer"

        unit_cost = adjusted["unit_cost"]

        if unit_cost == "":
            adjusted["unit_cost"] = None

        else:
            try:
                adjusted["unit_cost"] = int (unit_cost)

            except ValueError:
                adjusted["unit_cost"] = None
                conversion_errors["unit_cost"] = "unit_cost must be number"
            
        
        adjusted["_conversion_errors"] = conversion_errors
        converted.append(adjusted)

    return converted 


