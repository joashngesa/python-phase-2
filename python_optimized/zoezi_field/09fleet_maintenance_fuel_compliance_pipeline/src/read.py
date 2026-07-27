import json
from pathlib import Path


def read_file(file_path):

    raw = Path(file_path)

    if not raw.exists():
        raise FileNotFoundError(f"file not found in {raw}")

    if raw.stat().st_size == 0:
        raise ValueError(f"the file {raw.name} is empty")

    with open(raw, "r", encoding="utf-8") as file:
        return json.load(file)
