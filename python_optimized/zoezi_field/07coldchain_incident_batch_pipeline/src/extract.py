def extract_data(raw_data):

    if isinstance(raw_data, list):
        return raw_data

    if isinstance(raw_data, dict):
        for name, table in raw_data.items():
            if isinstance(table, list) and isinstance(table[0], dict):
                return table

            if isinstance(table, dict):
                nested_table = extract_data(table)

                if nested_table:
                    return nested_table

    raise ValueError("❌ Could not find valid list of dictionary 🚨")


def extract_region(raw_data):

    region = raw_data.get("region")
    return region


def extract_batch(raw_data):

    batch_id = raw_data.get("batch_id")
    return batch_id
