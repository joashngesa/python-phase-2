from src.config import RAW_DIR
from src.config import SUMMARIES_DIR
from src.config import RUN_SUMMARY_COLUMNS
from src.config import OUTPUT_COLUMNS
from src.config import OUTPUT_DELIMITER
from src.config import FILE_PATTERN

from src.scan import scan_input_folder
from src.process import process_one_file
from src.summary import summarize_run
from src.write import write_output


def execute_incident_batch_pipeline():

    file_result = []

    files = scan_input_folder(RAW_DIR, FILE_PATTERN)

    for path in files:
        result = process_one_file(path)
        file_result.append(result)

    execution_summary = summarize_run(file_result)

    write_output(
        SUMMARIES_DIR / "file_results.csv",
        file_result,
        OUTPUT_DELIMITER,
        OUTPUT_COLUMNS,
    )
    write_output(
        SUMMARIES_DIR / "run_summary.csv",
        [execution_summary],
        OUTPUT_DELIMITER,
        RUN_SUMMARY_COLUMNS,
    )

    print("batch_status: ", execution_summary["batch_status"])
    print("files_discovered: ", execution_summary["files_discovered"])
    print("files_succeeded: ", execution_summary["files_succeeded"])
    print("files_failed: ", execution_summary["files_failed"])


if __name__ == "__main__":
    execute_incident_batch_pipeline()
