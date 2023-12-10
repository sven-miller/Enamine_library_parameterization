import argparse
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, Lipinski

def calculate_tpsa(mol):
    """Calculate the Topological Polar Surface Area (TPSA)."""
    return rdMolDescriptors.CalcTPSA(mol)

def calculate_lipinski_violations(mol):
    """Calculate the number of Lipinski rule violations."""
    return sum([
        Lipinski.NumHDonors(mol) > 5,
        Lipinski.NumHAcceptors(mol) > 10,
        Lipinski.NumRotatableBonds(mol) > 10,
        Lipinski.FractionCSP3(mol) > 0.3
    ])

def calculate_rotatable_bonds(mol):
    """Calculate the number of rotatable bonds."""
    return Lipinski.NumRotatableBonds(mol)

def has_brenk_alerts(mol):
    brenk_alerts = [
        '[!#6;!#1][N,S,O!H0]~[c,s]',
        '[!#6;!#1][N,S,O!H0]~[CH2][N,S,O!H0]',
        '[c;!R;!#6;!#1][C;!R;!#6;!#1]~[c,s]',
        '[c;!R;!#6;!#1][C;!R;!#6;!#1]~[CH2][N,S,O!H0]',
        '[$([N;!R;!H0][C;!R;!#6;!#1](=[O,S;!H0])=[O,S;!H0]),$([N;!R;!H0][C;!R;!#6;!#1]~[O,S;!H0])]',
        'c[Cl,Br,I]~[c,s]',
        'c[Cl,Br,I]~[CH2][N,S,O!H0]'
    ]

    for alert in brenk_alerts:
        pattern = Chem.MolFromSmarts(alert)
        if mol.HasSubstructMatch(pattern):
            return True
    return False

def main(input_csv_path, output_csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Process SMILES and calculate properties
    tpsa_values = []
    lipinski_violations = []
    rotatable_bonds_values = []
    brenk_violations = []

    for smiles in df['SMILES']:
        mol = Chem.MolFromSmiles(smiles)

        tpsa = calculate_tpsa(mol)
        lipinski_violation_count = calculate_lipinski_violations(mol)
        rotatable_bonds = calculate_rotatable_bonds(mol)
        brenk_violation = has_brenk_alerts(mol)

        tpsa_values.append(tpsa)
        lipinski_violations.append(lipinski_violation_count)
        rotatable_bonds_values.append(rotatable_bonds)
        brenk_violations.append(brenk_violation)

    # Add new columns to the DataFrame
    df['TPSA'] = tpsa_values
    df['Lipinski violations'] = lipinski_violations
    df['Rotatable Bonds'] = rotatable_bonds_values
    df['Brenk violations'] = brenk_violations

    # Save the DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process input CSV file and save results to output CSV file.')
    parser.add_argument('input_csv', help='Path to the input CSV file')
    parser.add_argument('output_csv', help='Path to the output CSV file')
    args = parser.parse_args()

    main(args.input_csv, args.output_csv)

