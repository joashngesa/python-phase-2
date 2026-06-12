from tabulate import tabulate

from src.config import INPUT_PATH
from src.config import VALIDS_PATH
from src.config import INVALIDS_PATH
from src.config import TRANSFORMED_PATH
from src.config import SUPPLIERS_PATH
from src.config import DEPO_PATH

from src.config import OUTPUT_DELIMITER

from src.config import VALIDS_COLUMNS
from src.config import INVALIDS_COLUMN
from src.config import TRANSFORMED_COLUMN
from src.config import SUPPLIERS_COLUMN 
from src.config import DEPO_COLUMN

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
from src.write import write_output

def execute_purchase_orders_pipeline(file_path):

    raw = read_json_file(file_path)
    data = extract_data(raw)
    converted = convert_data(data)
    invalids, valids_raw = get_invalid(converted)
    valids = get_valids(valids_raw)
    transformed = transform_data(valids)
    processed = processed_data(valids)
    suppliers = supplier_summary(processed)
    w_house = warehouse(valids)
    depo = warehouse_summary(w_house)

    write_output(VALIDS_PATH,valids,OUTPUT_DELIMITER,VALIDS_COLUMNS)
    write_output(INVALIDS_PATH,invalids,OUTPUT_DELIMITER,INVALIDS_COLUMN)
    write_output(TRANSFORMED_PATH,transformed,OUTPUT_DELIMITER,TRANSFORMED_COLUMN)
    write_output(SUPPLIERS_PATH,suppliers,OUTPUT_DELIMITER,SUPPLIERS_COLUMN)
    write_output(DEPO_PATH,depo,OUTPUT_DELIMITER,DEPO_COLUMN)

    print("Purchase order pipeline run successfully")
    print("Total row records: ",len(data))
    print("Total invalid records: ",len(invalids))
    print("Total valid records: ",len(valids))

if __name__=="__main__":
    execute_purchase_orders_pipeline(INPUT_PATH)