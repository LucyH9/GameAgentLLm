import csv
import os


def append_game_result_to_csv(result_dict, filename="game_results_labeled_v2.csv"):
    file_exists = os.path.isfile(filename)
    fieldnames = list(result_dict.keys())

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(result_dict)