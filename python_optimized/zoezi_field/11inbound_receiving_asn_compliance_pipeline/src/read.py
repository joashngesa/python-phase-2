import json
from pathlib import Path


def read_json_file(file_path):

    raw_path = Path(file_path)

    if raw_path.stat().st_size == 0:
        raise ValueError(f"{file_path} is empty")

    with raw_path.open("r", encoding="utf-8") as file:
        raw_file = json.load(file)

    if not isinstance(raw_file, list):
        raise TypeError(f"{raw_path.name} is expecting a list")

    return raw_file
