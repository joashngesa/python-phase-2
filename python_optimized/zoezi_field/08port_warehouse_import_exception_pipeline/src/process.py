from datetime import datetime, date
import json

from src.config import INVALID_DIR
from src.config import VALID_DIR
from src.config import FILE_SUMMARY_DIR
from src.config import RUN_SUMMARY_DIR
from src.config import TRANSFORMED_DIR

from src.config import VALID_COLUMNS
from src.config import INVALID_COLUMNS
from src.config import DUPLICATES_COLUMNS
from src.config import TRANSFORMED_COLUMNS
from src.config import OUTPUT_DELIMITER
from src.config import FILE_METRICS_COLUMNS
from src.config import TBL_SUMMARY_COLUMNS

from src.scan import scan_folder
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


def process_one_file(file_path):
    """
    this function processes one file a time safely
    """
    port = "unknown"
    batch_id = "unknown"
    try:
        raw = read_file(file_path)
        extracted = extract_tables(raw)
        batch_id = extract_batch_id(raw)
        port = extract_port(raw)

        processed_at = datetime.now()
        for row in extracted:
            row["processed_at"] = processed_at
            row["source_file"] = file_path.name

        converted = convert_data(extracted)
        invalid, valid_raw = get_invalid_tbl(converted)
        duplicates, valid = get_duplicates_valid(valid_raw)
        transformed = transform_data(valid)
        tbl_summary = summarize_table(transformed)

        file_stem = file_path.stem

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

        file_result = build_success_score(
            file_name=file_path.name,
            port=port,
            batch_id=batch_id,
            raw_count=len(raw),
            valid_count=len(valid),
            invalid_count=len(invalid),
            duplicate_count=len(duplicates),
            transformed_count=len(transformed),
        )

        write_output(
            RUN_SUMMARY_DIR / f"{file_stem}_filemetrics.csv",
            [file_result],
            FILE_METRICS_COLUMNS,
            OUTPUT_DELIMITER,
        )

        return file_result

    except FileNotFoundError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "scanning folder failed", error
        )

    except NotADirectoryError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "absent folder", error
        )

    except json.JSONDecodeError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "parsing failed", error
        )

    except UnicodeDecodeError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "encoding_failed", error
        )

    except PermissionError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "writing failed", error
        )

    except ValueError as error:
        return build_failure_score(
            file_path.name, port, batch_id, "structure failed", error
        )

    except Exception as error:
        return build_failure_score(
            file_path.name, port, batch_id, "unexpected failure", error
        )
