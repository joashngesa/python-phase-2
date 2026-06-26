
import json
from pathlib import Path

def scan_data(directory_path, pattern):

    folder_path = Path(directory_path)

    if not folder_path.exists():
        raise FileNotFoundError (f"🚫 The {folder_path} does not exist")
    
    if not folder_path.is_dir():
        raise NotADirectoryError (f"❌ The {folder_path} is not a directory")
    
    record = sorted (file for file in folder_path.glob(pattern) if file.is_file())

    if not record:
        print(f"\n⚠️ Files not found in {folder_path} using pattern {pattern} 🚨")

    return record