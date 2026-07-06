
from datetime import datetime, date

#Output
    #required_temp_min_c -> float
    #required_temp_max_c -> float
    #actual_temp_c       -> float
    #exposure_minutes    -> int
    #incident_rate       -> date

def add_error (field, message):

    errors = field.get("error_reasons")

    if errors:
        field["error_reasons"] = errors + message
    else:
        field["error_reasons"] = message



def parse_date (value, field_name):

    if value is None:
        return None, f"{field_name} is missing"

    value = str(value).strip()

    if value == "":
        return None, f"{field_name} is blank"
    
    try:
        return datetime.strptime(value, "%Y-%m-%d").date(), None
    except ValueError:
        return None, f"{field_name} should be in YYYY-MM-DD format" 


def convert_data (extracted):
    
    converted_tbl = []

    for event in extracted:

        converted = event.copy()

        min_temp = converted.get("required_temp_min_c")
        if min_temp in (None, ""):
            converted["required_temp_min_c"] = None
            add_error(converted, "required_min_temperature is missing or blank")

        try:
            converted["required_temp_min_c"] = float(min_temp)
        except ValueError as error:
            converted["required_temp_min_c"] = None
            add_error(converted, "Required_minimum temperature should be a number")


        max_temp = converted.get("required_temp_max_c")
        if max_temp in (None, ""):
            converted["required_temp_max_c"] = None
            add_error(converted, "required_max_temperature is missing or blank") 

        else:
            try:
                converted["required_temp_max_c"] = float (max_temp)
            except ValueError as error:
                converted["required_temp_max_c"] = None
                add_error(converted, "required_max_temperature should be a number") 


        actual_temp = converted.get("actual_temp_c")
        if actual_temp is (None, ""):
            converted["actual_temp_c"] = None
            add_error(converted, "actual_temp_c is missing or blank") 
        else:
            try:
                converted["actual_temp_c"] = float (actual_temp)
            except ValueError as error:
                converted["actual_temp_c"] = None
                add_error(converted, "actual_temp should be a number") 

        
        exposure_min = converted.get("exposure_minutes")
        if exposure_min in (None, ""):
            converted["exposure_minutes"] = None
            add_error(converted, "exposure_minutes is missing or blank")
        else:
            try:
                converted["exposure_minutes"] = int (exposure_min)
            except ValueError:
                converted["exposure_minutes"] = None
                add_error(converted, "exposure minutes ahould be integer") 


        parsed_incident_date, incident_date_error = parse_date (converted.get("incident_date"), "incident_date")

        converted["incident_date"] = parsed_incident_date
        if incident_date_error:
            add_error (converted, "incident_date error")

        
        converted_tbl.append(converted)

    return converted_tbl