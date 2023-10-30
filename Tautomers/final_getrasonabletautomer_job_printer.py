import os
import glob

# Define the input directory where your files are located
input_directory = "/expanse/lustre/scratch/millers7/temp_project/Enamine_NP_library_smiles"

# Define the submit template
submit_template = """#!/bin/bash
#SBATCH --job-name="t1"
#SBATCH --output="tautomers.%j.%N.out"
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=2G
#SBATCH --constraint="lustre"
#SBATCH --export=ALL
#SBATCH --account=was138
#SBATCH -t 24:00:00

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
export OE_LICENSE=/home/tjagraham/software/openeye_lic/oe_license.txt

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
env | grep PYTHON


# Start of job commands
"""

# Get a list of file paths in the input directory
file_paths = glob.glob(os.path.join(input_directory, '*'))

# Function to split a list into chunks of a specified size
def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

# Divide the list of file paths into chunks of 500
chunks = list(chunk_list(file_paths, 400))

# Create a job file for each chunk
for i, chunk in enumerate(chunks):
    job_file_name = f"tautomer_job_{i + 1}.sb"
    job_file_content = submit_template + "\n"

    # Append the command with file paths to the job file content
    for file_path in chunk:
        # Define the output name based on the input file name
        output_name = os.path.splitext(os.path.basename(file_path))[0] + "__tautomers.smi"
        
        # Define the command template with input and output paths
        command_template = f"python /home/millers7/scratch/tautomer_job_printer/getreasonabletautomers.py {file_path} /expanse/lustre/scratch/millers7/temp_project/Enamine_NP_library_tautomer_output/{output_name}"
        
        command = command_template
        job_file_content += command + "\n"

    # Write the job file content to a file
    with open(job_file_name, "w") as job_file:
        job_file.write(job_file_content)

    print(f"Created job file: {job_file_name}")

print("Job files created successfully.")

