# ITCS 6190 – Cloud Computing for Data Analysis

# v1.0.0 — Final Release

## Summary

This release marks the completion of the Flight Delay Prediction pipeline built on Apache Spark. The project processes the full January 2023 flight dataset (538,837 records) through an end-to-end Structured Streaming pipeline — ingesting data in  batches, computing delay-rate aggregations (by airline, airport, hour, and day), and applying an MLlib classification model to predict flight delays.

**Highlights:**
- Full-dataset run across 538,837 flight records, processed in 8 streaming batches (~75,000 rows each)
- MLlib delay classifier: 99.1% precision / 24.1% recall on the delayed class (high-confidence, low-coverage detector)
- Spark SQL aggregations covering airline delay rates, airport delay rates, hourly trends, delay-cause breakdown, and daily trend analysis
- Identified and documented a major anomaly: January 11, 2023 saw a 57.2% system-wide delay rate, more than double any other day
- Known limitations documented in `LIMITATIONS.md`, including the model's low recall and class-imbalance effects on weighted accuracy

## Documentation & Presentation

- 📄 Final report: [`results.md`](./results.md)
- 📄 Known limitations: [`LIMITATIONS.md`](./LIMITATIONS.md)
- 🎤 Final presentation slides: [Presentation](https://docs.google.com/presentation/d/1bnRHwZ-KdbSyXscu8n8XTHHo3j9hMrW2dyaKqgvT56U/edit?usp=sharing)
- 📓 EDA notebook: [`notebooks/eda.ipynb`](./notebooks/eda.ipynb)

## Running the Final Pipeline

**Requirements:**

**1. Clone and check out the release tag:**
```bash
git clone https://github.com/<your-username>/Flight-Delay-Prediction-Using-Apache-Spark.git
cd Flight-Delay-Prediction-Using-Apache-Spark
git checkout v1.0.0
```

**2. Run the streaming pipeline:**
Please refer to [reproduction_guide.md](https://github.com/geoffreycloud/Flight-Delay-Prediction-Using-Apache-Spark/blob/main/docs/reproduction_guide.md)
This produces per-batch outputs under `outputs/batch_0` through `outputs/batch_7`, each containing `airline_delays/`, `airport_delays/`, `hourly_delays/`, and `ml_predictions/` CSVs, plus `outputs/daily_trend/`.

**3. Run the EDA / results notebook:**
```bash
jupyter notebook notebooks/eda.ipynb
```
This loads the pipeline outputs and reproduces all figures and metrics summarized in `results.md`.

