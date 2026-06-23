from tabulate import tabulate

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

# FIX: Added semantic string indicators to clearly signify unreached stages during errors
def metadata(total_files, file_path, status, valids=None, invalids=None, transformed=None, summary=None):
    return [
        {
            "Number of files discovered": total_files,
            "File name": file_path.name,
            "Processing status": status,
            "File valids count": len(valids) if valids is not None else "N/A (Failed Early)",
            "File invalids count": len(invalids) if invalids is not None else "N/A (Failed Early)",
            "File transformed count": len(transformed) if transformed is not None else "N/A (Failed Early)",
            "File summaries count": len(summary) if summary is not None else "N/A (Failed Early)"
        }
    ]

def execute_vendor_returns_directory_pipeline(input_directory, output_delimiter):

    try:
        files = scan_folder(input_directory, FILE_PATTERN)
    except (FileNotFoundError, NotADirectoryError) as path_error:
        raise RuntimeError(f"❌ Configuration error: {path_error}")
    except Exception as error:
        raise RuntimeError(f"❌ Unexpected scan failure: {error}")

    if not files:
        print(f"⚠️ Scan successful but 0 files matched pattern '{FILE_PATTERN}'")  
        return

    total_files = len(files)

    for file_path in files:
        # FIX: Keep tracking variables independent of the data structures to guarantee error-safety
        valids_data = None
        invalids_data = None
        transformed_data = None
        summary_data = None

        try:
            raw = read_file(file_path)
            converted = convert_data(raw)
            
            invalids_data, valids_raw = get_invalid(converted)
            valids_data = get_valids(valids_raw)
            
            transformed_data = transform_data(valids_data)
            summary_data = summarize_data(transformed_data)
                   
            valids_output, invalids_output, transformed_output, summary_output = create_output_paths(file_path)

            write_output(valids_output, valids_data, output_delimiter, VALIDS_COLUMNS)
            write_output(invalids_output, invalids_data, output_delimiter, INVALIDS_COLUMNS)
            write_output(transformed_output, transformed_data, output_delimiter, TRANSFORMED_COLUMNS)
            write_output(summary_output, summary_data, output_delimiter, SUMMARY_COLUMNS)

            # FIX: Dynamically update status label based on actual data health findings
            if len(invalids_data) > 0 and len(valids_data) == 0:
                final_status = "processed (all records invalid)"
            elif len(invalids_data) > 0:
                final_status = "processed (partial data warnings)"
            else:
                final_status = "processed"

            file_metadata = metadata(total_files, file_path, final_status, valids_data, invalids_data, transformed_data, summary_data) 
            print(tabulate(file_metadata, headers="keys", tablefmt="grid"))

        except Exception as error:
            # FIX: Pass the state variables directly. If it crashed on read_file, they will neatly output "N/A"
            failed_metadata = metadata(total_files, file_path, "failed", valids_data, invalids_data, transformed_data, summary_data)
            print(tabulate(failed_metadata, headers="keys", tablefmt="grid"))
            print(f"❌ The {file_path.name} pipeline execution failed: {error}\n")
            continue


if __name__ == "__main__":
    execute_vendor_returns_directory_pipeline(RAW_DIR, "|")
