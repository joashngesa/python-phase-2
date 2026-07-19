import csv
from pathlib import Path


def write_output(output_path, data, output_columns, output_delimiter):

    folder_output = Path(output_path)

    try:
        folder_output.parent.mkdir(parents=True, exist_ok=True)

        with folder_output.open("w", newline="", encoding="utf-8") as file:
            write = csv.DictWriter(
                file,
                fieldnames=output_columns,
                delimiter=output_delimiter,
                extrasaction="ignore",
            )
            write.writeheader()
            write.writerows(data)
            print(f"output path: {folder_output.resolve()}")

    except PermissionError:
        print(f"permission denied when writing to {folder_output.resolve()}")

    except OSError as e:
        print(f"OS error occured when writing the files: {e}")
