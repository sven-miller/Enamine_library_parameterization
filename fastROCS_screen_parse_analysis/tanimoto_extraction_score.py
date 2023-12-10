import csv
import os

def process_csv(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read the header
        header = next(reader)

        # Check if the file has at least 5 columns
        if len(header) < 5:
            print(f"Skipping {input_path}: Not enough columns.")
            return

        # Write the header to the output file
        writer.writerow(['File Name', '1st Column', '2nd Column', '5th Column'])

        # Extract only the first 10 lines and write data to the output file
        for row in reader:
            if reader.line_num <= 10:
                data_to_write = [os.path.basename(input_path), row[0], row[1], row[4]]
                writer.writerow(data_to_write)

if __name__ == "__main__":
    input_directory = "/home/millers7/projects/NP_Enamine_screen/NP_screen/sorted_outputs/"  # Replace with the path to your CSV files
    output_file = "Top_tanimoto_scores.csv"

    # Loop through each CSV file in the specified directory
    for filename in os.listdir(input_directory):
        if filename.endswith("_sorted_combo_head500.csv"):
            input_path = os.path.join(input_directory, filename)
            process_csv(input_path, output_file)

    print("Processing complete. Output written to", output_file)

