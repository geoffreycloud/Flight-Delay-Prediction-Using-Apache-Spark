# Methodology

### Streaming Data Ingestion

To simulate a real-time flight monitoring system, the dataset is divided into multiple CSV batches and processed using Apache Spark Structured Streaming. A file-based streaming source continuously monitors an input directory (/stream_input/) for new flight data batches. As new files arrive, Spark processes them as micro-batches, enabling near real-time analytics.

The streaming pipeline uses a predefined schema to ensure consistency across all incoming batches and eliminate the need for schema inference during execution.

### Feature Engineering

Several features are created to support analysis and machine learning tasks:

`hour` – extracted from the scheduled departure time (CRS_DEP_TIME)
`is_delayed` – indicates whether a flight arrived 15 minutes or more behind schedule
`weather_flag` – identifies flights affected by weather-related delays
`nas_flag` – identifies delays caused by National Airspace System congestion
`security_flag` – identifies security-related delays
`late_aircraft_flag` – identifies delays caused by late-arriving aircraft

These engineered features simplify analytics and provide interpretable indicators of delay causes.

### Streaming Analytics

Each micro-batch is processed using Spark's `foreachBatch()` functionality, which treats each batch as an independent DataFrame and applies analytical transformations.

The following analyses are performed for each batch:

Airport Delay Analysis: 
- Flights are grouped by origin airport to calculate:
    - Total flights
    - Number of delayed flights
    - Delay rate percentage

This identifies airports that experience the highest frequency of delays.

Airline Performance Analysis:
- Flights are grouped by operating carrier to calculate:
    - Total flights
    - Number of delayed flights
    - Delay rate percentage

This enables comparison of delay performance across airlines.

Hourly Delay Trend Analysis:
- Flights are grouped by departure hour to determine:
    - Total flights by hour
    - Delay rate by hour

This helps identify periods of the day that are more susceptible to delays.

Delay Cause Analysis:
- Evaluates the contribution of:
    - Carrier delays
    - Weather delays
    - NAS delays
    - Security delays
    - Late aircraft delays

This analysis helps determine which delay factors are most responsible for flight disruptions.

### Output Generation

Results from each micro-batch are written to structured output directories using Spark's foreachBatch().

Each batch produces separate outputs for:

batch0/
- airport_delays/
- airline_delays/
- hourly_delays/
- delay_types/
- ml_predictions/

This structure preserves the results of each processing cycle and enables downstream reporting and visualization.

### Machine Learning Component

The project will develop a classification model that predicts whether a flight will be delayed.

The target variable is:

`is_delayed` (1 if arrival delay is greater than 15 minutes, otherwise 0)

Spark MLlib will be used to train and evaluate the model. Performance metrics such as accuracy, precision, recall, and F1-score will be used to evaluate performance.

### Technologies Used
*Apache Spark Structured Streaming* – streaming ingestion and processing
*Spark DataFrame API* – transformations and aggregations
*Spark MLlib* – delay prediction model
*Python (PySpark)* – pipeline implementation
*CSV File Storage* – streaming source and output sink
