import os
import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import pyarrow.parquet as pq
import pandas as pd
import glob

# Define the pattern to match the input Parquet files
file_pattern = '/expanse/lustre/scratch/millers7/temp_project/chem_space_parquet/MH*'
parquet_files = glob.glob(file_pattern)

# Output directory
parquet_database_q_out = "/expanse/lustre/scratch/millers7/temp_project/Enamine_NP_library_smiles"

con = duckdb.connect()

num = 4

con.execute('PRAGMA threads=8')

for input_file in parquet_files:
    # Load the current input Parquet file
    smiles_dataset = ds.dataset(input_file, format="parquet")

    # Run the query for the current input file
    query = con.execute(
        f"SELECT smiles, id FROM smiles_dataset WHERE num_aromatic_ring <= '{num}' AND HBD <= 5 AND HBA <= 10 AND MW <= 500 AND MW >= 275 AND sLogP <= 3.5 and HAC >= 14 and HAC <= 36 AND RotBonds <= 6"
    )
    record_batch_reader = query.fetch_record_batch()

    counter = 1

    while True:
        try:
            # Process a single chunk here
            chunk = record_batch_reader.read_next_batch()
            table = pa.Table.from_batches([chunk])
            record_batches = table.to_batches(max_chunksize=40000)
            for recbatchcount, record_batch in enumerate(record_batches):
                df = record_batch.to_pandas()

                # Extract the base name of the current input file
                input_file_basename = os.path.splitext(os.path.basename(input_file))[0]

                # Use the input file's base name in the output filename
                df.to_csv(f"{parquet_database_q_out}/{input_file_basename}_{counter}_{recbatchcount}.smi", sep='\t', index=False, escapechar='n')
            print(counter)
            counter += 1
        except StopIteration:
            break

