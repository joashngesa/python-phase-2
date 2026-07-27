def pipeline_summary(file_results):
    """
    this function summarizes all the pipleine metrics
    for the pipeline
    arg:
        file_results(aggregated file_results)
    """

    total_files = len(file_results)

    success_status = [
        "completed with invalid records",
        "completed with valid records",
        "completed with ivalid & duplicates",
        "completed with no valid record;failed business logic",
        "success",
    ]
    successful_files = sum(
        1 for result in file_results if result["processing_status"] in success_status
    )
    failed_files = total_files - successful_files

    total_raw_records = sum(result.get("raw_count", 0) for result in file_results)
    total_valid_records = sum(result.get("valid_count", 0) for result in file_results)
    total_invalid_records = sum(
        result.get("invalid_count", 0) for result in file_results
    )
    total_duplicate_records = sum(
        result.get("duplicate_count", 0) for result in file_results
    )
    total_transformed_records = sum(
        result.get("transformed_count", 0) for result in file_results
    )
    total_depot_summary_count = sum(
        result.get("depot_summary_count") for result in file_results
    )

    return {
        "total_files": total_files,
        "successful_files": successful_files,
        "failed_files": failed_files,
        "total_raw_records": total_raw_records,
        "total_valid_records": total_valid_records,
        "total_invalid_records": total_invalid_records,
        "total_duplicate_records": total_duplicate_records,
        "total_transformed_records": total_transformed_records,
        "total_depot_summary_count": total_depot_summary_count,
    }
