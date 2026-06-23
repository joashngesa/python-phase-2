
from pathlib import Path
import json

def read_file(file_path):

    raw_path = Path(file_path)

    if raw_path.stat().st_size == 0:
        raise ValueError (f"the file_path {file_path} is empty")
    
    try:
        with open (raw_path, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{file_path} contains invalid json file: {error}")
    
    return raw