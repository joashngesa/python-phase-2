def run_summary(file_result):
    """
    summarises the pipeline metrics of all the files that
    run through the pipeline
    """

    files_discovered = len(file_result)

    success_status = [
        "success",
        "completed_with_invalid_records",
        "completed_with_duplicates",
        "completed_with_invalids_and_duplicates",
    ]

    duplicates_status = [
        "completed_with_duplicates",
        "completed_with_invalids_and_duplicates",
    ]

    success_count = sum(
        1 for result in file_result if result["status"] in success_status
    )

    duplicates_count = sum(
        1 for result in file_result if result["status"] in duplicates_status
    )

    failure_count = sum(
        1 for result in file_result if result["status"] not in success_status
    )

    total_raw_count = sum(result["raw_count"] for result in file_result)
    total_valid_count = sum(result["valid_count"] for result in file_result)
    total_invalid_count = sum(result["invalid_count"] for result in file_result)
    total_duplicate_count = sum(result["duplicate_count"] for result in file_result)
    total_transformed_count = sum(result["transformed_count"] for result in file_result)

    if files_discovered == 0:
        batch_status = "no files found"

    if failure_count == 0:
        batch_status = "success"

    if success_count > 0 and failure_count > 0:
        batch_status = "completed with errors"

    if success_count > 0 and duplicates_count > 0:
        batch_status = "completed with duplicates"

    if success_count > 0 and failure_count > 0 and duplicates_count > 0:
        batch_status = "completed with errors and duplicates"

    else:
        batch_status = "failed"

    return {
        "batch_status": batch_status,
        "files_discovered": files_discovered,
        "files_succeeded": success_count,
        "files_with_duplicates": duplicates_count,
        "files_failed": failure_count,
        "total_raw_count": total_raw_count,
        "total_valid_count": total_valid_count,
        "total_invalid_count": total_invalid_count,
        "total_duplicate_count": total_duplicate_count,
        "total_transformed_count": total_transformed_count,
    }
