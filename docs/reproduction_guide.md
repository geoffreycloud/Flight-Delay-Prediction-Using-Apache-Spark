# Reproduction Guide

This guide explains how to set up and run the full Flight Delay Prediction pipeline end-to-end, from data ingestion through streaming and ML inference.

## Prerequisites

- Python 3.10+ (developed/tested on Python 3.13)
- Apache Spark with `spark-submit` available on your PATH (PySpark installed via pip is sufficient for local mode)
- Java 8 or 11 (required by Spark)
- Git Bash

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Flight-Delay-Prediction-Using-Apache-Spark
```

## 2. Create and Activate a Virtual Environment

**macOS / Linux / WSL / Git Bash:**
```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
# or
source venv/bin/activate       # macOS/Linux/WSL
```

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't yet have a `requirements.txt`, the minimum required packages are:
```
pyspark
pandas
boto3
fsspec
s3fs
```

## 4. Run the Full Pipeline

From the project root, with the virtual environment active:

```bash
bash run.sh
```

This single command will:
1. **Ingest data** — download the dataset from the public S3 bucket and split it into simulated streaming batches under `stream_input/`.
2. **Train the model** — run `ml_pipeline.py`, which trains a Logistic Regression model on the dataset and saves it to `models/flight_delay_model/`.
3. **Run the streaming job** — process all batch files in `stream_input/` via Spark Structured Streaming, computing aggregations (airport delays, airline delays, hourly delay patterns, delay-cause rates) and running ML inference per batch. Outputs are written to `outputs/batch_<id>/`.

The streaming job uses `trigger(availableNow=True)`, meaning it processes all currently available batch files and then terminates automatically — no manual intervention is needed to stop it.

## Expected Outputs

After a successful run, you should see:

```
stream_input/
 ├── flights_batch_0.csv
 ├── flights_batch_1.csv
 └── ...

models/
 └── flight_delay_model/

outputs/
 ├── batch_0/
 │   ├── airport_delays/
 │   ├── airline_delays/
 │   ├── hourly_delays/
 │   ├── delay_rates/
 │   └── ml_predictions/
 ├── batch_1/
 └── ...
```

## Verifying the Run

To check results, open any `ml_predictions/part-*.csv` file and confirm it contains `is_delayed` and `prediction` columns side by side. You can also inspect the console output from `spark-submit`, which prints a summary table for each batch (airport delays, airline delays, hourly delays, delay-type rates) as it processes.

## Notes on Dataset Source

The full dataset is hosted publicly on S3 and downloaded automatically during ingestion:

```
https://flight-records-2023-2026.s3.us-east-2.amazonaws.com/T_ONTIME_REPORTING.csv
```

A small sample (`data/sample.csv`) is committed to this repository for quick testing.

## Known Runtime Considerations

- First run will be slower due to the initial dataset download from S3 (full dataset is significantly larger than the 2,500-row sample used during development).
- `chunk_size` in `ingestion.py` is currently set to 75,000 for full-scale runs to reduce the number of batch files generated.
