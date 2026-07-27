from pathlib import Path


def scan_folder(input_path, file_pattern):

    raw_path = Path(input_path)

    if not raw_path.exists:
        raise FileNotFoundError(f"no input folder found in {raw_path}")

    if not raw_path.is_dir():
        raise NotADirectoryError(f"no folder found in {raw_path}")

    files = sorted(record for record in raw_path.glob(file_pattern) if record.is_file())

    if not files:
        raise ValueError(f"no files found matching the pattern {file_pattern}")

    return files
