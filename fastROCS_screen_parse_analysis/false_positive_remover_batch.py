import os
import csv
import re

directory_path = '/home/millers7/projects/NP_Enamine_screen/NP_screen/compiled_outputs/'
partial_strings_to_remove = [
    'm_275592____18897282____14136862____19048342',
    'm_275592____14114646____14136092____15859698'
]

def process_csv_file(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        lines = [line for line in reader if not any(re.search(partial_string, ','.join(line)) for partial_string in partial_strings_to_remove)]

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(lines)

def process_all_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, f"{os.path.splitext(filename)[0]}_cleaned.csv")
            
            process_csv_file(input_file, output_file)
            print(f"Processed: {filename} --> {os.path.splitext(filename)[0]}_cleaned.csv")

if __name__ == "__main__":
    process_all_csv_files(directory_path)

