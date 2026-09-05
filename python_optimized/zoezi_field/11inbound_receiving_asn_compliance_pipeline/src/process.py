from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import VALID_DIR
from src.config import VALID_COLUMNS
from src.config import INVALID_DIR
from src.config import INVALID_COLUMNS
from src.config import DUPLICATES_DIR
from src.config import DUPLICATES_COLUMNS
from src.config import TRANSFORMED_DIR
from src.config import TRANSFORMED_COLUMNS
from src.config import SUMMARIES_DIR
from src.config import SUPPLIER_DIGEST_COLUMNS
from src.config import WAREHOUSE_DIGEST_COLUMNS
from src.config import OUTPUT_DELIMITER
from src.config import RUN_SUMMARIES_DIR
from src.config import FILE_METRICS_COLUMN

from pathlib import Path
from time import perf_counter
import logging
import json

from src.read import read_json_file
from src.convert import convert_data
from src.invalid_valid import get_invalid_valid
from src.duplicate import get_duplicates
from src.transform import transform_data
from src.supplier_summary import supplier_summary
from src.warehouse_summary import warehouse_synopsis
from src.write import write_output
from src.result import build_success_file_metrics, build_failure_file_metrics
from src.scan import scan_folder

logger = logging.getLogger(__name__)


def manage_file_failure(
    run_id: str,
    file_path: Path,
    status: str,
    error: Exception,
    stage: str,
    file_start_time: float,
) -> dict:

    duration = perf_counter() - file_start_time

    file_result = build_failure_file_metrics(
        run_id=run_id,
        file_name=file_path.name,
        processing_status=status,
        error=error,
        duration=duration,
    )

    logger.exception(
        "File processing failed | run_id=%s | "
        "file=%s | stage=%s | status=%s | "
        "error=%s | duration_seconds=%.3f",
        run_id,
        file_path.name,
        stage,
        status,
        type(error).__name__,
        duration,
    )

    return file_result


