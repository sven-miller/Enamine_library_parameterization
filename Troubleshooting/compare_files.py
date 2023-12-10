def compare_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as output:
        set1 = set(line.strip() for line in f1)
        set2 = set(line.strip() for line in f2)

        missing_names = set1 - set2

        for name in missing_names:
            output.write(name + '\n')

# Replace 'file1.txt' and 'file2.txt' with the names of your input files
file1_name = 'compressed_library_stripped.txt'
file2_name = 'outputs_stripped.txt'

# Replace 'output.txt' with the desired output file name
output_file_name = 'missing_jobs.txt'

compare_files(file1_name, file2_name, output_file_name)

