def build_success_file_metrics(
    run_id: str,
    file_name: str,
    raw_count: int,
    valid_count: int,
    invalid_count: int,
    duplicate_count: int,
    transformed_count: int,
    supplier_digest_count: int,
    warehouse_digest_count: int,
    duration: float,
) -> dict:
    """
    ✅ This modules processes metrics of successfully processd files ⌛
    """

    if invalid_count > 0 and duplicate_count > 0:
        processing_status = "completed with invalid & duplicates"

    elif invalid_count > 0:
        processing_status = "completed with invalids"

    elif duplicate_count > 0:
        processing_status = "completed with duplicates"

    elif raw_count > 0 and valid_count == 0:
        processing_status = "completed with no valid"

    elif invalid_count == 0:
        processing_status = "success"

    return {
        "run_id": run_id,
        "file_name": file_name,
        "status": processing_status,
        "raw_count": raw_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "duplicate_count": duplicate_count,
        "transformed_count": transformed_count,
        "supplier_digest_count": supplier_digest_count,
        "warehouse_digest_count": warehouse_digest_count,
        "error_type": None,
        "error_message": None,
        "duration": duration,
    }


def build_failure_file_metrics(
    run_id: str,
    file_name: str,
    processing_status: str,
    error: Exception,
    duration: float,
):
    """
    ⛔ This function summarizes the metrics of failed files in the pipeline 🚫
    """

    return {
        "run_id": run_id,
        "file_name": file_name,
        "status": processing_status,
        "raw_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "duplicate_count": 0,
        "transformed_count": 0,
        "supplier_digest_count": 0,
        "warehouse_digest_count": 0,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "duration": duration,
    }
