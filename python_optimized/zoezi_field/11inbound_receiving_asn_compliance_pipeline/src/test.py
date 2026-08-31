from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR

import shutil
from tabulate import tabulate

from src.scan import scan_folder
from src.read import read_json_file
from src.convert import convert_data
from src.invalid_valid import get_invalid_valid
from src.duplicate import get_duplicates
from src.transform import transform_data
from src.supplier_summary import supplier_summary
from src.warehouse_summary import warehouse_synopsis

files = scan_folder(INPUT_DIR, FILE_PATTERN)
print("📁 Folder scanning initiated ...🔎")
print(f"🗂️ Files discovered: {len(files)}\n")

for count, file_path in enumerate(files, start=1):

    print(f"📥 {count}: File name: {file_path.name}")
    print(f"📬 File_paths: {file_path}\n")

file_read_count = 0
quarantined_file_from_read_count = 0
file_conversion_count = 0
invalids_files_count = 0

for index, raw_path in enumerate(files, start=1):
    try:
        raw = read_json_file(raw_path)
        # print(f"\n📁 {index}")
        # print(tabulate(raw, headers="keys", tablefmt="grid"))
        file_read_count += 1

    except (ValueError, TypeError, OSError) as error:
        print("\n❌ files that fail to read. 🚩")
        print(f"⛔ {index}: {raw_path.name} ⛔")
        print(f"\n🧰  {type(error).__name__}")
        print(f"\n🚩 {str(error)}\n")
        quarantine = QUARANTINE_DIR / raw_path.name
        shutil.move(raw_path, quarantine)
        quarantined_file_from_read_count += 1
        continue

    converted = convert_data(raw)
    # print(f"\n🗂️ {index}")
    # print(f"📜 converted {raw_path.name}")
    # print(tabulate(converted, headers="keys", tablefmt="grid"))
    file_conversion_count += 1

    invalid, valid = get_invalid_valid(converted)
    print(f"\n🗂️ {index}")
    print(f"📕 invalid {raw_path.name}")
    print(tabulate(invalid, headers="keys", tablefmt="grid"))

    duplicates = get_duplicates(valid)
    print(f"\n🗂️ {index}")
    print(f"📖 duplicate {raw_path.name}")
    print(tabulate(duplicates, headers="keys", tablefmt="grid"))

    transformed = transform_data(valid)
    print(f"\n🗂️ {index}")
    print(f"📊 transformed {raw_path.name}")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))

    supplier_sum = supplier_summary(transformed)
    print(f"\n🗂️ {index}")
    print(f"💹 supplier summary for the file {raw_path.name}")
    print(tabulate(supplier_sum, headers="keys", tablefmt="grid"))

    warehouse_digest = warehouse_synopsis(transformed)
    print(f"\n🗂️ {index}")
    print(f"🏗️ warehouse summary for {raw_path.name}")
    print(tabulate(warehouse_digest, headers="keys", tablefmt="grid"))

print(f"\n🔎 Files discovered: {len(files)}")
print(f"📥 files after read: {file_read_count}")
print(f"📦 files quarantined after read: {quarantined_file_from_read_count}")
print(f"📜 total files converted: {file_conversion_count}")
