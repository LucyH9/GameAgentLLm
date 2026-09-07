import csv
import os


def append_result_to_csv(result_dict, filename="results.csv"):
    #Check whether the CSV file already exists.
    file_exists = os.path.isfile(filename)

    #Open the CSV file in append mode.
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        #Create a writer using the keys of the result dictionary as column names.
        writer = csv.DictWriter(csvfile, fieldnames=result_dict.keys())

        #Write the header row only if the file is being created for the first time.
        if not file_exists:
            writer.writeheader()

        #Erite one result row to the CSV file.
        writer.writerow(result_dict)