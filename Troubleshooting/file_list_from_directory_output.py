import os

def list_files(directory, output_file):
    with open(output_file, 'w') as file:
        for filename in os.listdir(directory):
            file.write(filename + '\n')

# Replace 'your_directory_path' with the path of the directory you want to list files from
directory_path = '/home/millers7/scratch/large_scale_ROCS_screen/output/Zunyimycin_A/'

# Replace 'output.txt' with the desired output file name
output_file_name = 'outputs.txt'

list_files(directory_path, output_file_name)

