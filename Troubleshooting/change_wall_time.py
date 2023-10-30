import os

# Define the directory where your .sb files are located
directory = '/home/millers7/scratch/omega_job_printer/test_swap/'

# Define the old and new values you want to replace
old_value = '#SBATCH -t 24:00:00'
new_value = '#SBATCH -t 30:00:00'

# Loop through all .sb files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.sb'):
        file_path = os.path.join(directory, filename)
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        # Replace the old_value with the new_value
        updated_content = file_content.replace(old_value, new_value)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

print("Replacement complete.")
