from src.invalid import get_invalid_valid_raw

"""
Duplicate rule:
    purchase_order_id
    supplier_id
    product_category
"""


def get_valid_duplicate(valid_raw):

    valid = []
    duplicates = []
    seen_group = set()

    for procure in valid_raw:

        purchase_order_id = procure.get("purchase_order_id")
        supplier_id = procure.get("supplier_id")
        product_category = procure.get("product_category")
        group = (purchase_order_id, supplier_id, product_category)

        if group in seen_group:
            buy = procure.copy()
            buy["error_reasons"] = (
                "duplicate purchase_order_id, supplier_id, product_category"
            )
            duplicates.append(buy)

        else:
            seen_group.add(group)
            valid.append(procure.copy())

    return valid, duplicates
