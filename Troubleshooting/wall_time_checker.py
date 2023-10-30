import os

# Define the directory where your .sb files are located
directory = '/home/millers7/scratch/omega_job_printer/whole_library_omega/'

# Name of the output file
output_file = 'wall_times.txt'

# Open the output file for writing
with open(output_file, 'w') as output:
    # Loop through all .sb files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.sb'):
            file_path = os.path.join(directory, filename)
            
            # Open the file and read its contents
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Search for and write lines containing '#SBATCH -t' to the output file
            for line_number, line in enumerate(lines, start=1):
                if '#SBATCH -t' in line:
                    output.write(f'File: {filename}, Line {line_number}: {line.strip()}\n')

print(f"Search complete. Results saved to {output_file}")

