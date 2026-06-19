# Limitations

This document outlines known constraints, scoping decisions, and assumptions made during the development of the Flight Delay Prediction System.

## 1. Class Imbalance Not Addressed

The dataset is heavily skewed toward non-delayed flights (`is_delayed = 0`). I made a decision **not** to implement class weighting, oversampling, or undersampling, in order to keep the modeling pipeline simple and within project scope.

**Observed impact (full dataset, ~538,837 records, batches of 75,000):**

| | predicted 0 | predicted 1 |
|---|---|---|
| **actual 0 (not delayed)** | 425,713 (TN) | 234 (FP) |
| **actual 1 (delayed)** | 85,698 (FN) | 27,192 (TP) |

- **Precision (class 1) ≈ 99.1%** — when the model predicts "delayed," it is almost always correct.
- **Recall (class 1) ≈ 24.1%** — the model only identifies about 1 in 4 actual delays; the remaining ~76% are missed.
- **Overall (weighted) accuracy ≈ 84.1%**, weighted precision ≈ 86.6%, weighted recall ≈ 84.1%, weighted F1 ≈ 79.9%.

These weighted figures are heavily influenced by the ~95% majority class (not delayed). The class-1 precision/recall above are the meaningful numbers: the model behaves as a high-confidence, low-coverage delay detector — it rarely raises a false alarm, but misses the majority of real delays, particularly borderline ones near the 15-minute threshold.

This result is consistent with the decision not to address class imbalance (see above): without class weighting or threshold adjustment, the model defaults toward the majority class except when feature signals are unusually strong (e.g., severe delays).

**Possible future improvement:** class weighting or adjusting the classification threshold below the default 0.5 to trade precision for recall.

## 2. Small-Sample Noise in Per-Batch Aggregations (Largely Resolved at Full Scale)

Streaming aggregations (airport delay rate, airline delay rate) are computed **per batch**, not cumulatively across the full run. During early development, with small batches (500 rows), this produced statistically unreliable results for low-volume airports/routes — e.g., an airport with only 2 flights in a batch could show a 100% or 0% delay rate, which was not representative of its true performance.

With the full dataset (~540,000 records) now processed in batches of 75,000, this no longer an issue. Most airports and carriers receive enough flights per batch for delay rates to be meaningful. Very low-traffic regional airports may still show some noise within a single batch.

*Note that aggregations are per-batch (not cumulative across the full streaming run).*

## 3. Feature Set Limitations

The model uses `MONTH`, `DAY_OF_MONTH`, `DAY_OF_WEEK`, `departure_hour`, `DISTANCE`, `DEP_DELAY`, `OP_UNIQUE_CARRIER`, `ORIGIN`, and `DEST`. It does **not** include:
- Real-time weather conditions (only delay-minutes attributed to weather post-hoc, which isn't available at prediction time)
- Airport congestion history / traffic volume at time of departure
- Aircraft-specific or tail-number-level history

These would likely improve predictive power but were out of scope given the public dataset used.

## 4. Streaming Simulation, Not True Real-Time

Streaming ingestion is simulated by splitting a static CSV dataset into fixed-size batches (75000 rows each) and reading them via Spark Structured Streaming's file-based source. This does not reflect a true real-time data feed.

## 6. No Performance Optimization Benchmarking

Spark optimization techniques (caching, broadcast joins, partition tuning) were not applied in this version.

## 7. Public S3 Bucket for Dataset Hosting

The raw dataset is hosted in a publicly readable S3 bucket for reproducibility. This simplification was made because the dataset is non-sensitive public flight performance data.
