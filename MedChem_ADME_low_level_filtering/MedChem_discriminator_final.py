import pandas as pd
import sys
import os

def separate_and_filter(input_file, output_base):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Separate based on 'Molecule Name' column
    df_starts_with_s = df[df['Molecule Name'].str.startswith('s_')]
    df_starts_with_m = df[df['Molecule Name'].str.startswith('m_')]

    # Filter rows where 'Brenk violations' column is not equal to 'True'
    df_starts_with_s_below_4 = df_starts_with_s[
        (df_starts_with_s['Brenk violations'] != True) & 
        (df_starts_with_s['Lipinski violations'] < 2) & 
        (df_starts_with_s['Rotatable Bonds'] <= 4) & 
        (df_starts_with_s['TPSA'].between(60, 140, inclusive='both')) &
        (df_starts_with_s['SMILES'].str.count('F') <= 4)
    ].copy()

    df_starts_with_m_below_4 = df_starts_with_m[
        (df_starts_with_m['Brenk violations'] != True) & 
        (df_starts_with_m['Lipinski violations'] < 2) & 
        (df_starts_with_m['Rotatable Bonds'] <= 4) & 
        (df_starts_with_m['TPSA'].between(60, 140, inclusive='both')) &
        (df_starts_with_m['SMILES'].str.count('F') <= 4)
    ].copy()

    df_starts_with_s_above_4 = df_starts_with_s[
        (df_starts_with_s['Brenk violations'] != True) & 
        (df_starts_with_s['Lipinski violations'] < 2) & 
        (df_starts_with_s['Rotatable Bonds'] > 4) & 
        (df_starts_with_s['TPSA'].between(60, 140, inclusive='both')) &
        (df_starts_with_s['SMILES'].str.count('F') <= 4)
    ].copy()

    df_starts_with_m_above_4 = df_starts_with_m[
        (df_starts_with_m['Brenk violations'] != True) & 
        (df_starts_with_m['Lipinski violations'] < 2) & 
        (df_starts_with_m['Rotatable Bonds'] > 4) & 
        (df_starts_with_m['TPSA'].between(60, 140, inclusive='both')) &
        (df_starts_with_m['SMILES'].str.count('F') <= 4)
    ].copy()

    # Calculate a new column as the product of 'ColorTanimoto' and 'TanimotoCombo'
    df_starts_with_s_below_4.loc[:, 'Product'] = df_starts_with_s_below_4['ColorTanimoto'] * df_starts_with_s_below_4['TanimotoCombo']
    df_starts_with_m_below_4.loc[:, 'Product'] = df_starts_with_m_below_4['ColorTanimoto'] * df_starts_with_m_below_4['TanimotoCombo']
    df_starts_with_s_above_4.loc[:, 'Product'] = df_starts_with_s_above_4['ColorTanimoto'] * df_starts_with_s_above_4['TanimotoCombo']
    df_starts_with_m_above_4.loc[:, 'Product'] = df_starts_with_m_above_4['ColorTanimoto'] * df_starts_with_m_above_4['TanimotoCombo']

    # Sort the DataFrames based on the 'Product' column in descending order
    df_starts_with_s_below_4_sorted = df_starts_with_s_below_4.sort_values(by='Product', ascending=False)
    df_starts_with_m_below_4_sorted = df_starts_with_m_below_4.sort_values(by='Product', ascending=False)
    df_starts_with_s_above_4_sorted = df_starts_with_s_above_4.sort_values(by='Product', ascending=False)
    df_starts_with_m_above_4_sorted = df_starts_with_m_above_4.sort_values(by='Product', ascending=False)

    # Append category to the output file names
    output_file_s_below_4_sorted = f"{output_base}_s_below_4_sorted.csv"
    output_file_m_below_4_sorted = f"{output_base}_m_below_4_sorted.csv"
    output_file_s_above_4_sorted = f"{output_base}_s_above_4_sorted.csv"
    output_file_m_above_4_sorted = f"{output_base}_m_above_4_sorted.csv"

    # Write the modified and sorted DataFrames to separate CSV files
    df_starts_with_s_below_4_sorted.to_csv(output_file_s_below_4_sorted, index=False)
    df_starts_with_m_below_4_sorted.to_csv(output_file_m_below_4_sorted, index=False)
    df_starts_with_s_above_4_sorted.to_csv(output_file_s_above_4_sorted, index=False)
    df_starts_with_m_above_4_sorted.to_csv(output_file_m_above_4_sorted, index=False)

    print(f"Rows with 'True' value in 'Brenk violations' column, 2+ Lipinski violations, 'TPSA' outside of 60-140, and more than 4 'F' in 'SMILES' removed. Output saved and sorted by product to {output_file_s_below_4_sorted}, {output_file_m_below_4_sorted}, {output_file_s_above_4_sorted}, and {output_file_m_above_4_sorted}")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv_file> <output_base>")
    else:
        input_csv = sys.argv[1]
        output_base = sys.argv[2]
        separate_and_filter(input_csv, output_base)

