

def build_success_score (file_name, raw_count, invalids_count, valids_count, transformed_count):

    if invalids_count > 0:
        status = "completed with invalid records"
    else:
        status = "success"

    return {
        "file_name": file_name,
        "status": status,
        "raw_count": raw_count,
        "valid_count": valids_count,
        "invalid_count": invalids_count,
        "transformed_count": transformed_count,
        "error_type": None,
        "error_message": None
    }



def buid_failure_score (file_name, status, error):

    return {
        "file_name": file_name,
        "status": status,
        "raw_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "transformed_count": 0,
        "error_type": type(error).__name__,
        "error_message": str(error)
    }