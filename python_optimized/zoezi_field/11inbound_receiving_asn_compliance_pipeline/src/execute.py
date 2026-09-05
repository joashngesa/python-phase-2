import logging
import sys

from src.config import PIPELINE_NAME
from src.config import RUN_SUMMARIES_DIR
from src.config import PIPELINE_METRICS_COLUMN
from src.config import OUTPUT_DELIMITER
from src.config import LOG_FILE

from src.process import process_all_files
from src.metrics import pipeline_summary
from src.write import write_output
from src.log_config import logging_configuration
from src.utility import get_run_id

logger = logging.getLogger(__name__)


def execute_inbound_receiving_asn_compliance_pipeline(run_id: str):

    logger.info(
        "Pipeline processing initiated | run_id=%s | pipeline=%s",
        run_id,
        PIPELINE_NAME,
    )

    file_results = process_all_files(run_id)
    pipeline_digest = pipeline_summary(file_results, run_id)

    write_output(
        [pipeline_digest],
        RUN_SUMMARIES_DIR / "run_digest.csv",
        OUTPUT_DELIMITER,
        PIPELINE_METRICS_COLUMN,
    )

    return pipeline_digest


if __name__ == "__main__":

    logging_configuration(LOG_FILE)
    run_id = get_run_id()

    try:

        pipeline_digest = execute_inbound_receiving_asn_compliance_pipeline(run_id)
        logger.info(
            "Pipeline processing completed | run_id=%s | pipeline=%s | status=%s",
            run_id,
            PIPELINE_NAME,
            pipeline_digest.get("pipeline_status", "unknown"),
        )

    except Exception:

        logger.exception(
            "Unhandled pipeline failure | run_id=%s | pipeline=%s",
            run_id,
            PIPELINE_NAME,
        )

        sys.exit(1)
