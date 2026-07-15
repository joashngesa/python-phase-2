from datetime import datetime, date

# numeric conversion
# declared_value_usd  -> float
# container_weight_kg -> float
# date conversions
# arrival_date
# customs_release_date
# warehouse_eta
# actual_warehouse_arrival


def add_error(field_name, message):

    error = field_name.get("error_reasons")

    if error:
        field_name["error_reasons"] = error + ": " + message
    else:
        field_name["error_reasons"] = message


def parse_date(column, field_name):
    if column is None:
        return None, f"{field_name} is missing"

    column = str(column).strip()

    if column == "":
        return None, f"{field_name} is blank"

    try:
        return datetime.strptime(column, "%Y-%m-%d").date(), None

    except:
        return None, f"the {field_name} should be in the YYYY-MM-DD format"


def convert_data(extracted_data):

    converted = []

    for event in extracted_data:

        altered = event.copy()

        # convert declared_value_usd
        declared_value = altered.get("declared_value_usd")

        if declared_value is None or str(declared_value).strip() == "":
            altered["declared_value_usd"] = None
            add_error(altered, "declared_value_usd is missing or blank")

        else:
            try:
                altered["declared_value_usd"] = float(declared_value)
            except:
                altered["declared_value_usd"] = None
                add_error(altered, "declared_value_usd should be a number")

        # convert container_weight_kg
        container_weight = altered.get("container_weight_kg")

        if container_weight is None or str(container_weight).strip() == "":
            altered["container_weight"] = None
            add_error(altered, "container_weight_kg is missing or blank")

        else:
            try:
                altered["container_weight_kg"] = float(container_weight)
            except:
                altered["container_weight_kg"] = None
                add_error(altered, "container_weight_kg should be a number")

        # convert arrival date
        cnv_arrival_date, cnv_date_error = parse_date(
            altered.get("arrival_date"), "arrival_date"
        )

        altered["arrival_date"] = cnv_arrival_date

        if cnv_date_error:
            add_error(altered, "arrival_date error")

        # convert customs_release_date
        cnv_release_date, release_date_error = parse_date(
            altered.get("customs_release_date"), "customs_release_date"
        )

        altered["customs_release_date"] = cnv_release_date

        if release_date_error:
            add_error(altered, "customs_release_date error")

        # convert warehouse_eta
        cnv_warehouse_eta, warehouse_eta_error = parse_date(
            altered.get("warehouse_eta"), "warehouse_eta"
        )

        altered["warehouse_eta"] = cnv_warehouse_eta

        if warehouse_eta_error:
            add_error(altered, "warehouse_eta error")

        # convert actual_warehouse_arrival
        cnv_warehouse_arrival, warehouse_arrrival_error = parse_date(
            altered.get("actual_warehouse_arrival"), "actual_warehouse_arrival"
        )

        altered["actual_warehouse_arrival"] = cnv_warehouse_arrival

        if warehouse_arrrival_error:
            add_error(altered, "actual_warehouse_arrival error")

        converted.append(altered)

    return converted
