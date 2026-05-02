import csv
import os


def append_result_to_csv(result_dict, filename="results.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=result_dict.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(result_dict)