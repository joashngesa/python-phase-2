def pipeline_summary(file_results: list[dict], run_id: str) -> dict:
    """
    This function summarizes all metrics of the files in the pipeline
    """

    total_files = len(file_results)

    success_status = [
        "completed with invalid & duplicates",
        "completed with invalid records",
        "completed with duplicate records",
        "success",
    ]

    succesfull_files = sum(
        1 for result in file_results if result["processing_status"] in success_status
    )
    failed_files = total_files - succesfull_files

    if total_files == 0:
        pipeline_status = "FAILED"

    elif succesfull_files == total_files:
        pipeline_status = "SUCCESS"

    elif succesfull_files > 0:
        pipeline_status = "PARTIAL_SUCCESS"

    else:
        pipeline_status = "FAILED"

    total_raw_records = sum(result.get("raw_count", 0) for result in file_results)
    total_valid_records = sum(result.get("valid_count", 0) for result in file_results)
    total_invalid_records = sum(
        result.get("invalid_count", 0) for result in file_results
    )
    total_duplicates_records = sum(
        result.get("duplicate_count", 0) for result in file_results
    )
    total_transformed_records = sum(
        result.get("transformed_count", 0) for result in file_results
    )
    total_summary_count = sum(result.get("summary_count", 0) for result in file_results)

    return {
        "run_id": run_id,
        "total_files": total_files,
        "succesful_files": succesfull_files,
        "failed_files": failed_files,
        "pipeline_status": pipeline_status,
        "total_raw_records": total_raw_records,
        "total_valid_records": total_valid_records,
        "total_invalid_records": total_invalid_records,
        "total_duplicates_records": total_duplicates_records,
        "total_transformed_records": total_transformed_records,
        "total_summary_count": total_summary_count,
    }
