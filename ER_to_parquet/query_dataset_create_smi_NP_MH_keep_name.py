import os
import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import pyarrow.parquet as pq
import pandas as pd
from pyarrow import csv
import glob

file_pattern = "/expanse/lustre/scratch/millers7/temp_project/test_parq/"
parquet_database = glob.glob(os.path.join(file_pattern, '*.parquet'))


print(parquet_database)

parquet_database_q_out = "/expanse/lustre/scratch/millers7/temp_project/Enamine_NP_library_smiles"

smiles_dataset = ds.dataset(parquet_database, format="parquet")

#print(type(smiles_dataset))

#dataset_scanner = ds.Scanner.from_dataset(smiles_dataset, batch_size=1)

#print(type(dataset_scanner))

con = duckdb.connect()

num = 4


con.execute('PRAGMA threads=8')
query = con.execute(
        f"SELECT smiles, id FROM smiles_dataset WHERE num_aromatic_ring <= '{num}' AND HBD <= 5 AND HBA <= 10 AND MW <= 500 AND MW >= 275 AND sLogP <= 3.5 and HAC >= 14 and HAC <= 36 AND RotBonds <= 6"
    )
record_batch_reader = query.fetch_record_batch()

#print(type(record_batch_reader))


counter = 1

while True:
    try:
            # Process a single chunk here
            # pyarrow.lib.RecordBatch
        chunk = record_batch_reader.read_next_batch()
        #print(type(chunk))
        table = pa.Table.from_batches([chunk])
        record_batches = table.to_batches(max_chunksize=40000)
        for recbatchcount, record_batch in enumerate(record_batches):
            df = record_batch.to_pandas()
            #table = pa.Table.from_batches([chunk])
            #pq.write_table(table, f"{parquet_database_q_out}/er_query_out_{counter}.parquet")
            output_name = os.path.splitext(os.path.basename(parquet_database))[0]
            df.to_csv(f"{parquet_database_q_out}/{output_name}_{counter}_{recbatchcount}.smi", sep='\t', index=False, escapechar='n')
        print(counter)
        counter += 1
    except StopIteration:
        break
