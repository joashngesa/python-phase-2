import logging
import json
from pathlib import Path
from datetime import datetime, date
from time import perf_counter

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

logger = logging.getLogger(__name__)


def handle_file_failure(
    run_id,
    file_path: Path,
    depot: str,
    batch_id: str,
    processing_status: str,
    stage: str,
    error: Exception,
    file_start_time: float,
) -> dict:

    duration = perf_counter - file_start_time

    file_result = build_failure_metrics(
        file_name=file_path.name,
        depot=depot,
        batch_id=batch_id,
        processing_status=processing_status,
        error=error,
    )

    logger.exception(
        "File processing failed | run_id=%s | file_name=%s | stage=%s | status=%s | error_type=%s | duration_seconds=%.3f",
        run_id,
        file_path.name,
        stage,
        processing_status,
        type(error).__name__,
        duration,
    )

    return file_result


def process_one_file(file_path: str | Path, run_id: str) -> dict:
    """
    the function processes one file at a time
    argument:
        -receives file_path from scan module
    returns:
        -file_result(both success & failed files in the pipeline)
    notes:
        - the outcome of this function will be used as the argument for process_all_files
    """

    file_start_time = perf_counter()
    file_path = Path(file_path)
    depot = "Unknown"
    batch_id = "Unknown"
    stage = "Initialization"

    logger.debug(
        "File processing started | run_id=%s | file_name=%s",
        run_id,
        file_path.name,
    )

    try:
        stage = "read"
        raw = read_file(file_path)

        stage = "extract"
        extracted = extract_json(raw)
        batch_id = extract_batch_id(raw)
        depot = extract_depot(raw)

        stage = "enrich"
        generated_at = datetime.now()
        source_file = file_path.name

        for row in extracted:
            row["generated_at"] = generated_at
            row["source_file"] = source_file

        stage = "convert"
        converted = convert_data(extracted)

        stage = "validate"
        invalid, valid_raw = get_invalid(converted)

        stage = "deduplicate"
        duplicates, valid = get_duplicates_valid(valid_raw)

        for row in valid:
            row["depot"] = depot

        stage = "transform"
        transformed = transform_data(valid)

        stage = "summarize"
        depot_summary = get_depot_summary(transformed)

        stage = "write_outputs"
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

        stage = "build_file_metrics"
        file_result = build_success_metrics(
            run_id=run_id,
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

        stage = "write_file_metrics"
        write_output(
            RUN_SUMMARY_DIR / f"{file_stem}_filemetrics.csv",
            [file_result],
            OUTPUT_DELIMITER,
            FILE_METRICS_COLUMN,
        )

        duration = perf_counter() - file_start_time
        logger.info(
            "File processing completed | "
            "run_id=%s |  file_name=%s | "
            "raw=%d | valid=%d | invalid=%d | "
            "duplicate=%d | transformed=%d | depot=%d | duration_seconds=%.3f",
            run_id,
            file_path.name,
            file_result["raw_count"],
            file_result["valid_count"],
            file_result["invalid_count"],
            file_result["duplicate_count"],
            file_result["transformed_count"],
            file_result["depot_summary_count"],
            duration,
        )

        return file_result

    except json.JSONDecodeError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status="JSON parsing error",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except UnicodeDecodeError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status="encoding failed",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except FileNotFoundError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status=f"file not found during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except PermissionError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status=f"permission denied during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except KeyError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status=f"missing required key in {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except ValueError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status=f"invalid value during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except Exception as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path.name,
            depot=depot,
            batch_id=batch_id,
            processing_status=f"unexpected error during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )


def process_all_files(run_id):
    """
    -> this function process all files starting from the scan module 🔎
    -> addresses all folder errors 📂
    -> expects file_results✅ and or batch_failure🚫 as output used in the execute module
    """
    file_results = []

    try:
        files = scan_folder(INPUT_DIR, FILE_PATTERN)
        logger.info(
            "Batch processing started | run_id=%s | total_files=%d",
            run_id,
            len(files),
        )

    except FileNotFoundError as error:
        batch_failure = build_failure_metrics(
            file_name="N/A",
            depot="Uknown",
            batch_id="Uknown",
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

    for position, file_path in enumerate(files, start=1):
        logger.info(
            "Batch progress run | run_id=%s | total_files=%d | position=%d | file_name=%s",
            run_id,
            len(files),
            position,
            file_path.name,
        )
        file_result = process_one_file(file_path, run_id)
        file_results.append(file_result)

    logger.info(
        "Batch process complete | run_id=%s | total_files=%d", run_id, len(files)
    )

    write_output(
        RUN_SUMMARY_DIR / "all_files_summary.csv",
        file_results,
        OUTPUT_DELIMITER,
        FILE_METRICS_COLUMN,
    )

    return file_results
