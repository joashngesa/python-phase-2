from datetime import datetime, date
import json
from pathlib import Path

from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import VALID_DIR
from src.config import INVALID_DIR
from src.config import DUPLICATES_DIR
from src.config import TRANSFORMED_DIR
from src.config import RUN_SUMMARY_DIR
from src.config import DEPOT_SUMMARY_DIR
from src.config import OUTPUT_DELIMITER

from src.config import VALID_COLUMNS
from src.config import INVALID_COLUMNS
from src.config import DUPLICATE_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import DEPOT_SUMMARY_COLUMNS
from src.config import FILE_METRICS_COLUMN
from src.config import PIPELINE_METRICS_COLUMN

from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_json
from src.extract import extract_batch_id
from src.extract import extract_depot
from src.convert import convert_data
from src.invalid import get_invalid
from src.valid import get_duplicates_valid
from src.transform import transform_data
from src.depot import get_depot_summary
from src.write import write_output
from src.result import build_success_metrics, build_failure_metrics
from src.metrics import pipeline_summary


def process_one_file(file_path):
    """
    the function processes one file at a time
    argument:
        -receives file_path from scan module
    returns:
        -file_result(both success & failed files in the pipeline)
    notes:
        - the outcome of this function will be used as the argument for process_all_files
    """

    file_path = Path(file_path)
    depot = "Uknown"
    batch_id = "Uknown"
    stage = "Initialization"

    try:
        stage = "reading"
        raw = read_file(file_path)

        stage = "extracting"
        extracted = extract_json(raw)
        batch_id = extract_batch_id(raw)
        depot = extract_depot(raw)

        stage = "enriching"
        generated_at = datetime.now()
        source_file = file_path.name

        for row in extracted:
            row["generated_at"] = generated_at
            row["source_file"] = source_file

        stage = "converting"
        converted = convert_data(extracted)

        stage = "validating"
        invalid, valid_raw = get_invalid(converted)

        stage = "detecting duplicates"
        duplicates, valid = get_duplicates_valid(valid_raw)

        for row in valid:
            row["depot"] = depot

        stage = "transforming"
        transformed = transform_data(valid)

        stage = "depot_summarizing"
        depot_summary = get_depot_summary(transformed)

        stage = "writing file outputs"
        file_stem = file_path.stem
        write_output(
            VALID_DIR / f"{file_stem}_valid.csv", valid, OUTPUT_DELIMITER, VALID_COLUMNS
        )

        write_output(
            INVALID_DIR / f"{file_stem}_invalid.csv",
            invalid,
            OUTPUT_DELIMITER,
            INVALID_COLUMNS,
        )

        write_output(
            DUPLICATES_DIR / f"{file_stem}_duplicate.csv",
            duplicates,
            OUTPUT_DELIMITER,
            DUPLICATE_COLUMNS,
        )

        write_output(
            TRANSFORMED_DIR / f"{file_stem}_transformed.csv",
            transformed,
            OUTPUT_DELIMITER,
            TRANSFORMED_COLUMNS,
        )

        write_output(
            DEPOT_SUMMARY_DIR / f"{file_stem}_summary.csv",
            depot_summary,
            OUTPUT_DELIMITER,
            DEPOT_SUMMARY_COLUMNS,
        )

        stage = "building file_results"
        file_result = build_success_metrics(
            file_name=file_path.name,
            depot=depot,
            batch_id=batch_id,
            raw_count=len(converted),
            valid_count=len(valid),
            invalid_count=len(invalid),
            duplicate_count=len(duplicates),
            transformed_count=len(transformed),
            depot_summary_count=len(depot_summary),
        )

        stage = "writing files output"
        write_output(
            RUN_SUMMARY_DIR / f"{file_stem}_filemetrics.csv",
            [file_result],
            OUTPUT_DELIMITER,
            FILE_METRICS_COLUMN,
        )

        return file_result

    except json.JSONDecodeError as error:
        status = "JSON parsing error"
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
        status = f"missing required key in {stage}"
        caught_error = error

    except ValueError as error:
        status = f"invalid value during {stage}"
        caught_error = error

    except Exception as error:
        status = f"unexpected error during {stage}"
        caught_error = error

    return build_failure_metrics(
        file_name=file_path.name,
        depot=depot,
        batch_id=batch_id,
        processing_status=status,
        error=caught_error,
    )


def process_all_files():
    """
    -> this function process all files starting from the scan module 🔎
    -> addresses all folder errors 📂
    -> expects file_results✅ and or batch_failure🚫 as output used in the execute module
    """
    file_results = []

    try:
        files = scan_folder(INPUT_DIR, FILE_PATTERN)

    except FileNotFoundError as error:
        batch_failure = build_failure_metrics(
            file_name="N/A",
            depot="Uknown",
            processing_status="input folder not found",
            error=error,
        )

        return [batch_failure]

    except PermissionError as error:
        batch_failure = build_failure_metrics(
            file_name="N/A",
            depot="Uknown",
            batch_id="Uknown",
            processing_status="input folder access denied",
            error=error,
        )
        return [batch_failure]

    except ValueError as error:
        batch_failure = build_failure_metrics(
            file_name="N/A",
            depot="Uknown",
            batch_id="Uknown",
            processing_status="no matching input files",
            error=error,
        )
        return [batch_failure]

    for file_path in files:
        file_result = process_one_file(file_path)
        file_results.append(file_result)

    write_output(
        RUN_SUMMARY_DIR / "all_files_summary.csv",
        file_results,
        OUTPUT_DELIMITER,
        FILE_METRICS_COLUMN,
    )

    return file_results
