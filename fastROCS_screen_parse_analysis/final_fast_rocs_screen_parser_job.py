import os

# Define the path to the text file containing the list of input file paths
file_list_path = "/home/millers7/scratch/large_scale_ROCS_screen/output_directories.txt"

# Read the list of file paths from the text file
with open(file_list_path, "r") as file_list_file:
    file_paths = file_list_file.read().splitlines()

# Define the submit template with placeholders
submit_template = """#!/bin/bash
#SBATCH --job-name="parse"
#SBATCH --output="{output_filename}"
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4G
#SBATCH --constraint="lustre"
#SBATCH --export=ALL
#SBATCH --account=was136
#SBATCH -t 48:00:00

#  Environment
module purge
module load slurm
module load cpu/0.15.4 gcc/10.2.0
module load anaconda3/2020.11
echo "Checking conda location..."
which conda

. $ANACONDA3HOME/etc/profile.d/conda.sh
conda deactivate
conda activate /home/millers7/.conda/envs/RNN
export OE_LICENSE=/home/millers7/oe_license.txt
export PATH="/home/millers7/projects/openeye/bin/:$PATH"

#   perform some basic unix commands

echo "----------------------------------"
echo "hostname= " `hostname`
echo "date= " `date`
echo "whoami= " `whoami`
echo "pwd= " `pwd`

echo "Checking OE_License location..."
echo $OE_LICENSE

echo "Checking python interpreter..."
which python

echo "Getting python enviroment details..."



# Start of job commands
"""

# Function to split a list into chunks of a specified size
def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

# Divide the list of file paths into chunks of 6
chunks = list(chunk_list(file_paths, 1))

# Create a job file for each chunk
for i, chunk in enumerate(chunks):
    # Define job file name
    job_file_name = f"parser_jobs/parser_job_{i + 1}.sb"

    # Define the output filename based on the job file name
    output_filename = os.path.splitext(job_file_name.split("/")[-1])[0] + f".%j.%N.out"
    # Replace placeholders in the submit template with actual values
    job_file_content = submit_template.format(job_name=job_file_name, output_filename=output_filename) + "\n"

    # Append the command with file paths to the job file content
    for file_path in chunk:
        # Define the output name based on the input file name
        output_name = os.path.splitext(os.path.basename(file_path))[0]

        # Define the command template with input and output paths
        command_template = f"python /home/millers7/Enamine_library_parameterization/fastROCS_screen_parse_analysis/sdf_parse_script_final.py --input_directory /home/millers7/scratch/large_scale_ROCS_screen/output/{output_name} --output_csv_path /home/millers7/scratch/large_scale_ROCS_screen/parser_outputs/{output_name}.csv"

        command = command_template
        job_file_content += command + "\n"

    # Write the job file content to a file
    with open(job_file_name, "w") as job_file:
        job_file.write(job_file_content)

    print(f"Created job file: {job_file_name}")

print("Job files created successfully.")

