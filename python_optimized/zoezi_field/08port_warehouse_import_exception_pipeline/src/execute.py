from src.config import INPUT_DIR
from src.config import FILE_PATTERN
from src.config import RUN_SUMMARY_DIR
from src.config import OUTPUT_DELIMITER
from src.config import FILE_METRICS_COLUMNS
from src.config import PIPELINE_METRICS_COLUMNS

from src.scan import scan_folder
from src.process import process_one_file
from src.metrics import run_summary
from src.write import write_output


def execute_warehouse_import_pipeline():

    file_results = []

    print("📂 Scanning input folder ....")
    files = scan_folder(INPUT_DIR, FILE_PATTERN)

    print(f"📥 Files discovered: {len(files)}\n")

    for record in files:
        result = process_one_file(record)
        file_results.append(result)

        print(f"🔎 Processing: {record.name}")
        print(f"🪧 Status: {result["status"]}")

    pipeline_summary = run_summary(file_results)

    write_output(
        RUN_SUMMARY_DIR / "file_results.csv",
        file_results,
        FILE_METRICS_COLUMNS,
        OUTPUT_DELIMITER,
    )

    write_output(
        RUN_SUMMARY_DIR / "pipeline_summary.csv",
        [pipeline_summary],
        PIPELINE_METRICS_COLUMNS,
        OUTPUT_DELIMITER,
    )

    print("✅ Batch complete")
    print(f"📊 Batch_status: {pipeline_summary["batch_status"]}")
    print(f"⌛ Files_discovered: {pipeline_summary["files_succeeded"]}")
    print(f"❌ Files failed: {pipeline_summary["files_failed"]}")


if __name__ == "__main__":
    execute_warehouse_import_pipeline()
