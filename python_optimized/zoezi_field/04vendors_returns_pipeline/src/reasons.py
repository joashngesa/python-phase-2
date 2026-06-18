
#output:
    #return_reason
    #valid_line_count
    #total_returned_qty
    #total_accepted_qty
    #total_rejected_qty
    #total_return_value
    #total_accepted_value
    #avg_acceptance_rate

def reasons_summary(valids):

    reasons = {}

    for revert in valids:
        logic = revert.copy()

        return_reason = logic.get("return_reason")
        qty_returned = logic.get("quantity_returned")
        qty_accepted = logic.get("quantity_accepted")
        unit_cost = logic.get("unit_cost")

        qty_rejected = qty_returned - qty_accepted
        return_value = qty_returned * unit_cost
        accepted_value = qty_accepted * unit_cost

        if return_reason not in reasons:
            reasons[return_reason] = {
                "return_reason": return_reason,
                "valid_line_count": 0,
                "total_returned_qty": 0,
                "total_accepted_qty": 0,
                "total_rejected_qty": 0,
                "total_return_value": 0,
                "total_accepted_value": 0,
                "avg_acceptance_rate": 0
            }

        reasons[return_reason]["valid_line_count"] += 1
        reasons[return_reason]["total_returned_qty"] += qty_returned
        reasons[return_reason]["total_accepted_qty"] += qty_accepted
        reasons[return_reason]["total_rejected_qty"] += qty_rejected
        reasons[return_reason]["total_return_value"] += return_value
        reasons[return_reason]["total_accepted_value"] += accepted_value
        
    for key, record in reasons.items():
        if record["total_returned_qty"] > 0:
            record["avg_acceptance_rate"] = round(record["total_accepted_qty"] / record["total_returned_qty"])
        else:
            record["avg_acceptance_rate"] = 0.0

    return list(reasons.values())