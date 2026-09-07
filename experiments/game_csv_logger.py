import csv
import os


def append_game_result_to_csv(result_dict, filename="final_game_results_connect4.csv"):
    #Check whether the CSV file already exists.
    file_exists = os.path.isfile(filename)

    #Use the dictionary keys as the CSV column names.
    fieldnames = list(result_dict.keys())

    #Open the CSV file in append mode.
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        #Create a writer for the per-game results.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #Write the header row only if the file is new.
        if not file_exists:
            writer.writeheader()

        #Write one game's result to the CSV file.
        writer.writerow(result_dict)