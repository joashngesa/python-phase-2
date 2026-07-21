def run_summary(file_results):
    """
    summarises the pipeline metrics of all the files that
    run through the pipeline
    arg:
        - uses file_results(aggregated file_result)
    """
    total_files = len(file_results)

    success_status = [
        "completed with invalid records",
        "completed with duplicates",
        "completed with invalid & duplicates",
        "success",
    ]

    successful_files = sum(
        1
        for result in file_results
        if result.get("processing_status") in success_status
    )

    failed_files = total_files - successful_files

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

    return {
        "total_files": total_files,
        "successful_files": successful_files,
        "failed_files": failed_files,
        "total_raw_records": total_raw_records,
        "total_valid_records": total_valid_records,
        "total_invalid_records": total_invalid_records,
        "total_duplicate_records": total_duplicates_records,
        "total_transformed_records": total_transformed_records,
    }
