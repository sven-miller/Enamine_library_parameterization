import os
import pandas as pd
from rdkit import Chem
import argparse

def process_csv(csv_file, sdf_directory, output_directory):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Extract name from the first column
        name = row.iloc[0]

        # Extract SDF file name from the 6th column
        sdf_file_name = row.iloc[5]

        # Construct the full path to the SDF file in the reference directory
        sdf_path = os.path.join(sdf_directory, sdf_file_name)

        # Read SDF file using RDKit
        mol_supplier = Chem.SDMolSupplier(sdf_path)

        # Iterate through each molecule in the SDF file
        for mol_index, mol in enumerate(mol_supplier):
            # Check if the molecule has the desired name
            if mol.GetProp('_Name') == name:
                # Write the molecule to a new SDF file in the output directory
                output_sdf_path = os.path.join(output_directory, f"{index + 1}_{name}.sdf")
                writer = Chem.SDWriter(output_sdf_path)
                writer.write(mol)
                writer.close()
                print(f"Processed: {name} - Output SDF: {output_sdf_path}")
                break

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Process CSV file and generate SDF files.')
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file')
    parser.add_argument('sdf_directory', type=str, help='Path to the directory containing reference SDF files')
    parser.add_argument('output_directory', type=str, help='Path to the output directory')

    # Parse command-line arguments
    args = parser.parse_args()

    # Process the CSV file and generate SDF files
    process_csv(args.csv_file_path, args.sdf_directory, args.output_directory)

if __name__ == "__main__":
    main()

