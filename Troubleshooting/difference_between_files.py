file1 = 'omega_partial_run_list.txt'
file2 = 'files_submitted_to_omega.txt'
output_file = 'differences.txt'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    lines1 = set(f1.readlines())
    lines2 = set(f2.readlines())

lines_only_in_file2 = lines2 - lines1

# Write the lines only in file2 to the output file
with open(output_file, 'w') as output:
    output.writelines(lines_only_in_file2)

