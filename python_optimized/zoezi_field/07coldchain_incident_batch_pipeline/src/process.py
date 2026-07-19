from datetime import datetime, date
import json

from src.config import VALIDS_DIR
from src.config import INVALIDS_DIR
from src.config import TRANSFORMED_DIR
from src.config import SUMMARIES_DIR
from src.config import OUTPUT_DELIMITER
from src.config import OUTPUT_COLUMNS

from src.config import VALID_COLUMNS
from src.config import INVALID_COLUMNS
from src.config import TRANSFORMED_COLUMNS

from src.read import read_data
from src.extract import extract_data
from src.extract import extract_region
from src.extract import extract_batch
from src.convert import convert_data
from src.splitter import get_valid_invalids
from src.transform import transform_data
from src.write import write_output
from src.result import build_success_score, buid_failure_score
from src.summary import summarize_run


def process_one_file(file_path):
    """
    this function is designed to process one file at a time safely
    """

    try:
        raw = read_data(file_path)
        extracted = extract_data(raw)

        processed_at = datetime.now().isoformat(timespec="seconds")
        for data in extracted:
            data["processed_at"] = processed_at
            data["source_file"] = file_path.name

        converted = convert_data(extracted)
        invalid, valid = get_valid_invalids(converted)
        transformed = transform_data(valid)

        file_stem = file_path.stem

        write_output(
            VALIDS_DIR / f"{file_stem}_valids.csv",
            valid,
            OUTPUT_DELIMITER,
            VALID_COLUMNS,
        )
        write_output(
            INVALIDS_DIR / f"{file_stem}_invalid.csv",
            invalid,
            OUTPUT_DELIMITER,
            INVALID_COLUMNS,
        )
        write_output(
            TRANSFORMED_DIR / f"{file_stem}_transformed.csv",
            transformed,
            OUTPUT_DELIMITER,
            TRANSFORMED_COLUMNS,
        )

        file_result = build_success_score(
            file_name=file_path.name,
            raw_count=len(raw),
            invalids_count=len(invalid),
            valids_count=len(valid),
            transformed_count=len(transformed),
        )

        write_output(
            SUMMARIES_DIR / f"{file_stem}_fileresult.csv",
            [file_result],
            OUTPUT_DELIMITER,
            OUTPUT_COLUMNS,
        )

        return file_result

    except FileNotFoundError as error:
        return buid_failure_score(file_path.name, "read_failed", error)
    except json.JSONDecodeError as error:
        return buid_failure_score(file_path.name, "parse_failed", error)
    except UnicodeDecodeError as error:
        return buid_failure_score(file_path.name, "encoding_failed", error)
    except PermissionError as error:
        return buid_failure_score(file_path.name, "writing permission_failed", error)
    except ValueError as error:
        return buid_failure_score(file_path.name, "structure_failed", error)
    except Exception as error:
        return buid_failure_score(file_path.name, "unexpected_failure", error)
