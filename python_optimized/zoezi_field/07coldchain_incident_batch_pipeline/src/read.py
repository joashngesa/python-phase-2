
from pathlib import Path
import json

def read_data (file_path):

    raw = Path (file_path)

    if not raw.exists():
        raise FileNotFoundError (f"⚠️ the file_path give is not found 🚨")
    
    if raw.stat().st_size == 0:
        raise ValueError (f"⚠️ the file in the path given is empty 🚩")
    
    try:
        with open (raw, "r", encoding="utf-8") as file:
            pared_json = json.load (file)

    except json.JSONDecodeError as error:
        raise ValueError (f"⛔The file path contains invalid json file: {error} 🚨")
    
    except UnicodeDecodeError as error:
        raise ValueError (f"❌ Encoding error 🚨 ")
    
    return pared_json