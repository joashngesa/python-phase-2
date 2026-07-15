# this modile is solely meant for testing purposes in the coding design duration

import json
import os
import shutil
from tabulate import tabulate

from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR

from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_tables
from src.convert import convert_data

files = scan_folder(INPUT_DIR, FILE_PATTERN)
print("\nfiles discovered: ", len(files))
print(files)

for file in files:
    print(f"\n🪦 {file.name}")

read_files_count = 0
quarantined_files_count_from_reading = 0
extracted_files_count = 0
quarantined_files_count_from_extraction = 0

for record in files:

    try:
        raw = read_file(record)
        print(f"\n📔 file name: {record.name}")
        print(record)
        read_files_count += 1

    except ValueError as error:
        print(f"\n📕 file_name: {record.name} has a reading error\n")
        print(f"🏮 the file {record.stem} has error {error} ⚠️")
        quarantine = QUARANTINE_DIR / record.name
        shutil.move(record, quarantine)
        quarantined_files_count_from_reading += 1
        continue

    try:
        extracted = extract_tables(raw)
        print(f"\n📖 extracted file_name: {record.name}")
        print(tabulate(extracted, headers="keys", tablefmt="grid"))
        extracted_files_count += 1

    except ValueError as error:
        print(
            f"\n📕 the file {record.stem} has failed extraction due to structure failure"
        )
        print(f"🚫 the file {record.name} has an error: {error} ❌")
        quarantine = QUARANTINE_DIR / record.name
        shutil.move(record, quarantine)
        quarantined_files_count_from_extraction += 1
        continue

    converted = convert_data(extracted)
    print(f"\n📜 converted file: {record.name}")
    print(tabulate(converted, headers="keys", tablefmt="grid"))

print(f"\nprocessed file count: {read_files_count}")
print(f"quarantined files after reading: {quarantined_files_count_from_reading}")
print(f"total files extracted: {extracted_files_count}")
print(f"quarantined files after extraction: {quarantined_files_count_from_extraction}")
