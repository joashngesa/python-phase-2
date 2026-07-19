from pathlib import Path
import csv


def write_output(output_path, data, output_delimiter, output_columns):

    folder_path = Path(output_path)

    try:
        folder_path.parent.mkdir(parents=True, exist_ok=True)

        with folder_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                delimiter=output_delimiter,
                fieldnames=output_columns,
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(data)
            print("write to: ", folder_path.resolve())
    except PermissionError:
        print(f"permission denied when writing to the folder {folder_path}")
    except OSError as e:
        print(f"an OS error occured when writing the file: {e}")
