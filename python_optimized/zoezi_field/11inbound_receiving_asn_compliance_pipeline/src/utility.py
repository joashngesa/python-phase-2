from datetime import datetime, UTC


def get_run_id() -> str:

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    return f"inbound_{timestamp}"
