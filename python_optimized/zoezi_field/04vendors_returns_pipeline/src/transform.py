


#expected output:
    #return_value = quantity_returned * unit_cost
    #accepted_value = quantity_accepted * unit_cost
    #rejected_qty = quantity_returned - quantity_accepted
    #acceptance_rate = quantity_accepted / quantity_returned
    #processing_days = received_date - return_date
        ##N/B: if the received_date is none, set processing days to none
            
def get_return_value(revert):
    return revert.get("quantity_returned") * revert.get("unit_cost")


def get_accepted_value(revert):
    return revert.get("quantity_accepted") * revert.get("unit_cost")


def get_rejected_quantity(revert):
    return revert.get("quantity_returned") - revert.get("quantity_accepted")


def get_acceptance_rate(revert):

    if not revert["quantity_returned"]:
        return 0.0
    return revert.get("quantity_accepted") / revert.get("quantity_returned")


def get_processing_days(revert):

    received_date = revert.get("received_date")
    if received_date in (None, ""):
        return None
    else:
        return (revert.get("received_date") - revert.get("return_date")).days  

    #resolution_status:
        #Pending → Awaiting Receipt
        #Rejected → Rejected by Vendor
        #Closed → Closed
        #Received + accepted == returned → Fully Accepted
        #Received + accepted < returned → Partially Accepted
def get_resolution_status(revert):
    status = revert.get("return_status")
    qty_returned = revert.get("quantity_returned")
    qty_accepted = revert.get("quantity_accepted")
    if status == "Pending":
        return "Awaiting receipt" 
    if status == "Rejected":
        return "Rejected by vendor"
    if status == "Closed":
        return "Closed"
    if status == "Received" and qty_accepted == qty_returned:
        return "Fully accepted"
    if status == "Received" and qty_accepted < qty_returned:
        return "Partially accepted"


def transform_data(valids):
    return [
        {
            "return value": get_return_value(revert),
            "accepted value": get_accepted_value(revert),
            "rejected quantity": get_rejected_quantity(revert),
            "acceptance rate": get_acceptance_rate(revert),
            "processing days": get_processing_days(revert),
            "resolution status": get_resolution_status(revert)
        }
        for revert in valids
    ]
