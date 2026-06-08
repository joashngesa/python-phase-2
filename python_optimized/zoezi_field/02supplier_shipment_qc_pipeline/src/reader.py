import json
from pathlib import Path

def read_json_file(file_path):

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError (f"the file_path {file_path} not found")
    
    if path.stat().st_size == 0:
        raise ValueError (f"the file {file_path} is empty")
    
    try:
        with open (path, "r", encoding="utf-8") as file:
            raw = json.load(file)

    except json.JSONDecoder as error:
        raise ValueError (f"{file_path} contains invalid json: {error}")
    
    return raw