
from tabulate import tabulate

from src.config import RAW_DIR
from src.config import FILE_PATTERN

from src.scan import scan_folder
from src.read import read_file
from src.convert import convert_data
from src.invalid import get_invalid
from src.valid import get_valids
from src.transform import transform_data
from src.summarize import summarize_data

files = scan_folder(RAW_DIR,FILE_PATTERN)
for file_name in files:
    print("row files from folders\n")
    print(file_name.stem)

for file_path in files:

    raw = read_file(file_path)
    print("file numbers: ",len(files) )
    print(f"\n{file_path.name} file from folder\n")
    print(tabulate(raw,headers="keys",tablefmt="grid"))

    converted = convert_data(raw)
    print(f"{file_path.name} converted file")
    print(tabulate(converted,headers="keys",tablefmt="grid"))

    invalids, valids_raw = get_invalid(converted)
    print(f"\n{file_path.name} invalid_data table")
    print(tabulate(invalids,headers="keys",tablefmt="grid"))
    print(f"\n{file_path.name} valids_raw table")
    print(tabulate(valids_raw, headers="keys", tablefmt="grid"))

    valids = get_valids(valids_raw)
    print(f"{file_path.name} valid table")
    print(tabulate(valids, headers="keys", tablefmt="grid"))

    transformed = transform_data(valids)
    print(f"{file_path.name} transformed table")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))

    vendors = summarize_data(transformed)
    print(f"{file_path.name} vendors table")
    print(tabulate(vendors, headers="keys", tablefmt="grid"))