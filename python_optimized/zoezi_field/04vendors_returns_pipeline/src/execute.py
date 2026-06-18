
from src.config import INPUT_PATH

from src.config import INVALIDS_PATH
from src.config import VALIDS_PATH
from src.config import TRANSFORMED_PATH
from src.config import VENDORS_PATH
from src.config import OUTPUT_SUMMARY_PATH

from src.config import INVALIDS_COLUMNS
from src.config import VALIDS_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import VENDORS_COLUMNS
from src.config import OUTPUT_SUMMARY_COLUMNS

from src.read import read_json_files
from src.extract import extract_data
from src.extract import extract_metadata
from src.convert import convert_data
from src.valid_split import get_invalids
from src.valids import get_valids
from src.transform import transform_data
from src.vendor_raw import vendor_table
from src.vendor import vendor_summary
from src.write import write_output
from src.run_summary import output_metadata
from src.reasons import reasons_summary

def execute_vendors_returns_pipeline (file_path,output_delimiter):

    raw = read_json_files(file_path)
    data = extract_data(raw)
    metadata = extract_metadata(raw)
    converted = convert_data(data)
    invalids, raw_valids = get_invalids(converted)
    valids = get_valids(raw_valids)
    transformed = transform_data(valids)
    vendor_tbl = vendor_table(valids)
    vendors = vendor_summary(vendor_tbl)
    reasons_sum = reasons_summary(valids)

    output_summary = output_metadata(metadata = metadata,
                                     extracted_record_count=len(data),
                                     valids_record_count=len(valids),
                                     invalids_record_count=len(invalids),
                                     transformed_record_count=len(transformed),
                                     vendors_record_count=len(vendors),
                                     reasons_record_count=len(reasons_sum),
                                     )

    write_output(INVALIDS_PATH,invalids,output_delimiter,INVALIDS_COLUMNS)
    write_output(VALIDS_PATH,valids,output_delimiter,VALIDS_COLUMNS)
    write_output(TRANSFORMED_PATH,transformed,output_delimiter,TRANSFORMED_COLUMNS)
    write_output(VENDORS_PATH,vendors,output_delimiter,VENDORS_COLUMNS)
    write_output(OUTPUT_SUMMARY_PATH,output_summary,output_delimiter,OUTPUT_SUMMARY_COLUMNS)

    print("vendors returns pipeline executed successfully")
    print("source: vendor_returns_api")
    print("Batch: RET-BATCH-20260614-001")
    print("total raw records: ",len(raw))
    print("valid records: ",len(valids))
    print("invalids records: ", len(invalids))
    print("vendor summary rows: ",len(vendors))
 

if __name__=="__main__":
    execute_vendors_returns_pipeline(INPUT_PATH,"|")

