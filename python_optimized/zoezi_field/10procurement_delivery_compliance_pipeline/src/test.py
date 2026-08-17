"""
This module is designed for testing the modules as i design the pipeline.
The pipeline will not be run through this module.
"""

from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR

import shutil
from tabulate import tabulate
from datetime import datetime
from src.convert import convert_data
from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_table
from src.extract import extract_depot
from src.extract import extract_batch_id
from src.invalid import get_invalid_valid_raw
from src.valid import get_valid_duplicate
from src.transform import transform_data
from src.summary import summarize_table

files = scan_folder(INPUT_DIR, FILE_PATTERN)

print("📁 Folder scanning ...🔎")
for raw_path in files:
    print(f"📂 total files discovered: {len(files)}")
    print(f"📥 File_name: {raw_path.name}\n")

read_file_count = 0
quarantined_file_from_read_count = 0
extracted_file_count = 0
quarantined_file_from_extracted_count = 0

for file in files:
    try:
        raw = read_file(file)
        print(f"🗂️ raw file name: {file.name}\n")
        print(raw)
        read_file_count += 1
    except (ValueError, OSError) as error:
        print(f"❌ File read failed: {file.name} 🚩")
        print(f"🚫 {file.name}: {error} 🚩")
        quarantine = QUARANTINE_DIR / file.name
        shutil.move(file, quarantine)
        quarantined_file_from_read_count += 1
        continue

    try:
        extracted = extract_table(raw)
        batch_id = extract_batch_id(raw)
        depot = extract_depot(raw)
        print(f"\n📜 Extracted file name: {file.name}")
        print(f"🏗️ {file.name} Depot name: {depot}")
        print(f"🪪 {file.name} Batch_id: {batch_id}")
        print(tabulate(extracted, headers="keys", tablefmt="grid"))
        extracted_file_count += 1
    except (ValueError, KeyError) as error:
        print(f"\n‼️ {file.name} extraction failed 🚩")
        print(f"⛔ {file.name} extraction error: {error}")
        quarantine = QUARANTINE_DIR / file.name
        shutil.move(file, quarantine)
        quarantined_file_from_extracted_count == 1
        continue

    source_file = file.name
    processed_at = datetime.now()
    for data in extracted:
        data["processed_at"] = processed_at
        data["source_file"] = source_file

    converted = convert_data(extracted)
    print(f"\n📄 converted {file.name}")
    print(tabulate(converted, headers="keys", tablefmt="grid"))

    invalid, valid_raw = get_invalid_valid_raw(converted)
    print(f"📕 Invalid {file.name}")
    print(tabulate(invalid, headers="keys", tablefmt="grid"))

    valid, duplicates = get_valid_duplicate(valid_raw)
    print(f"📖 {file.name} duplicates")
    print(tabulate(duplicates, headers="keys", tablefmt="grid"))
    print(f"💹 {file.name} valid")
    print(tabulate(valid, headers="keys", tablefmt="grid"))

    transformed = transform_data(valid)
    print(f"📑 {file.name} transformed")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))

    summary = summarize_table(transformed)
    print(f"📊 {file.name} summary")
    print(tabulate(summary, headers="keys", tablefmt="grid"))

print(f"\n📂 Files discovered count: {len(files)}")
print(f"✔️ read_file_count: {read_file_count}")
print(f"📦 quarantined_file_from_read_count: {quarantined_file_from_read_count} 🚫")
print(f"✔️ extracted_file_count: {extracted_file_count}")
print(
    f"📦 quarantined_file_from_extracted_count: {quarantined_file_from_extracted_count} 🚫"
)
