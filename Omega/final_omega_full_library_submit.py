import os
import glob

# Define the input directory where your files are located
input_directory = "/home/millers7/scratch/omega_job_printer/whole_library_omega/"

# Define the submit template
submit_template = ""

# Get a list of file paths in the input directory
file_paths = glob.glob(os.path.join(input_directory, '*'))

# Function to split a list into chunks of a specified size
def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

# Divide the list of file paths into chunks of 6
chunks = list(chunk_list(file_paths, 4000))

# Create a job file for each chunk
for i, chunk in enumerate(chunks):
    job_file_name = f"whole_library_omega/submit_job_{i + 1}.sh"
    job_file_content = submit_template

    # Append the command with file paths to the job file content
    for file_path in chunk:
        # Define the output name based on the input file name
        output_name = os.path.splitext(os.path.basename(file_path))[0] + "__oeomega.oeb"
        
        # Define the command template with input and output paths
        command_template = f"sbatch {file_path}"
        
        command = command_template
        job_file_content += command + "\n"

    # Write the job file content to a file
    with open(job_file_name, "w") as job_file:
        job_file.write(job_file_content)

    print(f"Created job file: {job_file_name}")

print("Job files created successfully.")

