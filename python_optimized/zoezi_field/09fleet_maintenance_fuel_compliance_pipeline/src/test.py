"""
This module is designed to test the modules during the making of the pipeline
"""

from tabulate import tabulate
from datetime import datetime, date
from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR
import shutil

from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_json
from src.extract import extract_batch_id
from src.extract import extract_depot
from src.convert import convert_data
from src.invalid import get_invalid
from src.valid import get_duplicates_valid
from src.transform import transform_data
from src.depot import get_depot_summary

records = scan_folder(INPUT_DIR, FILE_PATTERN)
"""
for file_path in records:
    print("\n📁 Folder scanning ...🔎\n")
    print(f"📂 total files discovered: {len(records)}")
    print(f"\n📥 File_name: {file_path.name}")
"""

read_file_count = 0
quarantined_files_from_read_count = 0
extracted_file_count = 0
quarantined_files_from_extraction_count = 0


for file_path in records:
    try:
        raw = read_file(file_path)
        print(f"\n📜 extracted file: {file_path.name}")
        print(file_path)
        read_file_count += 1

    except ValueError as error:
        print(f"\n⛔ File did not read succesfully: {file_path.name}")
        print(f"\n🚩 {file_path.name} error: {error} 🚫")
        quarantine = QUARANTINE_DIR / file_path.name
        shutil.move(file_path, quarantine)
        quarantined_files_from_read_count += 1
        continue

    try:
        extracted = extract_json(raw)
        batch_id = extract_batch_id(raw)
        depot = extract_depot(raw)
        print(f"\n📖 extracted file name: {file_path.name}")
        print(f"🏗️ depot: {depot}")
        print(f"🪪 batch_id: {batch_id}\n")
        print(tabulate(extracted, headers="keys", tablefmt="grid"))
        extracted_file_count += 1

    except ValueError as error:
        print(f"\n⚠️ file did not extract json: {file_path.name}")
        print(f"❌ {file_path.name} error: {error}")
        quarantine = QUARANTINE_DIR / file_path.name
        shutil.move(file_path, quarantine)
        quarantined_files_from_extraction_count += 1
        continue

    source_file = file_path.name
    generated_at = datetime.now()
    for data in extracted:
        data["generated_at"] = generated_at
        data["source_file"] = source_file

    converted = convert_data(extracted)
    print(f"\n🗒️ Converted {file_path.name}")
    print(tabulate(converted, headers="keys", tablefmt="grid"))

    invalid, valid_raw = get_invalid(converted)
    print(f"\n📕 invalid table; {file_path.name}")
    print(tabulate(invalid, headers="keys", tablefmt="grid"))
    print(f"🪦 valid_raw: {file_path.name}")
    print(tabulate(valid_raw, headers="keys", tablefmt="grid"))

    duplicates, valid = get_duplicates_valid(valid_raw)
    print(f"\n⚠️ Duplicate {file_path.name}")
    print(tabulate(duplicates, headers="keys", tablefmt="grid"))
    print(f"📑 valid {file_path.name}")
    print(tabulate(valid, headers="keys", tablefmt="grid"))

    for table in valid:
        table["depot"] = depot

    try:
        transformed = transform_data(valid)
        print(f"💹 tranformed {file_path.name}")
        print(tabulate(transformed, headers="keys", tablefmt="grid"))
    except ValueError as error:
        print(f"\n🚫 failed transformation: {file_path.name}")
        print(f"{file_path.name} failed due to {error}")

    depot = get_depot_summary(transformed)
    print(f"🏚️ depot {file_path.name}")
    print(tabulate(depot, headers="keys", tablefmt="grid"))


print(f"\n📂 total files discovered: {len(records)}")
print(f"✔️ read file count: {read_file_count}")
print(f"✔️ extracted file count: {extracted_file_count}")
print(f"📦 quarantined files from read count : {quarantined_files_from_read_count}")
print(
    f"📦 quarantined files from extraction count : {quarantined_files_from_extraction_count}"
)
