
import csv
import os

def write_output (output_path,data,output_delimiter,output_column):

    folder_output = os.path.dirname (output_path)
    if folder_output:
        os.makedirs (folder_output, exist_ok=True)

    with open (output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter (file, delimiter=output_delimiter, fieldnames=output_column, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
        print ("write to: ",os.path.abspath(output_path))