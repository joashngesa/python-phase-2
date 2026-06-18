from tabulate import tabulate

from src.config import INPUT_PATH
from src.read import read_json_files
from src.extract import extract_data
from src.convert import convert_data
from src.valid_split import get_invalids
from src.valids import get_valids
from src.transform import transform_data
from src.vendor_raw import vendor_table
from src.vendor import vendor_summary
from src.reasons import reasons_summary
from src.extract import extract_metadata

raw = read_json_files(INPUT_PATH)
print("raw file")
print(raw)

data = extract_data(raw)
print("\nRaw extracted file")
print("Total raw records: \n",len(data))
print(tabulate(data, headers="keys", tablefmt="grid"))

metadata = extract_metadata(raw)
print("metadata table")

converted = convert_data(data)
print("\nConverted data")
print(tabulate(converted, headers="keys", tablefmt="grid"))

invalids, raw_valids = get_invalids(converted)
print("\ninvalid data")
print("invalids record count: \n",len(invalids))
print(tabulate(invalids, headers="keys", tablefmt="grid"))

valids = get_valids(raw_valids)
print("\nvalid record count",len(valids))
print("valid data")
print(tabulate(valids, headers="keys", tablefmt="grid"))

transformed = transform_data(valids)
print("\ntransformed data")
print(tabulate(transformed, headers="keys", tablefmt="grid"))

vendor_tbl = vendor_table(valids)
print("\nvendor table")
print(tabulate(vendor_tbl, headers="keys",tablefmt="grid"))

vendors = vendor_summary(vendor_tbl)
print("\nvendor summary")
print(tabulate(vendors,headers="keys",tablefmt="grid"))

return_sum = reasons_summary(valids)
print("\nreaasons summary")
print("reasons summary record rows: ",len(return_sum))
print(tabulate(return_sum, headers="keys", tablefmt="grid"))