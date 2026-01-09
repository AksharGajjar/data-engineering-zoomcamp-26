import sys
import pandas as pd

month = int(sys.argv[1])
df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df['month'] = month

df.to_parquet(f"output_{month}.parquet")

print("arguments", sys.argv)
print(df.head())
print(f"Running pipeline for month {month}")