def process_one_file(file_path: str | Path, run_id: str) -> dict:
    """
    -> ⌛ process one file at a time in the pipeline
    -> receives file_path from the scan module 🔎
    -> returns ✅success & ❌failure file metrics from the pipeline
    """

    record_path = Path(file_path)
    file_start_time = perf_counter()

    stage = "Initialization"

    logger.debug(
        "File processing initiated | run_id=%s | file=%s",
        run_id,
        record_path.name,
    )

    try:
        stage = "Reading"
        raw = read_json_file(record_path)

        stage = "Converting"
        converted = convert_data(raw)

        stage = "Validation"
        invalid, valid = get_invalid_valid(converted)

        stage = "Duplicate_detection"
        duplicates = get_duplicates(valid)

        stage = "Transformation"
        transformed = transform_data(valid)

        stage = "Supplier_summary"
        supplier_digest = supplier_summary(transformed)

        stage = "Warehouse_digest"
        warehouse_digest = warehouse_synopsis(transformed)

        stage = "Write_outputs"
        file_stem = record_path.stem
        write_output(
            invalid,
            INVALID_DIR / f"{file_stem}_invalid.csv",
            OUTPUT_DELIMITER,
            INVALID_COLUMNS,
        )

        write_output(
            valid, VALID_DIR / f"{file_stem}_valid.csv", OUTPUT_DELIMITER, VALID_COLUMNS
        )

        write_output(
            duplicates,
            DUPLICATES_DIR / f"{file_stem}_duplicates.csv",
            OUTPUT_DELIMITER,
            DUPLICATES_COLUMNS,
        )

        write_output(
            transformed,
            TRANSFORMED_DIR / f"{file_stem}_transformed.csv",
            OUTPUT_DELIMITER,
            TRANSFORMED_COLUMNS,
        )

        write_output(
            supplier_digest,
            SUMMARIES_DIR / f"{file_stem}_suppliers_digest.csv",
            OUTPUT_DELIMITER,
            SUPPLIER_DIGEST_COLUMNS,
        )

        write_output(
            warehouse_digest,
            SUMMARIES_DIR / f"{file_stem}_warehouse_digest.csv",
            OUTPUT_DELIMITER,
            WAREHOUSE_DIGEST_COLUMNS,
        )

        duration = perf_counter() - file_start_time
        stage = "File_metrics_build"
        file_result = build_success_file_metrics(
            run_id=run_id,
            file_name=record_path.name,
            raw_count=len(raw),
            valid_count=len(valid),
            invalid_count=len(invalid),
            duplicate_count=len(duplicates),
            transformed_count=len(transformed),
            supplier_digest_count=len(supplier_digest),
            warehouse_digest_count=len(warehouse_digest),
            duration=duration,
        )

        stage = "Write_file_metrics"
        write_output(
            [file_result],
            RUN_SUMMARIES_DIR / f"{file_stem}_metrics.csv",
            OUTPUT_DELIMITER,
            FILE_METRICS_COLUMN,
        )

        logger.info(
            "File processing completed | "
            "run_id=%s | file=%s | "
            "raw_count=%d | invalid_count=%d | "
            "valid_count=%d | duplicates=%d | transformed_count=%d | "
            "supplier_sum=%d | warehouse_sum_count=%d | "
            "duration_seconds=%.3f",
            run_id,
            record_path.name,
            file_result["raw_count"],
            file_result["invalid_count"],
            file_result["valid_count"],
            file_result["duplicate_count"],
            file_result["transformed_count"],
            file_result["supplier_digest_count"],
            file_result["warehouse_digest_count"],
            duration,
        )

        return file_result

    except ValueError as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status=f"Invalid value during {stage}",
            error=error,
            stage=stage,
            file_start_time=file_start_time,
        )

    except UnicodeDecodeError as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status="encoding failed",
            error=error,
            stage=stage,
            file_start_time=file_start_time,
        )

    except json.JSONDecodeError as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status="JSON parsing errors",
            error=error,
            stage=stage,
            file_start_time=file_start_time,
        )

    except PermissionError as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status=f"permission denied during {stage}",
            error=error,
            stage=stage,
            file_start_time=file_start_time,
        )

    except TypeError as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status=f"unexpected data type in {stage}",
            error=error,
            stage=stage,
            file_start_time=file_start_time,
        )

    except Exception as error:
        return manage_file_failure(
            run_id=run_id,
            file_path=record_path,
            status=f"unexpected error during {stage}",
            stage=stage,
            file_start_time=file_start_time,
        )


def process_all_files(run_id: str) -> dict:
    """
    -> function processes all files from scan module 🔎
    -> captures folder 📂 level errors🚩
    -> return of the function(file_results) will be used in the execute module
    """
    batch_start_time = perf_counter()
    file_results = []

    try:

        files = scan_folder(INPUT_DIR, FILE_PATTERN)
        logger.info(
            "Batch process initiated | run_id=%s | total_files=%d",
            run_id,
            len(files),
        )

    except PermissionError as error:
        return build_failure_file_metrics(
            run_id=run_id,
            file_name="N/A",
            processing_status="input folder access denied",
            error=error,
            duration=perf_counter() - batch_start_time,
        )

    except FileNotFoundError as error:
        return build_failure_file_metrics(
            run_id=run_id,
            file_name="N/A",
            processing_status="input directory not found",
            error=error,
            duration=perf_counter() - batch_start_time,
        )

    except NotADirectoryError as error:
        return build_failure_file_metrics(
            run_id=run_id,
            file_name="N/A",
            processing_status="input path has no directory",
            error=error,
            duration=perf_counter() - batch_start_time,
        )

    except ValueError as error:
        return build_failure_file_metrics(
            run_id=run_id,
            file_name="N/A",
            processing_status=f"no matching files from the {FILE_PATTERN} pattern",
            error=error,
            duration=perf_counter() - batch_start_time,
        )

    for record_path in files:

        file_result = process_one_file(record_path, run_id)
        file_results.append(file_result)

    batch_duration = perf_counter() - batch_start_time
    logger.info(
        "Batch process completed | run_id=%s | total_files=%d | batch_duration=%.3f",
        run_id,
        len(files),
        batch_duration,
    )

    write_output(
        file_results,
        RUN_SUMMARIES_DIR / "all_files_digest.csv",
        OUTPUT_DELIMITER,
        FILE_METRICS_COLUMN,
    )

    return file_results
