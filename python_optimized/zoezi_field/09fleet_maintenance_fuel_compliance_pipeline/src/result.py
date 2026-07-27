"""
Expected output:
    file_name
    depot
    batch_id
    processing_status
    raw_record_count
    valid_record_count
    invalid_record_count
    duplicate_record_count
    transformed_record_count
    summary_row_count
    error_type
    error_message
"""


def build_success_metrics(
    file_name,
    depot,
    batch_id,
    raw_count,
    valid_count,
    invalid_count,
    duplicate_count,
    transformed_count,
    depot_summary_count,
):
    """
    this function is used to summarize the score of successfully processed files ⏳
    """

    if invalid_count > 0:
        processing_status = "completed with invalid records"

    elif duplicate_count > 0:
        processing_status = "completed with valid records"

    elif invalid_count > 0 and duplicate_count > 0:
        processing_status = "completed with ivalid & duplicates"

    elif raw_count > 0 and valid_count == 0:
        processing_status = "completed with no valid record;failed business logic"

    elif invalid_count == 0:
        processing_status = "success"

    return {
        "file_name": file_name,
        "depot": depot,
        "batch_id": batch_id,
        "processing_status": processing_status,
        "raw_count": raw_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "duplicate_count": duplicate_count,
        "transformed_count": transformed_count,
        "depot_summary_count": depot_summary_count,
        "error_type": None,
        "error_message": None,
    }


def build_failure_metrics(file_name, depot, batch_id, processing_status, error):
    """
    this function is used to summarize the score of failed processed files 🧰
    """

    return {
        "file_name": file_name,
        "depot": depot,
        "batch_id": batch_id,
        "processing_status": processing_status,
        "raw_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "duplicate_count": 0,
        "transformed_count": 0,
        "depot_summary_count": 0,
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
