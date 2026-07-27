from src.config import RUN_SUMMARY_DIR
from src.config import OUTPUT_DELIMITER
from src.config import PIPELINE_METRICS_COLUMN

from src.process import process_all_files
from src.metrics import pipeline_summary
from src.write import write_output


def execute_fleet_maintenance_compliance_pipeline():

    print("\n🚛 Starting fleet maintenance fuel compliance pipeline ⏳")

    file_results = process_all_files()
    pipeline_metrics = pipeline_summary(file_results)

    write_output(
        RUN_SUMMARY_DIR / "run_summary.csv",
        [pipeline_metrics],
        OUTPUT_DELIMITER,
        PIPELINE_METRICS_COLUMN,
    )

    print("Pipeline run summary")
    print(f"\n📥 Processed_files: {pipeline_metrics['total_files']}")
    print(f"✔️ Successful_files: {pipeline_metrics['successful_files']}")
    print(f"❌ Failed_files: {pipeline_metrics['failed_files']}")
    print(f"📜 Total_raw_records: {pipeline_metrics['total_raw_records']}")
    print(f"📄 Total_valid_records: {pipeline_metrics['total_valid_records']}")
    print(f"⚠️ Total_invalid_records: {pipeline_metrics['total_invalid_records']}")
    print(f"‼️ Total_duplicate_records: {pipeline_metrics['total_duplicate_records']}")
    print(
        f"📑 Total_transformed_records: {pipeline_metrics['total_transformed_records']}"
    )
    print(
        f"💹 total_depot_summary_count: {pipeline_metrics['total_depot_summary_count']}"
    )

    print("\n✅Pipeline completed")

    return pipeline_metrics


if __name__ == "__main__":
    execute_fleet_maintenance_compliance_pipeline()
