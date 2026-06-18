def extract_data(raw):

    if isinstance (raw, list):
        return raw
    
    if isinstance (raw, dict):
        for key, value in raw.items():
            if isinstance (value, list) and isinstance (value[0], dict):
                return value

            if isinstance (value, dict):
                nested_data = extract_data(value)

                if nested_data:
                    return nested_data
                
    raise ValueError ("could not find a valid list of dictionaries in the json file")



def extract_metadata(raw):
    
    payload = raw.get("payload", {})

    return {
        "source": raw.get("source"),
        "status": raw.get("status"),
        "generated_at": raw.get("generated_at"),
        "record_count": raw.get("record_count"),
        "batch_id": payload.get("batch_id")
    }
    