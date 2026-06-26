
import os
import json
from pathlib import Path

def read_data(record):

    raw = Path(record)

    if not raw.exists():
        raise FileNotFoundError (f"🚫 The path {record} was not found")
    
    if raw.stat().st_size == 0:
        raise ValueError (f"⚠️ The {record} is empty")
     
    try:
        with open (raw, "r", encoding="utf-8") as file:
            raw = json.load (file)
    except json.JSONDecodeError as error:
        raise ValueError  (f"The {record} contains invalid json file: {error}")

    return raw