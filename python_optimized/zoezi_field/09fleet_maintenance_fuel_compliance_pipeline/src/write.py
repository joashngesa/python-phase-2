import csv
from pathlib import Path


def write_output(output_path, data, output_delimiter, output_columns):

    folder_output = Path(output_path)

    try:
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
            print(f"\n📬 Output path: {folder_output.resolve()}")

    except PermissionError as error:
        print(f"Permission denied when writing to: {folder_output.resolve()}")

    except OSError as error:
        print(f"OSError occured when writing the files: {error}")
