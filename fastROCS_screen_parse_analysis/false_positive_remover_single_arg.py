import os
import csv
import re
import sys

def process_csv_file(input_file, output_file):
    partial_strings_to_remove = [
        'm_275592____18897282____14136862____19048342',
        'm_275592____14114646____14136092____15859698'
    ]

    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        lines = [line for line in reader if not any(re.search(partial_string, ','.join(line)) for partial_string in partial_strings_to_remove)]

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_csv_file>")
        sys.exit(1)

    input_csv_file = sys.argv[1]

    if not input_csv_file.endswith('.csv'):
        print("Error: Please provide a CSV file.")
        sys.exit(1)

    input_directory = os.path.dirname(input_csv_file)
    output_file_path = os.path.join(input_directory, f"{os.path.splitext(os.path.basename(input_csv_file))[0]}_cleaned.csv")

    process_csv_file(input_csv_file, output_file_path)
    print(f"Processed: {input_csv_file} --> {os.path.splitext(os.path.basename(input_csv_file))[0]}_cleaned.csv")

if __name__ == "__main__":
    main()

