def build_success_metrics(
    run_id: str,
    file_name: str,
    batch_id: str,
    depot: str,
    raw_count: int,
    valid_count: int,
    invalid_count: int,
    duplicate_count: int,
    transformed_count: int,
    summary_count: int,
) -> dict:
    """
    This function is used to summarize the metrics of successfully processed files ⌛
    """

    if invalid_count > 0 and duplicate_count > 0:
        processing_status = "completed with invalid & duplicates"

    elif invalid_count > 0:
        processing_status = "completed with invalid records"

    elif duplicate_count > 0:
        processing_status = "completed with duplicate records"

    elif raw_count > 0 and valid_count == 0:
        processing_status = "completed with no valid records"

    elif invalid_count == 0:
        processing_status = "success"

    return {
        "run_id": run_id,
        "file_name": file_name,
        "batch_id": batch_id,
        "depot": depot,
        "processing_status": processing_status,
        "raw_count": raw_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "duplicate_count": duplicate_count,
        "transformed_count": transformed_count,
        "summary_count": summary_count,
        "error_type": None,
        "error_message": None,
    }


def build_failure_metrics(
    file_name: str,
    batch_id: str,
    depot: str,
    processing_status: str,
    error: Exception,
    run_id: str = None,
):
    """
    this function summarizes the metrics of failed files in the pipeline 🧰
    """

    return {
        "run_id": run_id,
        "file_name": file_name,
        "batch_id": batch_id,
        "depot": depot,
        "processing_status": processing_status,
        "raw_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "duplicate_count": 0,
        "transformed_count": 0,
        "summary_count": 0,
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
