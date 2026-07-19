# this modile is solely meant for testing purposes in the coding design duration

import json
import os
import shutil
from tabulate import tabulate
from datetime import datetime, date

from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR

from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_tables
from src.extract import extract_batch_id
from src.extract import extract_port
from src.convert import convert_data
from src.invalid import get_invalid_tbl
from src.valid import get_duplicates_valid
from src.transform import transform_data
from src.summary import summarize_table

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
        batch_id = extract_batch_id(raw)
        port = extract_port(raw)

        print(f"🏗️ Port: {port}")
        print(f"🪪 Batch_id: {batch_id}")
        extracted_files_count += 1

        processed_at = datetime.now()
        for row in extracted:
            row["processed_at"] = processed_at
            row["source_file"] = record.name

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

    invalid, valid_raw = get_invalid_tbl(converted)
    print(f"\n📕 invalid table: {record.name}")
    print(tabulate(invalid, headers="keys", tablefmt="grid"))

    duplicates, valid = get_duplicates_valid(valid_raw)
    print(f"\n📕 duplicates table: {record.name}")
    print(tabulate(duplicates, headers="keys", tablefmt="grid"))
    print(f"\n📄 valid table: {record.name}")
    print(tabulate(valid, headers="keys", tablefmt="grid"))

    transformed = transform_data(valid)
    print(f"\n📑 transformed table: {record.name}")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))

    table_summary = summarize_table(transformed)
    print(f"\n💹 table summary: {record.name}")
    print(tabulate(table_summary, headers="keys", tablefmt="grid"))

print(f"\nprocessed file count: {read_files_count}")
print(f"quarantined files after reading: {quarantined_files_count_from_reading}")
print(f"total files extracted: {extracted_files_count}")
print(f"quarantined files after extraction: {quarantined_files_count_from_extraction}")
