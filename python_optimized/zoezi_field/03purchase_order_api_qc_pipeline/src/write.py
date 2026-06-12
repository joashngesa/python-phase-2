import os
from pathlib import Path
import csv

def write_output(output_path,data,output_delimiter,output_columns):

    output_folder = os.path.dirname (output_path)
    if output_folder:
        os.makedirs (output_folder, exist_ok=True)

    try:
        with open (output_path, "w", encoding="utf-8") as file:
            writer = csv.DictWriter (file,delimiter=output_delimiter,fieldnames=output_columns,extrasaction="ignore")
            writer.writeheader()
            writer.writerows(data)
            print("write output to: ",os.path.abspath(output_path))
    except PermissionError:
        print(f"\n❌PIPELINE HALTED:permission denied when writing to {output_path}")
        print(f"💡Troubleshoot: please close the applications opening the file and try again")
        