import os

# Specify the directory where your *.out files are located
directory = "/home/millers7/scratch/omega_job_printer/"

# Define the target phrase
target_phrase = "slurmstepd"

# Create a list to store the filenames with errors
error_files = []

# Loop through *.out files in the specified directory
for filename in os.listdir(directory):
    if filename.endswith(".out"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            if target_phrase in file.read():
                error_files.append(filename)

# Save the error filenames to error_runs.txt
with open("error_runs.txt", 'w') as output_file:
    for filename in error_files:
        output_file.write(f"{filename}\n")

print("Error filenames saved to error_runs.txt")

