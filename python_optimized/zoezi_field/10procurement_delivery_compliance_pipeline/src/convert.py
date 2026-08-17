from datetime import datetime, date


def add_error(field, new_error):

    existing_error = field.get("error_reasons", "")
    if existing_error:
        field["error_reasons"] = f"{existing_error} : {new_error}"

    else:
        field["error_reasons"] = new_error


def parse_date(column, field_name):

    if column is None:
        return None, f"{field_name} is missing"

    column = str(column).strip()

    if column == "":
        return None, f"{field_name} is blank"

    try:
        return datetime.strptime(column, "%Y-%m-%d").date(), None

    except ValueError:
        return None, f"{field_name} should be in date format_YYYY-MM-DD"


def convert_data(extracted):

    converted = []
    conversion_error_count = 0

    for procure in extracted:

        buy = procure.copy()

        # convert quantity_ordered -> int
        quantity_ordered = buy.get("quantity_ordered")
        if quantity_ordered is None or str(quantity_ordered).strip() == "":
            buy["quantity_ordered"] = None
            add_error(buy, "quantity_ordered is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["quantity_ordered"] = int(quantity_ordered)
            except (ValueError, TypeError):
                buy["quantity_ordered"] = None
                add_error(buy, "quantity_ordered should be integer")
                conversion_error_count += 1

        # convert quantity_received -> int
        quantity_received = buy.get("quantity_received")
        if quantity_received is None or str(quantity_received).strip() == "":
            buy["quantity_received"] = None
            add_error(buy, "quantity_received is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["quantity_received"] = int(quantity_received)

            except (ValueError, TypeError):
                buy["quantity_received"] = None
                add_error(buy, "quantity_received should be integer")
                conversion_error_count += 1

        # convert unit_cost -> float
        unit_cost = buy["unit_cost"]
        if unit_cost is None or str(unit_cost).strip() == "":
            buy["unit_cost"] = None
            add_error(buy, "unit_cost is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["unit_cost"] = float(unit_cost)

            except (ValueError, TypeError):
                buy["unit_cost"] = None
                add_error(buy, "unit_cost should be float")
                conversion_error_count += 1

        # convert approved_budget -> float
        approved_budget = buy.get("approved_budget")
        if approved_budget is None or str(approved_budget).strip() == "":
            buy["approved_budget"] = None
            add_error(buy, "approved_budget is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["approved_budget"] = float(approved_budget)

            except (ValueError, TypeError):
                buy["approved_budget"] = None
                add_error(buy, "approved_budget is missing or blank")
                conversion_error_count += 1

        # convert order_date -> date
        parsed_order_date, order_date_error = parse_date(
            buy.get("order_date"), "order_date"
        )

        buy["order_date"] = parsed_order_date

        if order_date_error:
            add_error(buy, order_date_error)
            conversion_error_count += 1

        # convert expected_delivery_date -> date
        parsed_expected_delivery_date, expected_delivery_date_error = parse_date(
            buy.get("expected_delivery_date"), "expected_delivery_date"
        )

        buy["expected_delivery_date"] = parsed_expected_delivery_date

        if expected_delivery_date_error:
            add_error(buy, expected_delivery_date_error)
            conversion_error_count += 1

        # convert actual_delivery_date -> date | allow none & ""
        actual_delivery_date = buy.get("actual_delivery_date")
        if actual_delivery_date is None or str(actual_delivery_date).strip() == "":
            buy["actual_delivery_date"] = None

        else:
            parsed_actual_delivery_date, actual_delivery_date_error = parse_date(
                buy.get("actual_delivery_date"), "actual_delivery_date"
            )

            buy["actual_delivery_date"] = parsed_actual_delivery_date

            if actual_delivery_date_error:
                add_error(buy, actual_delivery_date_error)
                conversion_error_count += 1

        converted.append(buy)

    return converted
