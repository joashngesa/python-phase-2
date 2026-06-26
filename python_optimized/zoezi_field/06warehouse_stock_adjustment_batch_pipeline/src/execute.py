
from tabulate import tabulate
from datetime import datetime

from src.config import RAW_DIR
from src.config import FILE_PATTERN

from src.config import INVALIDS_DIR
from src.config import VALIDS_DIR
from src.config import TRANSFORMED_DIR
from src.config import SUMMARY_DIR
from src.config import ARCHIVE_DIR


from src.config import REQUIRED_FIELDS
from src.config import VALIDS_COLUMN
from src.config import INVALIDS_COLUMN
from src.config import TRANSFORMED_COLUMN
from src.config import SUMMARY_COLUMNS

from src.scan import scan_data
from src.read import read_data
from src.convert import convert_data
from src.splitter import get_invalids_valids
from src.transform import transform_data
from src.summary import warehouse_summary
from src.write import write_output

def create_output_paths (input):
    valids_output = VALIDS_DIR / f"{input.stem}_valids.csv"
    invalids_output = INVALIDS_DIR / f"{input.stem}_invalids.csv"
    transformed_output = TRANSFORMED_DIR / f"{input.stem}_transformed.csv"
    summary_output = SUMMARY_DIR / f"{input.stem}_summary.csv"
    archive_output = ARCHIVE_DIR / f"{input.stem}_archive.csv"

    return valids_output, invalids_output, transformed_output, summary_output, archive_output

BATCH_SUMMARY_COLUMNS = [
    "number of files discovered",
    "file_name",
    "processing status",
    "file valid count",
    "file invalid count",
    "file transformed count",
    "file summaries count",
    "error message"
]

def stock_adjustment_pipeline(RAW_DIRECTORY, output_delimiter):

    print("Scanning raw documents ...")
    print(f"Raw directory path: {RAW_DIRECTORY}")

    try:
        files = scan_data (RAW_DIR, FILE_PATTERN)
    except (FileNotFoundError, NotADirectoryError) as path_error:
        raise RuntimeError (f"❌ Configuration error: {path_error} 🚨")
    except Exception as error:
        raise RuntimeError (f"🚫 Unexpected error: {error} 🚨")
    
    if not files:
        print("⚠️ Scan successfull but 0 files matched in the folder ❓❓")

    files_found = len (files)
    print(f"Number of files found: {files_found}")

    pipeline_metadata = []
    all_valids = []
    all_invalids = []
    all_transformed = []
    all_summaries = []

    for record in files:

        print("\nFiles discovered:")
        print(record)

        raw = []
        converted = []
        invalids = []
        valids = []
        transformed = []
        summary = []

        try:
            raw = read_data (record)

            processed_at = datetime.now().isoformat (timespec="seconds")
            for field in raw:
                field["source_file"] = record.name
                field["processed_at"] = processed_at

            converted = convert_data(raw)
            invalids, valids = get_invalids_valids (converted)
            transformed = transform_data (valids)
            summary = warehouse_summary (transformed)

            metadata_row = {
                "number of files discovered": files_found,
                "file_name": record.name,
                "processing status":"processed",
                "file valid count": len(valids),
                "file invalid count": len(invalids),
                "file transformed count": len(transformed),
                "file summary count": len(summary),
                "error_message": ""
            }

            pipeline_metadata.append(metadata_row)
            print(tabulate([metadata_row], headers="keys", tablefmt="grid"))

            valids_output, invalids_output, transformed_output, summary_output, archive_output = create_output_paths(record)

            write_output (valids_output, valids, output_delimiter, VALIDS_COLUMN)
            write_output (invalids_output, invalids, output_delimiter, INVALIDS_COLUMN)
            write_output (transformed_output, transformed, output_delimiter, TRANSFORMED_COLUMN)
            write_output (summary_output, summary, output_delimiter, SUMMARY_COLUMNS)
            write_output (archive_output, raw, output_delimiter, REQUIRED_FIELDS)

            all_valids.extend (valids)
            all_invalids.extend (invalids)
            all_transformed.extend (transformed)
            all_summaries.extend (summary)

        except Exception as error:
            metadata_row = {
                "number of files discovered": files_found,
                "file_name": record.name,
                "processing status":"failed",
                "file valid count": len(valids),
                "file invalid count": len(invalids),
                "file transformed count": len(transformed),
                "file summary count": len(summary),
                "error_message": str(error)
            }

            pipeline_metadata.append(metadata_row)
            print(tabulate([metadata_row], headers="keys", tablefmt="grid"))
            print(f"🚩 Pipeline execution failed: {error} 🚩")

            continue

    write_output (
        VALIDS_DIR / "all_valids.csv",
        all_valids,
        output_delimiter,
        VALIDS_COLUMN
        )

    write_output (
        INVALIDS_DIR / "all_invalids.csv",
        all_invalids,
        output_delimiter,
        INVALIDS_COLUMN
    )

    write_output (
        TRANSFORMED_DIR / "all_transformed.csv",
        all_transformed,
        output_delimiter,
        TRANSFORMED_COLUMN
    )

    write_output (
        SUMMARY_DIR / "all_summary.csv",
        all_summaries,
        output_delimiter,
        SUMMARY_COLUMNS
    )

    print("\n✅Pipeline complete.💯🔚")

if __name__=="__main__":
    stock_adjustment_pipeline(RAW_DIR, "|")