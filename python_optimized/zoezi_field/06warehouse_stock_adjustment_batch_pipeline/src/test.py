
import os
from dotenv import load_dotenv
from tabulate import tabulate
from datetime import datetime, date

from src.config import RAW_DIR
from src.config import FILE_PATTERN

from src.scan import scan_data
from src.read import read_data
from src.convert import convert_data
from src.splitter import get_invalids_valids
from src.transform import transform_data
from src.summary import warehouse_summary

files = scan_data(RAW_DIR,FILE_PATTERN)
print(f"Files path: {files}")

print("\nRaw folder path: ",RAW_DIR)
print("Raw folder path name: ",RAW_DIR.name)
print("Check if directory exists: ",RAW_DIR.exists())
print("File pattern: ",FILE_PATTERN)

print("\nEverything inside the folder")
for item in RAW_DIR.iterdir():
    print(item.name)

for record in files:

    raw = read_data(record)
    print("\ntable: ",record.name)
    print(tabulate(raw, headers="keys", tablefmt="grid"))

    processed_at = datetime.now().isoformat(timespec="seconds")
    for file in raw:
        file["source_file"] = record.name
        file["processed_at"] = processed_at

    converted = convert_data (raw)
    print(f"\nConverted table: {record.name}")
    print(tabulate(converted, headers="keys", tablefmt="grid"))

    invalids, valids = get_invalids_valids (converted)
    print(f"\ninvalids table: {record.name}")
    print(tabulate(invalids, headers="keys", tablefmt="grid"))
    print(f"\nvalids table: {record.name}")
    print(tabulate(valids, headers="keys", tablefmt="grid"))

    transformed = transform_data (valids)
    print(f"\nTransformed_data: {record.name}")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))

    summary = warehouse_summary (transformed)
    print(f"\nwarehouse summary : {record.name}")
    print(tabulate(summary, headers="keys", tablefmt="grid"))