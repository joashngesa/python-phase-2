
def extract_data(raw):

    if isinstance (raw, list):
        return raw
    
    if isinstance (raw, dict):

        for key, value in raw.items():
            if isinstance (value, list) and isinstance (value[0], dict):
                return value

    raise ValueError ("could not find valid list of dictionaries")        