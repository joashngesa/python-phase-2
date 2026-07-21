from datetime import datetime
import json
from pathlib import Path

from src.config import INVALID_DIR
from src.config import VALID_DIR
from src.config import FILE_SUMMARY_DIR
from src.config import RUN_SUMMARY_DIR
from src.config import TRANSFORMED_DIR
from src.config import INPUT_DIR
from src.config import FILE_PATTERN

from src.config import VALID_COLUMNS
from src.config import INVALID_COLUMNS
from src.config import DUPLICATES_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import OUTPUT_DELIMITER
from src.config import FILE_METRICS_COLUMNS
from src.config import TBL_SUMMARY_COLUMNS

from src.read import read_file
from src.extract import extract_tables
from src.extract import extract_batch_id
from src.extract import extract_port
from src.convert import convert_data
from src.invalid import get_invalid_tbl
from src.valid import get_duplicates_valid
from src.transform import transform_data
from src.summary import summarize_table
from src.result import build_success_score, build_failure_score
from src.write import write_output
from src.scan import scan_folder


def process_one_file(file_path):
    """
    this function processes one file a time safely
    argument:
        -recieves file_path from scan.py module
    returns:
        -file_result(both success and failure score has the same design of output)
    notes:
        -after processing each file, it passes the return to process_all_files
    """

    file_path = Path(file_path)
    port = "unknown"
    batch_id = "unknown"
    stage = "initialization"

    try:
        stage = "reading"
        raw = read_file(file_path)

        stage = "extacting"
        extracted = extract_tables(raw)
        batch_id = extract_batch_id(raw)
        port = extract_port(raw)

        stage = "enriching"
        processed_at = datetime.now()
        for row in extracted:
            row["processed_at"] = processed_at
            row["source_file"] = file_path.name

        stage = "converting"
        converted = convert_data(extracted)

        stage = "validating"
        invalid, valid_raw = get_invalid_tbl(converted)

        stage = "detecting duplicates"
        duplicates, valid = get_duplicates_valid(valid_raw)

        stage = "transforming"
        transformed = transform_data(valid)

        stage = "summarizing"
        tbl_summary = summarize_table(transformed)

        file_stem = file_path.stem

        stage = "writing file outputs"
        write_output(
            VALID_DIR / f"{file_stem}_valid.csv", valid, VALID_COLUMNS, OUTPUT_DELIMITER
        )

        write_output(
            INVALID_DIR / f"{file_stem}_invalid.csv",
            invalid,
            INVALID_COLUMNS,
            OUTPUT_DELIMITER,
        )

        write_output(
            INVALID_DIR / f"{file_stem}_duplicates.csv",
            duplicates,
            DUPLICATES_COLUMNS,
            OUTPUT_DELIMITER,
        )

        write_output(
            TRANSFORMED_DIR / f"{file_stem}_transformed.csv",
            transformed,
            TRANSFORMED_COLUMNS,
            OUTPUT_DELIMITER,
        )

        write_output(
            FILE_SUMMARY_DIR / f"{file_stem}_summary.csv",
            tbl_summary,
            TBL_SUMMARY_COLUMNS,
            OUTPUT_DELIMITER,
        )

        stage = "building file_result"
        file_result = build_success_score(
            file_name=file_path.name,
            port=port,
            batch_id=batch_id,
            raw_count=len(converted),
            valid_count=len(valid),
            invalid_count=len(invalid),
            duplicate_count=len(duplicates),
            transformed_count=len(transformed),
        )

        stage = "writing file metrics"
        write_output(
            RUN_SUMMARY_DIR / f"{file_stem}_filemetrics.csv",
            [file_result],
            FILE_METRICS_COLUMNS,
            OUTPUT_DELIMITER,
        )

        return file_result

    except json.JSONDecodeError as error:
        status = "JSON parsing failed"
        caught_error = error

    except UnicodeDecodeError as error:
        status = "encoding failed"
        caught_error = error

    except FileNotFoundError as error:
        status = f"file not found during {stage}"
        caught_error = error

    except PermissionError as error:
        status = f"permission denied during {stage}"
        caught_error = error

    except KeyError as error:
        status = f"missing required key during {stage}"
        caught_error = error

    except TypeError as error:
        status = f"invalid structure during {stage}"
        caught_error = error

    except ValueError as error:
        status = f"invalid value during {stage}"
        caught_error = error

    except Exception as error:
        status = f"unexpected failure during {stage}"
        caught_error = error

    return build_failure_score(
        file_name=file_path.name,
        port=port,
        batch_id=batch_id,
        processing_status=status,
        error=caught_error,
    )


def process_all_files():
    """
    This function process all files starting from the scan module.
    it addresses all the folder level errors
    the expected output is file_results which is going to be used in the execute module
    """

    file_results = []

    try:
        files = scan_folder(INPUT_DIR, FILE_PATTERN)

    except FileNotFoundError as error:
        batch_failure = build_failure_score(
            file_name="N/A",
            port="unknown",
            batch_id="unknown",
            processing_status="input folder not found",
            error=error,
        )

        return [batch_failure]

    except NotADirectoryError as error:
        batch_failure = build_failure_score(
            file_name="N/A",
            port="unknown",
            batch_id="unknown",
            processing_status="input folder not a directory",
            error=error,
        )

        return [batch_failure]

    except PermissionError as error:
        batch_failure = build_failure_score(
            file_name="N/A",
            port="uknown",
            batch_id="unknown",
            processing_status="input folder access denied",
            error=error,
        )

        return [batch_failure]

    except ValueError as error:
        batch_failure = build_failure_score(
            file_name="N/A",
            port="unknown",
            batch_id="unkown",
            processing_status="no matching input files",
            error=error,
        )

        return [batch_failure]

    for file_path in files:

        file_result = process_one_file(file_path)
        file_results.append(file_result)

    write_output(
        RUN_SUMMARY_DIR / "all_files_metrics.csv",
        file_results,
        FILE_METRICS_COLUMNS,
        OUTPUT_DELIMITER,
    )

    return file_results
