from tabulate import tabulate

from src.config import INPUT_PATH
from src.read import read_json_file
from src.extract import extract_data
from src.convert import convert_data
from src.valid_split import get_invalid
from src.valids import get_valids
from src.transform import transform_data
from src.suppliers_tbl import processed_data
from src.supplier import supplier_summary
from src.warehouse_tbl import warehouse
from src.warehouse import warehouse_summary

raw = read_json_file (INPUT_PATH)
print("raw json file\n")
print(raw)

data = extract_data (raw)
print("\n\nextracted table")
print("record number: ",len(data))
print(tabulate(data, headers="keys", tablefmt="grid"))

converted = convert_data (data)
print("\ntable after numeric conversion")
print(tabulate(converted, headers="keys", tablefmt="grid"))

invalids, valids_raw = get_invalid (converted)
print("\ninvalids table")
print(tabulate(invalids, headers="keys", tablefmt="grid"))
print("\nvalids raw table")
print(tabulate(valids_raw, headers="keys", tablefmt="grid"))

valids = get_valids (valids_raw)
print("\nvalid table")
print(tabulate(valids, headers="keys", tablefmt="grid"))

transformed = transform_data (valids)
print("\ntransformed table")
print(tabulate(transformed, headers="keys", tablefmt="grid"))

processed = processed_data(valids)
print("\nprocessed table for summary calculation")
print(tabulate(processed, headers="keys", tablefmt="grid"))

suppliers = supplier_summary(processed)
print("\nsupplier summary")
print(tabulate(suppliers,headers="keys", tablefmt="grid"))

w_house = warehouse(valids)
print("\nwarehouse table")
print(tabulate(w_house, headers="keys", tablefmt="grid"))

depo = warehouse_summary(w_house)
print("warehouse summary table")
print(tabulate(depo, headers="keys", tablefmt="grid"))