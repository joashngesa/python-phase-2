import logging
import sys

from src.config import PIPELINE_NAME
from src.config import RUN_SUMMARY_DIR
from src.config import PIPELINE_METRICS_COLUMN
from src.config import OUTPUT_DELIMITER
from src.config import LOG_FILE

from src.process import process_all_files
from src.metrics import pipeline_summary
from src.write import write_output
from src.log_config import logging_configuration
from src.utility import get_run_id

logger = logging.getLogger(__name__)


def execute_procurement_delivery_compliance_pipeline(run_id: str):

    logging.info(
        "Pipeline processing initiated | pipeline_name | run_id",
        PIPELINE_NAME,
        run_id,
    )

    file_results = process_all_files(run_id)
    pipeline_metrics = pipeline_summary(file_results)

    write_output(
        RUN_SUMMARY_DIR / "run_summary.csv",
        [pipeline_metrics],
        OUTPUT_DELIMITER,
        PIPELINE_METRICS_COLUMN,
    )

    return pipeline_metrics


if __name__ == "__main__":

    logging_configuration(LOG_FILE)
    run_id = get_run_id()

    try:

        pipeline_metrics = execute_procurement_delivery_compliance_pipeline(run_id)

        logging.info(
            "Pipeline processing completed | pipeline_name=%s | run_id=%s | status=%s",
            PIPELINE_NAME,
            run_id,
            pipeline_metrics.get("pipeline_status", "unknown"),
        )

    except Exception:
        logging.exception(
            "unhandled pipeline failure | pipeline_name=%s | run_id=%s",
            PIPELINE_NAME,
            run_id,
        )

        sys.exit(1)
