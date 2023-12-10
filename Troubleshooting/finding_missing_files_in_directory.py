import pandas as pd
import os

# Function to get a list of files in a directory
def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Read names from the text file using pandas
def read_names_from_txt(txt_file):
    return pd.read_csv(txt_file, header=None, names=['Name'])

# Compare names and print missing file names to an output text file
def compare_and_print_missing(directory, txt_file, output_file):
    # Get the list of files in the directory
    files_in_directory = list_files_in_directory(directory)

    # Read names from the text file
    names_df = read_names_from_txt(txt_file)

    # Get the list of names from the DataFrame
    names_list = names_df['Name'].tolist()

    # Find missing names
    missing_names = set(names_list) - set(files_in_directory)

    # Write missing names to the output text file
    with open(output_file, 'w') as output_txt:
        for name in missing_names:
            output_txt.write(name + '\n')

if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual path of the directory containing files
    directory_path = '/home/millers7/scratch/Enamine_NP_library_oeomega_fastrocs_output/'

    # Replace 'your_input_txt_file.txt' with the actual name of the input text file
    input_txt_file = 'files_submitted_round_6.txt'

    # Replace 'output_missing_files.txt' with the desired name for the output text file
    output_txt_file = 'output_missing_files.txt'

    compare_and_print_missing(directory_path, input_txt_file, output_txt_file)

