
#Dynamic key hunting
    #Instead of forcing the file to have a "data" key, you can make Python scan the dictionary
    #.. and look for any key that holds a list of dictionaries. This ignores metadata objects
    #.. and automatically extracts the actual records

def extract_records_flexible(data):
    # 1. If it's already a flat list, return it
    if isinstance(data, list):
        return data

    # 2. If it's a dictionary, look inside it
    if isinstance(data, dict):
        # Scan all keys (e.g., "meta", "payload", "shipments")
        for key, value in data.items():
            # If a value is a list, we found our records container!
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                return value
            
            # Recursively check nested dictionaries 
            if isinstance(value, dict):
                nested_result = extract_records_flexible(value)
                if nested_result:
                    return nested_result

    raise ValueError("Could not find a valid list of record dictionaries in the JSON.")




#Explicit target keys

def extract_records_with_target(data, target_key="data"):
    if isinstance(data, list):
        return data

    elif isinstance(data, dict):
        # Check if the target key is inside the top-level or nested payload
        if target_key in data:
            records = data[target_key]
        elif "payload" in data and target_key in data["payload"]:
            records = data["payload"][target_key]
        else:
            raise ValueError(f"Could not find the '{target_key}' key in the data structure.")
        
        # Keep your original validations for safety
        if not isinstance(records, list):
            raise ValueError(f"The data inside '{target_key}' must be a list.")
        return records

    else:
        raise ValueError("Invalid JSON format.")
