import os
import csv
from tabulate import tabulate

from src.config import INPUT_PATH
from src.reader import read_data
from src.converter import convert_data
from src.validity_splitter import get_valids_invalids
from src.valids import get_valids
from src.transformed import transform_data
from src.reporter import print_output

def execute_warehouse_pipeline(file_path):

    raw = read_data(file_path)
    converted = convert_data(raw)
    invalids, valids_raw = get_valids_invalids(converted)
    valids = get_valids(valids_raw)
    transformed = transform_data(valids)

    print_output(valids,invalids,transformed)


if __name__=="__main__":

    execute_warehouse_pipeline(INPUT_PATH)