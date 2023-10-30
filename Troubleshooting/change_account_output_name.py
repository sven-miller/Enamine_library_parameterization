import os

# Define the directory where your .sb files are located
directory = '/home/millers7/scratch/omega_job_printer/test_swap/'

# Define the old and new values you want to replace
old_value_1 = '#SBATCH --account=was138'
new_value_1 = '#SBATCH --account=was136'


old_value_2 = '#SBATCH --output="omega.%j.%N.out"'
new_value_2 = f'#SBATCH --output="omega.self_name.%j.%N.out"'


# Loop through all .sb files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.sb'):
        file_path = os.path.join(directory, filename)

        # Extract the self_name (filename without extension)
        self_name = os.path.splitext(filename)[0]
        # Read the content of the file
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Replace the first old_value with the new_value
        updated_content = file_content.replace(old_value_1, new_value_1)
        
        # Replace the second old_value with the new_value
        updated_content = updated_content.replace(old_value_2, new_value_2)

        # Replace the "{self_name}" string with the actual self_name
        updated_content = updated_content.replace('self_name', self_name)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

print("Replacements complete.")

