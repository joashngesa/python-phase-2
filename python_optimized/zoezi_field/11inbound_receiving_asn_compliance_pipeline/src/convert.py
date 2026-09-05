from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


def add_error(field, message):

    existing_errors = field.get("error_reasons", "")

    if existing_errors:
        field["error_reasons"] = f"{existing_errors} : {message}"

    else:
        field["error_reasons"] = message


def parse_date(column, field_name):

    if column is None:
        return None, f"{field_name} is missing"

    column = str(column).strip()

    if column == "":
        return None, f"{field_name} is blank"

    try:
        return datetime.strptime(column, "%Y-%m-%d").date(), None

    except ValueError:
        return None, f"{field_name} should be in date format"


def convert_data(raw_file):

    converted = []
    conversion_error_count = 0

    logger.debug("Conversion initiated | raw_record_count=%d", len(raw_file))

    for procure in raw_file:

        buy = procure.copy()

        # ordered_qty conversion
        ordered_qty = buy.get("ordered_qty")
        if ordered_qty is None or str(ordered_qty).strip() == "":
            buy["ordered_qty"] = None
            add_error(buy, "ordered_qty is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["ordered_qty"] = int(ordered_qty)

            except (ValueError, TypeError):
                buy["ordered_qty"] = None
                add_error(buy, "ordered_qty should be integer")
                conversion_error_count += 1

        # shipped_qty conversion
        shipped_qty = buy.get("shipped_qty")
        if shipped_qty is None or str(shipped_qty).strip() == "":
            buy["shipped_qty"] = None
            add_error(buy, "shipped_qty is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["shipped_qty"] = int(shipped_qty)

            except (ValueError, TypeError):
                buy["shipped_qty"] = None
                add_error(buy, "shipped_qty should be integer")
                conversion_error_count += 1

        # received_qty conversion
        received_qty = buy.get("received_qty")
        if received_qty is None or str(received_qty).strip() == "":
            buy["received_qty"] = None
            add_error(buy, "received_qty is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["received_qty"] = int(received_qty)

            except (ValueError, TypeError):
                buy["received_qty"] = None
                add_error(buy, "received_qty should be integer")
                conversion_error_count += 1

        # unit_cost conversion
        unit_cost = buy.get("unit_cost")
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

        # damaged_qty
        damaged_qty = buy.get("damaged_qty")
        if damaged_qty is None or damaged_qty.strip() == "":
            buy["damaged_qty"] = None
            add_error(buy, "damaged_qty is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["damaged_qty"] = int(damaged_qty)

            except (ValueError, TypeError):
                buy["damaged_qty"] = None
                add_error(buy, "damaged_qty should be integer")
                conversion_error_count += 1

        # order_date conversion
        parsed_order_date, order_date_error = parse_date(
            buy["order_date"], "order_date"
        )

        buy["order_date"] = parsed_order_date

        if order_date_error:
            add_error(buy, order_date_error)
            conversion_error_count += 1

        # promised_delivery_date conversion
        parsed_promised_delivery_date, promised_delivery_date_error = parse_date(
            buy["promised_delivery_date"], "promised_delivery_date"
        )

        buy["promised_delivery_date"] = parsed_promised_delivery_date

        if promised_delivery_date_error:
            add_error(buy, promised_delivery_date_error)
            conversion_error_count += 1

        # ship_date conversion
        parsed_ship_date, ship_date_error = parse_date(buy["ship_date"], "ship_date")

        buy["ship_date"] = parsed_ship_date

        if ship_date_error:
            add_error(buy, ship_date_error)
            conversion_error_count += 1

        # receipt_date conversion
        parsed_receipt_date, receipt_date_error = parse_date(
            buy["receipt_date"], "receipt_date"
        )

        buy["receipt_date"] = parsed_receipt_date

        if receipt_date_error:
            add_error(buy, receipt_date_error)
            conversion_error_count += 1

        converted.append(buy)

    logger.info(
        "Conversion completed | conversion_error_count=%d", conversion_error_count
    )

    return converted
