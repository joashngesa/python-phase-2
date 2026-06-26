
from datetime import datetime

#Convert:
    #quantity_change -> int
    #unit_cost       -> float
    #adjustment_date -> date object

#Conversion rules:
    #If quantity_change is blank, set to None and record conversion error.
    #If quantity_change is non-numeric, set to None and record conversion error.
    #If unit_cost is blank, set to None and record conversion error.
    #If unit_cost is non-numeric, set to None and record conversion error.
    #If adjustment_date is invalid, set to None and record conversion error.

def add_error(field, message):

    error = field.get("error_reasons","")

    if error:
        field["error_reasons"] = error + ": " + message
    else:
        field["error_reasons"] = message


def parse_dates(column, field_name):

    if column is None:
        return None, f"{field_name} is missing"
    
    column = str(column).strip()

    if column == "":
        return None, f"{field_name} is blank"
    
    try:
        return datetime.strptime (column, "%Y-%m-%d").date(), None
    except:
        return None, f"the {field_name} should be in YYYY-MM--DD format"
    

def convert_data(data):

    converted = []

    for revised in data:

        modified = revised.copy()

        #quantity_change conversion
        qty_change = modified.get("quantity_change")

        if qty_change is None or str(qty_change).strip() == "":
            modified["quantity_change"] = None
            add_error (modified, "quantity_change is missing or blank")
        else:
            try:
                modified["quantity_change"] = int(modified["quantity_change"])
            except:
                modified["quantity_change"] = None
                add_error (modified, "quantity_change must be integer")
        

        #unit_cost conversion
        unit_cost = modified.get("unit_cost")

        if unit_cost is None or str(unit_cost).strip() == "":
            modified["unit_cost"] = None
            add_error (modified, "unit_cost is is missing or blank")
        else:
            try:
                modified["unit_cost"] = float (modified["unit_cost"])
            except:
                modified["unit_cost"]
                add_error (modified,"unit_cost should be in float format")

        #adjustment_date conversion

        parsed_adj_date, adj_date_error = parse_dates (modified.get("adjustment_date"),"adjustment_date")

        modified["adjustment_date"] = parsed_adj_date

        if adj_date_error:
            add_error (modified, "adjustment_date_error")

        converted.append(modified)

    return converted