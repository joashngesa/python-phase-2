from pathlib import Path
import json


def read_file(file_path):

    raw = Path(file_path)

    if not raw.exists():
        raise FileNotFoundError(f"🚩 file not found in the file {file_path.name} ❗")

    if raw.stat().st_size == 0:
        raise ValueError(f"⚠️ the file in the file {file_path.name} is empty 🚫")

    try:
        with open(raw, "r", encoding="utf-8") as file:
            parsed_raw = json.load(file)

    except UnicodeDecodeError as error:
        raise ValueError(f"🚫 encoding error when reading the file ⛔")

    except json.JSONDecodeError as error:
        raise ValueError(f"⚠️ the file {file_path.name} contains invalid json file ⛔")

    return parsed_raw
