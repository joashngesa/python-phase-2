from pathlib import Path


def scan_folder(folder_path, files_pattern):

    input_dir = Path(folder_path)

    if not input_dir.exists():
        raise FileNotFoundError(f"⛔ no folder found in the path {folder_path} ❌")

    if not input_dir.is_dir():
        raise NotADirectoryError(
            f"🚩 the path {folder_path} does not contain a folder 🏮"
        )

    files = sorted(file for file in input_dir.glob(files_pattern) if file.is_file())

    if not files:
        raise ValueError(f"⚠️ the folder {folder_path} is empty ⁉️")

    return files
