from datetime import datetime, date

"""
Conversion rules:
    inspection_date          → date or normalized date string
    odometer_km              → integer
    fuel_litres              → float
    fuel_cost_cad            → float
    engine_temperature_c     → float
    defect_reported          → boolean
"""


def add_error(field, message):

    error = field.get("error_reasons", "")

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
        return datetime.strptime(column, "%Y-%m-%d").date(), None
    except ValueError:
        return None, f"the {field_name} should be in the YYYY-MM-DD format"


def convert_data(extracted):

    converted = []

    # inspection_date validation

    for car in extracted:

        truck = car.copy()

        inspec_date, inspection_date_error = parse_dates(
            truck.get("inspection_date"), "inspection_date"
        )

        truck["inspection_date"] = inspec_date

        if inspection_date_error:
            add_error(truck, inspection_date_error)

        # convert odometer_km

        odometer = truck.get("odometer_km")
        if odometer is None or str(odometer).strip() == "":
            truck["odometer_km"] = None
            add_error(truck, "odometer_km is missing or blank")

        else:
            try:
                truck["odometer_km"] = int(odometer)
            except (ValueError, TypeError):
                truck["odometer_km"] = None
                add_error(truck, "odometer_km should be integer")

        # convert fuel litres
        fuel_litres = truck.get("fuel_litres")
        if fuel_litres is None or str(fuel_litres).strip() == "":
            truck["fuel_litres"] = None
            add_error(truck, "fuel_litres is missing or blank")

        else:
            try:
                truck["fuel_litres"] = float(fuel_litres)
            except (ValueError, TypeError):
                truck["fuel_litres"] = None
                add_error(truck, "fuel_litres should be float")

        # convert fuel_cost_cad
        fuel_cost_cad = truck.get("fuel_cost_cad")
        if fuel_cost_cad is None or str(fuel_cost_cad).strip() == "":
            truck["fuel_cost_cad"] = None
            add_error(truck, "fuel_cost_cad is missing or blank")

        else:
            try:
                truck["fuel_cost_cad"] = float(fuel_cost_cad)
            except (ValueError, TypeError):
                truck["fuel_cost_cad"] = None
                add_error(truck, "fuel_cost_cad should be float")

        # convert engine_temperature_c
        engine_temperature_c = truck.get("engine_temperature_c")
        if engine_temperature_c is None or str(engine_temperature_c).strip() == "":
            truck["engine_temperature_c"] = None
            add_error(truck, "engine_temperature_c is missing or blank")

        else:
            try:
                truck["engine_temperature_c"] = float(engine_temperature_c)
            except (ValueError, TypeError):
                truck["engine_temperature_c"] = None
                add_error(truck, "engine_temperature_c should be float")

        # convert defect_reported
        defect_reported = truck.get("defect_reported")
        if defect_reported is None or str(defect_reported).strip() == "":
            truck["defect_reported"] = None
            add_error(truck, "defect_reported is missing or blank")

            # normalize to a clean lowercase string
        value_string = str(defect_reported).strip().lower()

        if value_string in ("true", 1):
            truck["defect_reported"] = True

        elif value_string in ("false", 0):
            truck["defect_reported"] = False

        else:
            truck["defect_reported"] = None
            add_error(truck, "defect_reported should be a boolean value")

        converted.append(truck)

    return converted
