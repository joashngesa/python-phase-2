# output
# file_name
# port
# batch_id
# status
# raw_count
# valid_count
# invalid_count
# duplicate_count
# transformed_count
# error_type
# error_message

# status output:
# success
# completed_with_invalid_records
# completed_with_duplicates
# completed_with_invalids_and_duplicates


def build_success_score(
    file_name,
    port,
    batch_id,
    raw_count,
    valid_count,
    invalid_count,
    duplicate_count,
    transformed_count,
):
    """
    🚦the function is used to summarize the metrics of succesfully processed⏳ files
    """

    if invalid_count > 0:
        status = "completed with invalid records"

    elif duplicate_count > 0:
        status = "completed with duplicates"

    elif invalid_count > 0 and duplicate_count > 0:
        status = "completed with invalids & duplicates"

    else:
        status = "sucess"

    return {
        "file_name": file_name,
        "port": port,
        "batch_id": batch_id,
        "status": status,
        "raw_count": raw_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "duplicate_count": duplicate_count,
        "transformed_count": transformed_count,
        "error_type": None,
        "error_message": None,
    }


def build_failure_score(
    file_name,
    port,
    batch_id,
    status,
    error,
):
    """
    ❌the function is used to summarize the metrics of files that failed the process⌛
    """

    return {
        "file_name": file_name,
        "port": port,
        "batch_id": batch_id,
        "status": status,
        "raw_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "duplicate_count": 0,
        "transformed_count": 0,
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
