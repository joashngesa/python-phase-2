def summarize_run(file_result):
    """
    this module runs the summary metrics of execution process
    of all aggregated files in the pipeline
    """

    files_discovered = len(file_result)

    success_status = ["success", "completed with invalid records"]

    success_count = sum(
        1 for result in file_result if result["status"] in success_status
    )
    failure_count = sum(
        1 for result in file_result if result["status"] not in success_status
    )

    total_raw_count = sum(result["raw_count"] for result in file_result)
    total_valid_count = sum(result["valid_count"] for result in file_result)
    total_invalid_count = sum(result["invalid_count"] for result in file_result)
    total_transformed_count = sum(result["transformed_count"] for result in file_result)

    if files_discovered == 0:
        batch_status = "no files found"
    if failure_count == 0:
        batch_status = "success"
    if success_count > 0 and failure_count > 0:
        batch_status = "completed with errors"
    else:
        batch_status = "failed"

    return {
        "batch_status": batch_status,
        "files_discovered": files_discovered,
        "files_succeeded": success_count,
        "files_failed": failure_count,
        "total_raw_count": total_raw_count,
        "total_valid_count": total_valid_count,
        "total_invalid_count": total_invalid_count,
        "total_transformed_count": total_transformed_count,
    }
