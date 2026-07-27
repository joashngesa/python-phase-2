from src.config import RUN_SUMMARY_DIR
from src.config import OUTPUT_DELIMITER
from src.config import PIPELINE_METRICS_COLUMNS

from src.process import process_all_files
from src.metrics import run_summary
from src.write import write_output


def execute_warehouse_import_pipeline():

    print("Starting import exception pipeline ⏳")

    file_results = process_all_files()
    pipeline_summary = run_summary(file_results)

    write_output(
        RUN_SUMMARY_DIR / "run_summary.csv",
        [pipeline_summary],
        PIPELINE_METRICS_COLUMNS,
        OUTPUT_DELIMITER,
    )

    print("📊 Pipeline run summary")
    print(f"📥 Processed_files: {pipeline_summary["total_files"]}")
    print(f"✔️ Successful_files: {pipeline_summary["successful_files"]}")
    print(f"❌ Failed_files: {pipeline_summary["failed_files"]}")
    print(f"📜 Total_raw_records: {pipeline_summary["total_raw_records"]}")
    print(f"📑 Total_valid_records: {pipeline_summary["total_valid_records"]}")
    print(f"🚫 Total_invalid_records: {pipeline_summary["total_invalid_records"]}")
    print(f"📑🚫Total_duplicate_records: {pipeline_summary["total_duplicate_records"]}")
    print(
        f"💹 Total_transformed_records: {pipeline_summary["total_transformed_records"]}"
    )

    print("\n✅ Pipeline completed")

    return run_summary


if __name__ == "__main__":
    execute_warehouse_import_pipeline()
