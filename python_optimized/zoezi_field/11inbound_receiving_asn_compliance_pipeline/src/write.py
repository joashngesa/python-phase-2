from pathlib import Path
import csv
import logging

logger = logging.getLogger(__name__)


def write_output(data, output_path, output_delimiter, output_column):

    data_path = Path(output_path)
    data_path.parent.mkdir(parents=True, exist_ok=True)

    logger.debug(
        "Output writing initiated | path=%s | file=%s | file_count=%d",
        data_path,
        data_path.name,
        len(data),
    )

    with data_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=output_column,
            delimiter=output_delimiter,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(data)

    logger.info(
        "Output writing completed | path=%s | file=%s | file_count=%d",
        data_path,
        data_path.name,
        len(data),
    )
