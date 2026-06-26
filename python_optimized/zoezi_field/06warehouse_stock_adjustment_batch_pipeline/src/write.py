
import csv
import os
from pathlib import Path

def write_output (output_path, data, output_delimiter, output_fields):

    folder_path = os.path.dirname (output_path)

    if folder_path:
        os.makedirs (folder_path, exist_ok=True)

    try:
        with open (output_path, "w", encoding="utf-8") as file:
            write = csv.DictWriter (file, fieldnames=output_fields, delimiter=output_delimiter, extrasaction="ignore")
            write.writeheader()
            write.writerows(data)
            print("write to: ",os.path.abspath (output_path))
    except PermissionError:
        print(f"❌ Permission denied when writing to {output_path} 🚫")