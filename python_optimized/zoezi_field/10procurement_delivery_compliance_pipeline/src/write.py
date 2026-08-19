from pathlib import Path
import csv
import logging

logger = logging.getLogger(__name__)


def write_output(output_path, data, output_delimiter, output_column):

    file_path = Path(output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    logger.debug(
        "Output writing initiated | path=%s | file=%s | file_count=%d",
        file_path,
        file_path.name,
        len(data),
    )

    with file_path.open("w", encoding="utf-8", newline="") as file:
        write = csv.DictWriter(
            file,
            fieldnames=output_column,
            delimiter=output_delimiter,
            extrasaction="ignore",
        )
        write.writeheader()
        write.writerows(data)

    logger.info(
        "Output writing initiated | path=%s | file=%s | file_count=%d",
        file_path,
        file_path.name,
        len(data),
    )
