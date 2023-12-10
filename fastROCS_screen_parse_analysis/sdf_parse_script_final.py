import csv
import os
import argparse
from rdkit import Chem

def extract_tanimoto_scores(mol):
    # Extract Tanimoto scores if they exist
    shape_tanimoto = mol.GetProp("ShapeTanimoto") if mol.HasProp("ShapeTanimoto") else None
    color_tanimoto = mol.GetProp("ColorTanimoto") if mol.HasProp("ColorTanimoto") else None
    tanimoto_combo = mol.GetProp("TanimotoCombo") if mol.HasProp("TanimotoCombo") else None

    return shape_tanimoto, color_tanimoto, tanimoto_combo

def extract_and_write_tanimoto_scores(sdf_directory, output_csv_path):
    # Create a CSV file and write header
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Molecule Name', 'SMILES', 'ShapeTanimoto', 'ColorTanimoto', 'TanimotoCombo', 'SDF File Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Iterate over all SDF files in the directory
        for sdf_file_name in os.listdir(sdf_directory):
            if sdf_file_name.endswith(".sdf"):
                sdf_file_path = os.path.join(sdf_directory, sdf_file_name)

                # Load the SDF file
                suppl = Chem.SDMolSupplier(sdf_file_path)

                # Extract Tanimoto scores for each molecule in the SDF file
                for mol in suppl:
                    if mol is not None:
                        # Extract desired information (example: molecule name, SMILES)
                        mol_name = mol.GetProp("_Name")
                        smiles = Chem.MolToSmiles(mol)

                        # Extract Tanimoto scores
                        shape_tanimoto, color_tanimoto, tanimoto_combo = extract_tanimoto_scores(mol)

                        # Write information to CSV with SDF file name
                        writer.writerow({
                            'Molecule Name': mol_name,
                            'SMILES': smiles,
                            'ShapeTanimoto': shape_tanimoto,
                            'ColorTanimoto': color_tanimoto,
                            'TanimotoCombo': tanimoto_combo,
                            'SDF File Name': sdf_file_name
                        })

def main():
    parser = argparse.ArgumentParser(description='Extract Tanimoto scores from SDF files.')
    parser.add_argument('--input_directory', required=True, help='Path to the directory containing SDF files.')
    parser.add_argument('--output_csv_path', required=True, help='Path for the output CSV file.')

    args = parser.parse_args()

    # Call the function to extract information and write to CSV
    extract_and_write_tanimoto_scores(args.input_directory, args.output_csv_path)

if __name__ == "__main__":
    main()

