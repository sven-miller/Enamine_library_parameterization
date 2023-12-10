import os

# Define the path to the text file containing the list of input file paths
file_list_path = "/home/millers7/projects/NP_Enamine_screen/NP_screen/NP_list.txt"

# Read the list of file paths from the text file
with open(file_list_path, "r") as file_list_file:
    file_paths = file_list_file.read().splitlines()

# Define the submit template with placeholders
submit_template = """#!/bin/bash
#SBATCH --job-name="param_filter_xtract"
#SBATCH --output="{output_filename}"
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8G
#SBATCH --constraint="lustre"
#SBATCH --export=ALL
#SBATCH --account=was136
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
    job_file_name = f"param_filter_extract_job_{i + 1}.sb"

    # Define the output filename based on the job file name
    output_filename = os.path.splitext(job_file_name.split("/")[-1])[0] + f".%j.%N.out"
    # Replace placeholders in the submit template with actual values
    job_file_content = submit_template.format(job_name=job_file_name, output_filename=output_filename) + "\n"

    # Append the command with file paths to the job file content
    for file_path in chunk:
        # Define the output name based on the input file name
        output_name = os.path.splitext(os.path.basename(file_path))[0]

        # Define the command template with input and output paths
        command_template_1 = f"mkdir /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}"
        command_template_2 = f"python /home/millers7/Enamine_library_parameterization/MedChem_ADME_low_level_filtering/RDkit_MedChem_filter_args.py /home/millers7/projects/NP_Enamine_screen/NP_screen/compiled_outputs/{output_name}_cleaned.csv /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}_medchem_params.csv"
        command_template_3 = f"python /home/millers7/Enamine_library_parameterization/MedChem_ADME_low_level_filtering/MedChem_discriminator_final.py /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}_medchem_params.csv {output_name}"
        command_template_4 = f"mkdir  /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/m_below4 && mkdir  /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/m_above4 && mkdir  /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/s_below4 && mkdir  /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/s_above4"
        command_template_extract_1 = f"python /home/millers7/Enamine_library_parameterization/fastROCS_screen_parse_analysis/sdf_extraction_script_numbered_output_top250.py /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}__m_above_4_sorted.csv /home/millers7/scratch/large_scale_ROCS_screen/output/{output_name}/ /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/m_above4/ --rows 250"
        command_template_extract_2 = f"python /home/millers7/Enamine_library_parameterization/fastROCS_screen_parse_analysis/sdf_extraction_script_numbered_output_top250.py /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}__m_below_4_sorted.csv /home/millers7/scratch/large_scale_ROCS_screen/output/{output_name}/ /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/m_below4/ --rows 250"
        command_template_extract_3 = f"python /home/millers7/Enamine_library_parameterization/fastROCS_screen_parse_analysis/sdf_extraction_script_numbered_output_top250.py /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}__s_above_4_sorted.csv /home/millers7/scratch/large_scale_ROCS_screen/output/{output_name}/ /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/s_above4/ --rows 250"
        command_template_extract_4 = f"python /home/millers7/Enamine_library_parameterization/fastROCS_screen_parse_analysis/sdf_extraction_script_numbered_output_top250.py /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/{output_name}__s_below_4_sorted.csv /home/millers7/scratch/large_scale_ROCS_screen/output/{output_name}/ /home/millers7/projects/NP_Enamine_screen/NP_screen/MedChem_filtering/{output_name}/s_below4/ --rows 250"

        command = command_template_1 + "\n" + command_template_2 + "\n" + command_template_3 + "\n" + command_template_4 + "\n" + command_template_extract_1 + "\n" + command_template_extract_2 + "\n" + command_template_extract_3 + "\n" + command_template_extract_4 + "\n" 
        job_file_content += command + "\n"

    # Write the job file content to a file
    with open(job_file_name, "w") as job_file:
        job_file.write(job_file_content)

    print(f"Created job file: {job_file_name}")

print("Job files created successfully.")

