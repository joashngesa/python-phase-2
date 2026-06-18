
import os
import csv
from pathlib import Path

def write_output(output_path,data,output_delimiter,output_columns):

    folder_path = os.path.dirname (output_path)

    if folder_path:
        os.makedirs(folder_path, exist_ok=True)

    try:
        with open (output_path, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=output_columns, delimiter=output_delimiter,extrasaction="ignore")
            writer.writeheader()
            writer.writerows(data)
            print("write output to: ",os.path.abspath(output_path))
    except PermissionError:
        print(f"\n❌PIPELINE_HALTED: permission denied when writing to {output_path}")
        print("💡Troubleshoot: please close all the applications opening the files and try again")