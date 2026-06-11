# Extract python object from the data

def extract_data(raw):

    if isinstance (raw, list):
        return raw
    
    if isinstance (raw, dict):

        for key, value in raw.items():
            if isinstance (value, list) and len(value) > 0 and isinstance (value[0], dict):
                return value
            
            if isinstance (value, dict):
                nested_data = extract_data(value)

                if nested_data:
                    return nested_data
    
    raise ValueError ("could not find a valid list of dictionaries from the data")