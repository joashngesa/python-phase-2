from pathlib import Path


def scan_folder(input_folder: Path, file_pattern: str):

    input_dir = Path(input_folder)

    if not input_dir.exists():
        raise FileNotFoundError(f"{input_dir} is not found")

    if not input_dir.is_dir():
        raise NotADirectoryError(f"{input_dir} is not a directory")

    records = sorted(file for file in input_dir.glob(file_pattern) if file.is_file())

    if not records:
        raise ValueError(f"no files matching {file_pattern}")

    return records
