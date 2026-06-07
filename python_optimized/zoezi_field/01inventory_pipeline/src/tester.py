import os
from tabulate import tabulate

from src.config import INPUT_PATH
from src.reader import read_data
from src.converter import convert_data
from src.validity_splitter import get_valids_invalids
from src.valids import get_valids
from src.transformed import transform_data

raw = read_data(INPUT_PATH)
print("raw data parsed from source")
print(tabulate(raw, headers="keys", tablefmt="grid"))

converted = convert_data(raw)
print   ("converted data")
print(tabulate(converted, headers="keys", tablefmt="grid"))

invalids, valids_raw = get_valids_invalids(converted)
print("invalids table")
print(tabulate(invalids, headers="keys", tablefmt="grid"))
print("\nvalids_raw table")
print(tabulate(valids_raw, headers="keys", tablefmt="grid"))

valids = get_valids (valids_raw)
print("\nvalids table")
print(tabulate(valids, headers="keys", tablefmt="grid"))

transformed = transform_data(valids)
print("\ntransformed table")
print(tabulate(transformed, headers="keys", tablefmt="grid"))