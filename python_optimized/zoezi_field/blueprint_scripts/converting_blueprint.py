from datetime import datetime


def parse_date(value, field_name):
    if value is None:
        return None, f"{field_name} is missing"

    value = str(value).strip()

    if value == "":
        return None, f"{field_name} is blank"

    try:
        return datetime.strptime(value, "%Y-%m-%d").date(), None
    except ValueError:
        return None, f"{field_name} must be in YYYY-MM-DD format"


def add_error(record, message):
    current = record.get("error_reason", "")

    if current:
        record["error_reason"] = current + "; " + message
    else:
        record["error_reason"] = message


def convert_data(records):
    converted = []

    for record in records:
        refined = record.copy()

        refined["error_reason"] = refined.get("error_reason", "")

        # line_id
        try:
            refined["line_id"] = int(refined["line_id"]) if refined.get("line_id") not in (None, "") else None
        except (ValueError, TypeError):
            refined["line_id"] = None
            add_error(refined, "line_id must be an integer")

        # quantity_ordered
        try:
            refined["quantity_ordered"] = int(refined["quantity_ordered"]) if refined.get("quantity_ordered") not in (None, "") else None
        except (ValueError, TypeError):
            refined["quantity_ordered"] = None
            add_error(refined, "quantity_ordered must be an integer")

        # quantity_received
        try:
            refined["quantity_received"] = int(refined["quantity_received"]) if refined.get("quantity_received") not in (None, "") else None
        except (ValueError, TypeError):
            refined["quantity_received"] = None
            add_error(refined, "quantity_received must be an integer")

        # unit_cost
        try:
            refined["unit_cost"] = float(refined["unit_cost"]) if refined.get("unit_cost") not in (None, "") else None
        except (ValueError, TypeError):
            refined["unit_cost"] = None
            add_error(refined, "unit_cost must be a number")

        # order_date
        parsed_order_date, order_date_error = parse_date(
            refined.get("order_date"),
            "order_date")

        refined["order_date"] = parsed_order_date

        if order_date_error:
            add_error(refined, order_date_error)

        # expected_delivery_date
        parsed_expected_date, expected_date_error = parse_date(
            refined.get("expected_delivery_date"),
            "expected_delivery_date")

        refined["expected_delivery_date"] = parsed_expected_date

        if expected_date_error:
            add_error(refined, expected_date_error)

        converted.append(refined)

    return converted
