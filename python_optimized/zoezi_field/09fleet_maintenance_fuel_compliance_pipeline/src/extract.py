def extract_json(raw_data):

    if isinstance(raw_data, list):
        return raw_data

    if isinstance(raw_data, dict):
        for key, content in raw_data.items():

            if isinstance(content, list) and isinstance(content[0], dict):
                return content

            if isinstance(content, dict):
                try:
                    nested_data = extract_json(content)
                    if nested_data:
                        return nested_data
                except ValueError:

                    # if the above did not find the list, go to the next key
                    continue

    raise ValueError("could not find a valid list of dictionary")


def extract_depot(raw_data):

    depot = raw_data["metadata"]["depot"]
    return depot


def extract_batch_id(raw_data):

    batch_id = raw_data["metadata"]["batch_id"]
    return batch_id
