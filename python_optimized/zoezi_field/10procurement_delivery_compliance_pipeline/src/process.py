import json
import logging
from pathlib import Path
from time import perf_counter
from datetime import datetime, time

from src.scan import scan_folder
from src.read import read_file
from src.extract import extract_table, extract_batch_id, extract_depot
from src.convert import convert_data
from src.invalid import get_invalid_valid_raw
from src.valid import get_valid_duplicate
from src.transform import transform_data
from src.summary import summarize_table
from src.write import write_output
from src.result import build_success_metrics, build_failure_metrics

from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import OUTPUT_DELIMITER
from src.config import VALID_COLUMNS
from src.config import INVALID_COLUMNS
from src.config import DUPLICATES_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import SUMMARY_COLUMNS
from src.config import VALID_DIR
from src.config import INVALID_DIR
from src.config import DUPLICATES_DIR
from src.config import TRANSFORMED_DIR
from src.config import SUMMARY_DIR
from src.config import RUN_SUMMARY_DIR
from src.config import FILE_METRICS_COLUMNS

logger = logging.getLogger(__name__)


def handle_file_failure(
    run_id,
    file_path: Path,
    batch_id: str,
    depot: str,
    processing_status: str,
    stage: str,
    error: Exception,
    file_start_time: float,
) -> dict:

    duration = perf_counter() - file_start_time

    file_result = build_failure_metrics(
        file_name=file_path.name,
        batch_id=batch_id,
        depot=depot,
        processing_status=processing_status,
        run_id=run_id,
        error=error,
    )

    logger.exception(
        "File processing failed | run_id=%s | file=%s |"
        " stage=%s | status=%s | error=%s | duration_seconds=%.3f",
        run_id,
        file_path.name,
        stage,
        processing_status,
        type(error).__name__,
        duration,
    )

    return file_result


def process_one_file(record_path: str | Path, run_id: str) -> dict:
    """
    -> ⏳ Process one file at a time in the pipeline 📜
    -> Recieves file path from scan module 🔎
    -> Returns success & failed files in the pipeline
    -> The outcome of this file will be used in the process_all_files function
    """
    file_path = Path(record_path)
    file_start_time = perf_counter()
    depot = "Unknown"
    batch_id = "Unknown"
    stage = "Initialization"

    logger.debug(
        "File processing initiated | run_id=%s | file=%s", run_id, file_path.name
    )

    try:
        stage = "read"
        raw = read_file(file_path)

        stage = "extract"
        extracted = extract_table(raw)
        batch_id = extract_batch_id(raw)
        depot = extract_depot(raw)

        stage = "enrich"
        source_file = file_path.name
        processed_at = datetime.now()
        for table in extracted:
            table["processed_at"] = processed_at
            table["source_file"] = source_file

        stage = "convert"
        converted = convert_data(extracted)

        stage = "validate"
        invalid, valid_raw = get_invalid_valid_raw(converted)

        stage = "deduplicate"
        valid, duplicates = get_valid_duplicate(valid_raw)

        stage = "transform"
        transformed = transform_data(valid)

        stage = "summarize"
        summary = summarize_table(transformed)

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
            DUPLICATES_DIR / f"{file_stem}_duplicates.csv",
            duplicates,
            OUTPUT_DELIMITER,
            DUPLICATES_COLUMNS,
        )

        write_output(
            TRANSFORMED_DIR / f"{file_stem}_transformed.csv",
            transformed,
            OUTPUT_DELIMITER,
            TRANSFORMED_COLUMNS,
        )

        write_output(
            SUMMARY_DIR / f"{file_stem}_summary.csv",
            summary,
            OUTPUT_DELIMITER,
            SUMMARY_COLUMNS,
        )

        duration = perf_counter() - file_start_time
        stage = "build_file_metrics"
        file_result = build_success_metrics(
            run_id=run_id,
            file_name=file_path.name,
            batch_id=batch_id,
            depot=depot,
            raw_count=len(converted),
            valid_count=len(valid),
            invalid_count=len(invalid),
            duplicate_count=len(duplicates),
            transformed_count=len(transformed),
            summary_count=len(summary),
        )

        stage = "write_file_metrics"
        write_output(
            RUN_SUMMARY_DIR / f"{file_stem}_metrics.csv",
            [file_result],
            OUTPUT_DELIMITER,
            FILE_METRICS_COLUMNS,
        )

        logger.info(
            "File processing completed | "
            "run_id=%s | file=%s "
            "raw=%d | valid=%d | "
            "invalid=%d | duplicates=%d | "
            "transformed=%d | summary=%d | "
            "depot=%s | duration_seconds=%.3f",
            run_id,
            file_path.name,
            file_result["raw_count"],
            file_result["valid_count"],
            file_result["invalid_count"],
            file_result["duplicate_count"],
            file_result["transformed_count"],
            file_result["summary_count"],
            depot,
            duration,
        )

        return file_result

    except json.JSONDecodeError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status="JSON parsing errors",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except UnicodeDecodeError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status="encoding failed",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except PermissionError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status=f"permission denied during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except KeyError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status=f"missing required key in {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except ValueError as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status=f"invalid value during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )

    except Exception as error:
        return handle_file_failure(
            run_id=run_id,
            file_path=file_path,
            batch_id=batch_id,
            depot=depot,
            processing_status=f"unexpected error during {stage}",
            stage=stage,
            error=error,
            file_start_time=file_start_time,
        )


def process_all_files(run_id: str):
    """
    -> processes all files files from the scan module 🔎
    -> captures all folder errors 📁
    -> output: file_results ✅ & batch_failures ⛔
    -> passed down to the execute module
    """

    file_results = []

    try:
        files = scan_folder(INPUT_DIR, FILE_PATTERN)
        logger.info(
            "Batch processing initiated | run_id=%s | total_files=%d",
            run_id,
            len(files),
        )

    except FileNotFoundError as error:
        batch_error = build_failure_metrics(
            run_id=run_id,
            file_name="N/A",
            batch_id="unknown",
            depot="unknown",
            processing_status="input folder not found",
            error=error,
        )

        return [batch_error]

    except NotADirectoryError as error:
        batch_error = build_failure_metrics(
            run_id=run_id,
            file_name="N/A",
            batch_id="unknown",
            depot="unknown",
            processing_status="input_path is not a directory",
            error=error,
        )

        return [batch_error]

    except PermissionError as error:
        batch_error = build_failure_metrics(
            run_id=run_id,
            file_name="N/A",
            batch_id="unknown",
            depot="unknown",
            processing_status="input folder access denied",
            error=error,
        )

        return [batch_error]

    except ValueError as error:
        batch_error = build_failure_metrics(
            run_id=run_id,
            file_name="N/A",
            batch_id="unknown",
            depot="unknown",
            processing_status="no matching input files from file_pattern",
            error=error,
        )

        return [batch_error]

    for record in files:

        file_result = process_one_file(record, run_id)
        file_results.append(file_result)

    logger.info(
        "Batch process complete | run_id=%s | total_files=%d",
        run_id,
        len(files),
    )

    write_output(
        RUN_SUMMARY_DIR / "all_files_summary.csv",
        file_results,
        OUTPUT_DELIMITER,
        FILE_METRICS_COLUMNS,
    )

    return file_results
