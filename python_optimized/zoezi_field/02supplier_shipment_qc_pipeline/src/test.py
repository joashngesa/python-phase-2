from tabulate import tabulate

from src.config import INPUT_PATH
from src.reader import read_json_file
from src.convert import convert_data
from src.validity_splitter import split_table
from src.transform import transform_data
from src.summarizer import report

raw = read_json_file(INPUT_PATH)
print("raw file")
print(tabulate(raw, headers="keys", tablefmt="grid"))

converted = convert_data(raw)
print("\nconverted data")
print(tabulate(converted, headers="keys", tablefmt="grid"))

invalids, valids = split_table(converted)
print("\ninvalid table")
print(tabulate(invalids, headers="keys", tablefmt="grid"))
print("\nvalid table")
print(tabulate(valids, headers="keys", tablefmt="grid"))

transformed = transform_data(valids)
print("\ntransformed data")
print(tabulate(transformed, headers="keys", tablefmt="grid"))

summary = report (transformed)
print("\nsummary")
print(tabulate(summary, headers="keys", tablefmt="grid"))