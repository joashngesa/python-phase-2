from tabulate import tabulate

from src.config import INPUT_PATH
from src.reader import read_json_file
from src.convert import convert_data

raw = read_json_file(INPUT_PATH)
print("raw file")
print(tabulate(raw, headers="keys", tablefmt="grid"))

converted = convert_data(raw)
print("\nconverted data")
print(tabulate(converted, headers="keys", tablefmt="grid"))