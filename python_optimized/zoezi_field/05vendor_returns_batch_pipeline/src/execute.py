

from tabulate import tabulate
from datetime import datetime

from src.config import RAW_DIR
from src.config import FILE_PATTERN
from src.config import VALIDS_DIR
from src.config import INVALIDS_DIR
from src.config import TRANSFORMED_DIR
from src.config import SUMMARY_DIR

from src.config import VALIDS_COLUMNS
from src.config import INVALIDS_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import SUMMARY_COLUMNS

from src.scan import scan_folder
from src.read import read_file
from src.convert import convert_data
from src.invalid import get_invalid
from src.valid import get_valids
from src.transform import transform_data
from src.summarize import summarize_data
from src.write import write_output

def create_output_paths(input_path):
    valids_output = VALIDS_DIR / f"{input_path.stem}_valids.csv"
    invalids_output = INVALIDS_DIR / f"{input_path.stem}_invalids.csv"
    transformed_output = TRANSFORMED_DIR / f"{input_path.stem}_transformed.csv"
    summary_output = SUMMARY_DIR / f"{input_path.stem}_summary.csv"

    return valids_output, invalids_output, transformed_output, summary_output

BATCH_SUMMARY_COLUMNS = [
            "Number of files discovered",
            "File name",
            "Processing status",
            "File valids count",
            "File invalids count",
            "File transformed count",
            "File summaries count",
            "error_message"
]


def execute_vendor_returns_directory_pipeline(input_directory,output_delimiter):

    print("Scanning raw documents...")
    print("Raw folder: ",input_directory)
    print("File pattern used: ",FILE_PATTERN)

    try:
        files = scan_folder(input_directory, FILE_PATTERN)
    except (FileNotFoundError, NotADirectoryError) as path_error:
        raise RuntimeError (f"❌Configuration error: {path_error}")
    except Exception as error:
        raise RuntimeError (f"❌Unexpected scan failure: {error}")

    if not files:
        print (f"⚠️ Scan successful but 0 files matched")  
        return

    total_files = len(files)
    print("Files discovered: ",total_files)

    batch_metadata = []
    all_valids = []
    all_invalids = []
    all_transformed = []
    all_summary = []

    for file_path in files:

        raw = []
        converted = []
        invalids = []
        valids_raw = []
        valids = []
        transformed = []
        summary = []

        try:
            raw = read_file(file_path)

            converted = convert_data(raw)
            invalids, valids_raw = get_invalid(converted)
            valids = get_valids(valids_raw)
            transformed = transform_data(valids)
            summary = summarize_data(transformed)

            metadata_row = {
            "Number of files discovered": total_files,
            "File name": file_path.name,
            "Processing status": "processed",
            "File valids count": len(valids),
            "File invalids count": len(invalids),
            "File transformed count": len(transformed),
            "File summaries count": len(summary),
            "error_message": ""
            }

            batch_metadata.append(metadata_row)
            print(tabulate([metadata_row], headers="keys", tablefmt="grid"))
            valids_output, invalids_output, transformed_output, summary_output = create_output_paths(file_path)

            write_output(valids_output,valids,output_delimiter,VALIDS_COLUMNS)
            write_output(invalids_output,invalids,output_delimiter,INVALIDS_COLUMNS)
            write_output(transformed_output,transformed,output_delimiter,TRANSFORMED_COLUMNS)
            write_output(summary_output,summary,output_delimiter,SUMMARY_COLUMNS)

            
            all_valids.extend(valids)
            all_invalids.extend(invalids)
            all_transformed.extend(transformed)
            all_summary.extend(summary)

        except Exception as error:
            metadata_row = {
            "Number of files discovered": total_files,
            "File name": file_path.name,
            "Processing status": "failed",
            "File valids count": len(valids),
            "File invalids count": len(invalids),
            "File transformed count": len(transformed),
            "File summaries count": len(summary),
            "error_message": str(error)
            }
            batch_metadata.append(metadata_row)
            print(tabulate([metadata_row], headers="keys", tablefmt="grid"))
            print(f"❌The {file_path} pipeline execution failed: {error}")
            continue
    
    write_output(
        VALIDS_DIR / "all_valids.csv",
        all_valids,
        output_delimiter,
        VALIDS_COLUMNS
    )

    write_output (
        INVALIDS_DIR / "all_invalids.csv",
        all_invalids,
        output_delimiter,
        INVALIDS_COLUMNS
    )

    write_output (
        TRANSFORMED_DIR / "all_transformed.csv",
        all_transformed,
        output_delimiter,
        TRANSFORMED_COLUMNS
    )

    write_output (
        SUMMARY_DIR / "all_summary.csv",
        all_summary,
        output_delimiter,
        SUMMARY_COLUMNS
    )

    write_output (
        SUMMARY_DIR / "batch_run_summary.csv",
        batch_metadata,
        output_delimiter,
        BATCH_SUMMARY_COLUMNS
    )

    print("\nBatch complete")

if __name__=="__main__":
     execute_vendor_returns_directory_pipeline(RAW_DIR,"|")
