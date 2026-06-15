from pyspark.sql import SparkSession
import pandas as pd
import os


df = pd.read_csv("data/sample.csv") # Will read from amazon s3 link in the final version

os.makedirs("input", exist_ok=True)

chunk_size = 500 # Will change to 50000 for actual use

for i, start in enumerate(range(0, len(df), chunk_size)):
    chunk = df.iloc[start:start + chunk_size]

    chunk.to_csv(
        f"input/flights_batch_{i}.csv",
        index=False
    )