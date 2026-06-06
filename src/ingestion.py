from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when
from utils import get_schema_df, get_row_count_df, get_summary_stats, get_missing_values


spark = SparkSession.builder \
    .appName("FlightDelayEDA") \
    .getOrCreate()

# Load data
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/sample.csv")

# EDA
schema_df = get_schema_df(df, spark)
row_count_df = get_row_count_df(df, spark)
summary_df = get_summary_stats(df)
missing_df = get_missing_values(df)

# Save Outputs
schema_df.write.mode("overwrite").csv("output/schema")
row_count_df.write.mode("overwrite").csv("output/row_count")
summary_df.write.mode("overwrite").csv("output/summary_stats")
missing_df.write.mode("overwrite").csv("output/missing_values")

df.write \
    .mode("overwrite") \
    .csv("output/eda_output")

print("\nData written to output/eda_output")

spark.stop()

