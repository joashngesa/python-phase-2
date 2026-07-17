# duplicate rule:
# event_id has appeared before
# container_id + arrival_date combination has appeared before


def get_duplicates_valid(valid_raw):

    valid = []
    duplicates = []
    seen_event_id = set()
    seen_cont_id_arrivaldate = set()

    for event in valid_raw:

        event_id = event.get("event_id")
        container_id = event.get("container_id")
        arrival_date = event.get("arrival_date")
        dup_key = (container_id, arrival_date)

        is_duplicate = False
        reasons = []

        if event_id in seen_event_id:
            is_duplicate = True
            reasons.append("event_id duplicate")

        if dup_key in seen_cont_id_arrivaldate:
            is_duplicate = True
            reasons.append("container_id & arrival_date group duplicate")

        if is_duplicate:
            replica = event.copy()
            replica["error_reasons"] = "& ".join(reasons)
            duplicates.append(replica)

        else:
            valid.append(event.copy())

        seen_event_id.add(event_id)
        seen_cont_id_arrivaldate.add(dup_key)

    return duplicates, valid
