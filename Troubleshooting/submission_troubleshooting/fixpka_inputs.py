import glob
import csv

# Directory path where your files are located
directory_path = '/expanse/lustre/scratch/millers7/temp_project/Enamine_NP_library_fixpka_output/'

# Pattern to match all files in the directory (e.g., all files with .txt extension)
file_pattern = '*.smi'

# List to store the file names
file_names = []

# Use glob to find files matching the pattern in the directory
file_names = glob.glob(f'{directory_path}/{file_pattern}')

# Output CSV file path
output_csv = 'fixpka_input_names.csv'

# Write the file names to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write a header if needed
    csv_writer.writerow(['File Name'])
    
    # Write the file names to the CSV file
    for file_name in file_names:
        csv_writer.writerow([file_name])

print(f"File names have been written to {output_csv}")

