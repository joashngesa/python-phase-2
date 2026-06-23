
from pathlib import Path

def scan_folder(folder_path,pattern):

    directory = Path(folder_path)

    if not directory.exists():
        raise FileNotFoundError(f"the directory {directory} does not exist")

    if not directory.is_dir():
        raise NotADirectoryError(f"path is not a directory: {directory}")
    
    files = sorted(directory.glob(pattern))

    return [file for file in files if file.is_file()]