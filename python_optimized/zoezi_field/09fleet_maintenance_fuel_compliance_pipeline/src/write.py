import csv
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def write_output(output_path, data, output_delimiter, output_columns):

    folder_output = Path(output_path)
    logger.debug(
        "Output writing started | path=%s | row_count=%d", folder_output, len(data)
    )

    folder_output.parent.mkdir(parents=True, exist_ok=True)

    with folder_output.open("w", encoding="utf-8", newline="") as file:
        write = csv.DictWriter(
            file,
            delimiter=output_delimiter,
            fieldnames=output_columns,
            extrasaction="ignore",
        )
        write.writeheader()
        write.writerows(data)

    logger.info(
        "Output writing completed | file=%s | path=%s | row_count=%d",
        folder_output.name,
        folder_output.resolve(),
        len(data),
    )
