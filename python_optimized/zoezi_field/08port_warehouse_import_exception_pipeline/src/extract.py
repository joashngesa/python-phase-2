def extract_tables(raw):

    if isinstance(raw, list):
        return raw

    if isinstance(raw, dict):
        for name, table in raw.items():
            if (
                isinstance(table, list)
                and len(table) > 0
                and isinstance(table[0], dict)
            ):
                return table

            if isinstance(table, dict):
                try:
                    nested_table = extract_tables(table)
                    if nested_table:
                        return nested_table

                except ValueError:
                    # if this branch did not find the list, exit the loop and go to the next key
                    continue

    raise ValueError(f"🚩 could not find valid list of dictionary 🏮")


def extract_port(raw):

    port = raw.get("port")
    return port


def extract_batch_id(raw):

    batch_id = raw.get("batch_id")
    return batch_id
