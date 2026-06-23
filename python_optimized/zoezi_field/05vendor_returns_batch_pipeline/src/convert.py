
from datetime import datetime, date

#Output
    #quantity  -> int
    #unit_cost -> float
    #return_date

def parse_data(field,field_name):

    if field is None:
        return None, f"{field_name} is missing"
    
    field = str(field).strip()

    if field == "":
        return None, f"{field_name} is blank"
    
    try:
        return datetime.strptime(field, "%Y-%m-%d").date(), None
    except:
        return None, f"the {field_name} should be in the YYYY-MM--DD format"
    

def add_error(field,message):

    errors = field.get("error_reasons","")

    if errors:
        field["error_reasons"] = errors + "; " + message 
    else:
        field["error_reasons"] = message


def convert_data(raw):

    converted = []

    for item in raw:
        refined = item.copy()

        refined["error_reasons"] = refined.get("error_reasons","")

        #quantity conversion
        quantity = refined.get("quantity")
        if quantity is None or str(quantity).strip() == "":
            refined["quantity"] = None
            add_error(refined,"quantity is blank or missing")

        else:
            try:
                refined["quantity"] = int(quantity) 
            except ValueError:
                refined["quantity"] = None
                add_error(refined,"quantity must be integer")

        #unit_cost conversion
        unit_cost = refined.get("unit_cost")
        if unit_cost is None or str(unit_cost).strip() == "":
            refined["unit_cost"] = None
            add_error(refined, "unit_cost is missing or blank")

        else:
            try:
                refined["unit_cost"] = float(refined["unit_cost"])
            except ValueError:
                refined["unit_cost"] = None
                add_error(refined,"unit_cost must be in float format")

        #return date conversion
        parsed_return_date, return_date_error = parse_data(refined.get("return_date"),"return_date")

        refined["return_date"] = parsed_return_date
        if return_date_error:
            add_error(refined, return_date_error)

        converted.append(refined)

    return converted