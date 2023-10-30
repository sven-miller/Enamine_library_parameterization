import os

# Directory path where the files listed in filelist.txt are located
directory_path = '/home/millers7/scratch/omega_job_printer/whole_library_omega/'

# Initialize an empty list to store the extracted lines
output_text_list = []

# Read the list of files from filelist.txt
file_list_path = '/home/millers7/scratch/omega_job_printer/submit_job_1.txt'
try:
    with open(file_list_path, 'r') as file_list:
        files_to_process = file_list.read().splitlines()
except Exception as e:
    print(f"Error reading filelist.txt: {str(e)}")
    exit(1)

# Iterate through the listed files and search for *.oeb
for filename in files_to_process:
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path) and filename.endswith(".sb"):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if ".oeb" in line:
                        line = line.split("-out ")[-1].split(" -flipper")[0].split("/")[-1]
                        output_text_list.append(line.strip())
        
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")

# Write the extracted lines to an output file
output_file_path = 'files_submitted_to_omega.txt'
try:
    with open(output_file_path, 'w') as output_file:
        for line in output_text_list:
            output_file.write(line + '\n')
    print(f"Extracted lines written to {output_file_path}")
except Exception as e:
    print(f"Error writing to {output_file_path}: {str(e)}")

