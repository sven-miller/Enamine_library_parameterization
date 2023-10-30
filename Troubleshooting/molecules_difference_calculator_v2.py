import os
import pandas as pd

df1 = pd.read_csv("fixpka_results.txt", header=None)
df2 = pd.read_csv("omega_results.txt", header=None)

df2[0] = df2[0].apply(lambda x: x.replace("__oeomega.oeb", ".smi"))

df = df1.merge(df2, on=0)

df["Difference"] = df["1_x"] - df["1_y"]

df.query("Difference > 500")[0].to_csv("jobs_to_resubmit.csv", index=False, header=False)

