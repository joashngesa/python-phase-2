import logging
from datetime import datetime, UTC
from pathlib import Path

logger = logging.getLogger(__name__)


def get_run_id() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"fleet_{timestamp}"


def get_exit_code(pipeline_status: str) -> int:

    exit_codes = {"SUCCESS": 0, "FAILED": 1, "PARTIAL_SUCCESS": 2}

    return exit_codes.get(pipeline_status, 1)
