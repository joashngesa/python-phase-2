
#Convert module:

def convert_record(record):
    converted = record.copy()
    conversion_errors = {}

    quantity_raw = converted.get("quantity")

    if quantity_raw in ("", None):
        converted["quantity"] = None
        conversion_errors["quantity"] = "quantity is missing"
    else:
        try:
            converted["quantity"] = int(quantity_raw)
        except ValueError:
            converted["quantity"] = None
            conversion_errors["quantity"] = "quantity must be an integer"

    unit_cost_raw = converted.get("unit_cost")

    if unit_cost_raw in ("", None):
        converted["unit_cost"] = None
        conversion_errors["unit_cost"] = "unit_cost is missing"
    else:
        try:
            converted["unit_cost"] = float(unit_cost_raw)
        except ValueError:
            converted["unit_cost"] = None
            conversion_errors["unit_cost"] = "unit_cost must be a number"

    converted["_conversion_errors"] = conversion_errors

    return converted


#validate module;
#REQUIRED_FIELDS & ALLOWED_ADJUSTMENT_TYPES are put in quotes for illustration only!
def validate_record(record):
    errors = []

    for field in "REQUIRED_FIELDS":
        if field not in record:
            errors.append(f"{field} is missing")

    conversion_errors = record.get("_conversion_errors", {})
    for field, message in conversion_errors.items():
        errors.append(message)

    quantity = record.get("quantity")
    if quantity is not None and quantity <= 0:
        errors.append("quantity must be greater than 0")

    unit_cost = record.get("unit_cost")
    if unit_cost is not None and unit_cost <= 0:
        errors.append("unit_cost must be greater than 0")

    adjustment_type = record.get("adjustment_type")
    if adjustment_type not in "ALLOWED_ADJUSTMENT_TYPES":
        errors.append("adjustment_type is not allowed")

    if errors:
        return False, "; ".join(errors)

    return True, ""