
from pathlib import Path

def scan_input_folder(directory_path, pattern):

    folder_path = Path(directory_path)

    if not folder_path.exists():
        raise FileNotFoundError (f"⛔ The input directory does not exist 🚨")
    
    if not folder_path.is_dir():
        raise NotADirectoryError (f"⛔ The input directory is not a fodler. 🚨")
    
    files = sorted (record for record in folder_path.glob(pattern) if record.is_file())

    if not files:
        raise(f"⚠️ Files with the pattern {pattern} was not found in input folder_path ❌")

    return files