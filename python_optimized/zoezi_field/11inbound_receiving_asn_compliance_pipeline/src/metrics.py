def pipeline_summary(file_results: list[dict], run_id: str) -> dict:
    """
        This function summarizes the metrics of all the files passed through
    in the pipeline
    """

    total_files = len(file_results)

    success_status = [
        "completed with invalid & duplicates",
        "completed with invalids",
        "completed with duplicates",
        "completed with no valid",
        "success",
    ]

    successful_files = sum(
        1 for result in file_results if result["status"] in success_status
    )
    failed_files = total_files - successful_files

    if total_files == 0:
        pipeline_status = "FAILED"

    elif successful_files == total_files:
        pipeline_status = "SUCCESS"

    elif successful_files > 0:
        pipeline_status = "PARTIAL SUCCESS"

    else:
        pipeline_status = "FAILED"

    tot_raw = sum(result.get("raw_count", 0) for result in file_results)
    tot_valids = sum(result.get("valid_count", 0) for result in file_results)
    tot_invalids = sum(result.get("invalid_count", 0) for result in file_results)
    tot_duplicates = sum(result.get("duplicate_count", 0) for result in file_results)
    tot_transformed = sum(result.get("transformed_count", 0) for result in file_results)
    tot_suppliers = sum(
        result.get("supplier_digest_count", 0) for result in file_results
    )
    tot_warehouse = sum(
        result.get("warehouse_digest_count", 0) for result in file_results
    )

    return {
        "run_id": run_id,
        "total_files": total_files,
        "successful_files": successful_files,
        "failed_files": failed_files,
        "pipeline_status": pipeline_status,
        "total_raw_records": tot_raw,
        "total_valid_records": tot_valids,
        "total_invalid_records": tot_invalids,
        "total_duplicates_records": tot_duplicates,
        "total_transformed_records": tot_transformed,
        "total_suppliers_count": tot_suppliers,
        "total_warehouse_count": tot_warehouse,
    }
