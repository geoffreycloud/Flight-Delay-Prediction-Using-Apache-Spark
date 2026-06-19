import pandas as pd
import os
from pathlib import Path

# Setting up the path to the input file. In the final version, this will be an Amazon S3 link.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = "s3://flight-records-2023-2026/T_ONTIME_REPORTING.csv"
OUTPUT_DIR = PROJECT_ROOT / "stream_input"

df = pd.read_csv(INPUT_FILE)

os.makedirs(OUTPUT_DIR, exist_ok=True)

chunk_size = 75000 # Will change to 75000 for actual use

for i, start in enumerate(range(0, len(df), chunk_size)):
    chunk = df.iloc[start:start + chunk_size]

    chunk.to_csv(
        OUTPUT_DIR / f"flights_batch_{i}.csv",
        index=False
    )