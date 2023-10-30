import csv

# Function to read and load the CSV file into a list
def read_csv_file(file_name):
    data = []
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row[0])  # Assuming the file names are in the first column
    return data

# Load the contents of both CSV files
file1_data = read_csv_file('fixpka_input_names.csv')
file2_data = read_csv_file('omega_outputs_names.csv')

# Find unique file names
unique_files = set(file1_data).symmetric_difference(file2_data)

# Write unique file names to a new CSV file
with open('unsubmitted_jobs.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for file in unique_files:
        writer.writerow([file])

print("Unique file names have been saved to 'unsubmitted_jobs.csv'.")

