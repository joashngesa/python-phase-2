
from src.config import INPUT_PATH

from src.config import INVALIDS_PATH
from src.config import VALIDS_PATH
from src.config import TRANSFORMED_PATH
from src.config import SUMMARY_PATH

from src.reader import read_json_file
from src.extract import extract_data
from src.convert import convert_data
from src.validity_splitter import split_table
from src.transform import transform_data
from src.summarizer import report 
from src.write import write_output

invalids_column = ["shipment_id", "supplier_id", "supplier_name", "carrier",
                   "origin_country", "destination_country", "shipment_date",
                   "delivery_status", "units", "unit_cost", "error_reason"]
valids_column = ["shipment_id", "supplier_id", "supplier_name", "carrier",
                   "origin_country", "destination_country", "shipment_date",
                   "delivery_status", "units", "unit_cost"]
transformed_column = ["shipment_id", "carrier", "units", "unit_cost",
                      "shipment_value", "route", "risk_level"]
summary_column = ["carrier", "shipment_count", "total_units", "total_shipment_value", "avg_shipment_value"]

def execute_shipment_qc_pipeline(file_path, output_delimiter):

    raw = read_json_file (file_path)
    data = extract_data(raw)
    converted = convert_data (data)
    invalids, valids = split_table (converted)
    transformed = transform_data (valids)
    summary = report (transformed)

    write_output (INVALIDS_PATH, invalids, output_delimiter, invalids_column)
    write_output (VALIDS_PATH, valids, output_delimiter, valids_column)
    write_output (TRANSFORMED_PATH, transformed, output_delimiter, transformed_column)
    write_output (SUMMARY_PATH, summary, output_delimiter, summary_column)

    print("json shipment pipeline executed successfully")
    print(f"Total records: {len(raw)}")
    print(f"Total invalid records: {len(invalids)}")
    print(f"Total valid records: {len(valids)}")

if __name__=="__main__":

    execute_shipment_qc_pipeline(INPUT_PATH,"|")
