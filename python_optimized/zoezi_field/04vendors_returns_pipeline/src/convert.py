
#Conversion rule:
    #line_id            → int
    #quantity_returned  → int
    #quantity_accepted  → int
    #unit_cost          → float
    #return_date        → date
    #received_date      → date or None

    #N/B
        #received_date is required only when return_status is Received, Rejected, or Closed.
        #received_date may be blank when return_status is Pending.

from datetime import datetime, date
from src.config import RETURN_DATE_ALLOWED_STATUS

def convert_data(data):

    converted = []

    for revert in data:

        retreats = revert.copy()
        retreats["error_reasons"] = None

        line_id = retreats["line_id"]
        qty_returned = retreats["quantity_returned"]
        qty_accepted = retreats["quantity_accepted"]
        unit_cost = retreats["unit_cost"]
        return_date = retreats["return_date"]
        received_date = retreats["received_date"]
        status = retreats["return_status"]

        if line_id not in (None, ""):
            try:
                retreats["line_id"] = int(line_id) 
            except ValueError:
                retreats["error_reasons"] = "{line_id conversion to integer failed"

        if qty_returned not in (None, ""):
            try:
                retreats["quantity_returned"] = int(qty_returned)
            except ValueError:
                retreats["error_reasons"] = "quantity_ordered conversion to integer failed"

        if qty_accepted not in (None, ""):
            try:
                retreats["quantity_accepted"] = int(qty_accepted)
            except ValueError:
                retreats["error_reasons"] = "quantity_accepted conversion to integer failed"

        if unit_cost not in (None, ""):
            try:
                retreats["unit_cost"] = float(unit_cost)
            except ValueError:
                retreats["error_reasons"] = "unit_cost conversion to float failed"

        if return_date not in (None, "") or str(return_date).strip():
            try:
                retreats["return_date"] = datetime.strptime(return_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                retreats["error_reasons"] = "return_date conversion to date failed"

  #received_date is required only when return_status is Received, Rejected, or Closed.
        if status in RETURN_DATE_ALLOWED_STATUS and received_date not in (None, "") and str(received_date).strip():
            
            try:
                retreats["received_date"] = datetime.strptime (received_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                retreats["error_reasons"] = "received_date conversion failed or received_date does not have the required return_status"

        converted.append(retreats)

    return converted