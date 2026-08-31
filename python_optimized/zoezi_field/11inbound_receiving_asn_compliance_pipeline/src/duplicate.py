def get_duplicates(valid):

    duplicates = []
    seen_id = set()

    for procure in valid:

        receipt_id = procure.get("receipt_id")

        if receipt_id in seen_id:
            buy = procure.copy()
            buy["duplicates"] = "duplicate receipt_id"
            duplicates.append(buy)

        else:
            seen_id.add(receipt_id)

    return duplicates
