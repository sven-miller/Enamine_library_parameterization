#!/bin/bash

# Define the output file
output_file="omega_results.txt"

# Ensure the output file starts empty
> "$output_file"

# Loop through each file in the file_list.txt
while IFS= read -r file
do
  # Run your script for each file and extract the number of molecules
  num_molecules=$(python molcount.py ../Enamine_NP_library_oeomega_fastrocs_output/"$file" | grep -Eo '[0-9]+' | awk '{s+=$1} END {print s}')
  
  # Append the file name and the number of molecules to the output file
  echo "$file,$num_molecules" >> "$output_file"
done < job_outputs.txt

