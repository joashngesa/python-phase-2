from pathlib import Path
import json

def read_json_files(file_path):

    raw_path =  Path(file_path)
    if not raw_path.exists():
        raise FileNotFoundError(F"The file {file_path} was not found")
    
    if raw_path.stat().st_size == 0:
        raise ValueError(f"The {file_path} is empty")

    try:
        with open (raw_path, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"the {file_path} contains invalid json file: {error}")
    
    return raw