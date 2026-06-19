# Dataset Overview

This project uses a dataset from the [Bureau of Transportation Statistics (BTS) On-Time Reporting Carrier Performance](https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ). The dataset contains historical records of U.S. domestic flights and operational performance metrics.

For this project, data from **January 2023** will be analyzed, consisting of approximately **540,000** flight records in the selected dataset.

Date features: `MONTH, DAY_OF_MONTH, DAY_OF_WEEK, FL_DATE`
Airline information: `OP_UNIQUE_CARRIER`
Airport information: `ORIGIN, ORIGIN_CITY_NAME, DEST, DEST_CITY_NAME`
Scheduling information: `CRS_DEP_TIME, CRS_ARR_TIME`
Delay information: `DEP_DELAY, ARR_DELAY`
Flight status: `CANCELLED, DIVERTED`
Flight distance: `DISTANCE`
Delay cause categories: `CARRIER_DELAY, WEATHER_DELAY, NAS_DELAY, SECURITY_DELAY, LATE_AIRCRAFT_DELAY`

These features provide information to analyze flight performance, identify the primary causes of delays, evaluate airline and airport reliability, examine delay patterns, and support the development of a flight delay prediction model using Apache Spark and Spark MLlib.
