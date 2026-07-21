from pathlib import Path
import json


def read_file(file_path):

    raw = Path(file_path)

    if not raw.exists():
        raise FileNotFoundError(f"🚩 file not found in the file {raw.name} ❗")

    if raw.stat().st_size == 0:
        raise ValueError(f"⚠️ the file in the file {raw.name} is empty 🚫")

    with open(raw, "r", encoding="utf-8") as file:
        return json.load(file)
