
#This module is designmed for specifically testing the pippeline during coding,
#once the pipeline is up and running, the test module will be dormant

from datetime import datetime, date
from tabulate import tabulate
import json
import shutil

from src.config import RAW_DIR
from src.config import FILE_PATTERN
from src.config import QUARANTINE_DIR

from src.scan import scan_input_folder
from src.read import read_data
from src.extract import extract_data
from src.extract import extract_region
from src.extract import extract_batch
from src.convert import convert_data
from src.splitter import get_valids_invalids
from src.transform import transform_data

files = scan_input_folder (RAW_DIR,FILE_PATTERN)
print("\nFiles discovered: \n",len(files))

files_region = {
"north_file": RAW_DIR / "cold_chain_incidents_region_north_2026_06_24.json",
"south_file": RAW_DIR / "cold_chain_incidents_region_south_2026_06_24.json",
"west_file": RAW_DIR / "cold_chain_incidents_region_west_2026_06_24.json"
}

for region, path in files_region.items():

    print(f"\nTesting {path.name}\n")

    try:
        raw = read_data (path)
        print(f"✅ Success raw data {path.name}\n")
        print (raw)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"❓ {path.name} has  error ⛔")
        print(f"⚠️ Reading error: {error} ❌")
        qntn_destination = QUARANTINE_DIR / path.name
        shutil.move (str(path), str(qntn_destination))
        print(f"\n📦 Isolated corrupted source to {qntn_destination}")
        continue

    batch_id = extract_batch (raw)
    region = extract_region (raw)
    extracted = extract_data (raw)
    print(f"\nbatch_id: {batch_id}")
    print(f"Region: {region}")
    print(f"\nExtraction success for {path.name}")
    print(tabulate(extracted, headers="keys", tablefmt="grid"))

    processed_at = datetime.now().isoformat(timespec="seconds")
    for file in extracted:
        file["processed_at"] = processed_at
        file["source_file"] = path.name

    converted = convert_data (extracted)
    print(f"\nConvert {path.name}")
    print(tabulate(converted, headers="keys", tablefmt="grid"))

    invalids, valids = get_valids_invalids (converted)
    print(f"\ninvalid {path.name}")
    print(tabulate(invalids, headers="keys", tablefmt="grid"))
    print(f"\nvalids {path.name}")
    print(tabulate(valids, headers="keys", tablefmt="grid"))

    transformed = transform_data(valids)
    print(f"\ntransformed_{path.name}")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))