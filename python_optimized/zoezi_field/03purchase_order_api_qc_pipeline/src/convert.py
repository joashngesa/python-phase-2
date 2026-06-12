
from datetime import datetime, date

#Convert
    #line_id → int
    #quantity_ordered → int
    #quantity_received → int
    #unit_cost → float

def convert_data(data):
    converted = []

    for item in data:
        refined = item.copy()
        refined["error_reasons"] = None

        line_id = refined.get("line_id")
        try:
                refined["line_id"] = int(line_id) if not line_id in (None, "") else None
        except (ValueError, TypeError):
                refined["line_id"] = None

        qty_ordered = refined.get("quantity_ordered")
        try:
                refined["quantity_ordered"] = int (qty_ordered) if qty_ordered not in (None, "") else None
        except ValueError:
                refined["quantity_ordered"] = None
            
        qty_received = refined.get("quantity_received")
        try:
                refined["quantity_received"] = int (qty_received) if qty_received not in (None, "") else None
        except ValueError:
                refined["quantity_received"] = None

        unit_cost = refined.get("unit_cost")
        try:
                refined["unit_cost"] = float (unit_cost) if unit_cost not in (None, "") else None   
        except ValueError:
                refined["unit_cost"] = None

        order_date = refined.get("order_date")
        if order_date is None or not str(order_date).strip():
              refined["order_date"] = None

        try:
              refined["order_date"] = datetime.strptime(order_date.strip(), "%Y-%m-%d").date()
        except ValueError:
              refined["error_reasons"] = "invalid_date_format"

        expected_delivery_date = refined.get("expected_delivery_date")
        if expected_delivery_date is None or str(expected_delivery_date).strip():
               refined["expected_delivery_date"] = None

        try:
               refined["expected_delivery_date"] = datetime.strptime (expected_delivery_date.strip(), "%Y-%m-%d").date()
        except ValueError:
               refined["error_reasons"] = "invalid expected_delivery_date"

        converted.append(refined)

    return converted