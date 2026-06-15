from pyspark.sql import SparkSession
from pyspark.sql.functions import floor, col, when
from utils import get_schema_df, write_batch

# Initialize the Spark session
spark = SparkSession.builder.appName("FlightDelayStream").getOrCreate()

# Get the schema for the streaming data
schema = get_schema_df()

# Read the streaming data
stream_df = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv("stream_input/")
    
# Process the streaming data
processed = stream_df \
    .withColumn("hour", floor(col("CRS_DEP_TIME") / 100)) \
    .withColumn("is_delayed", when(col("ARR_DELAY") > 15, 1).otherwise(0)) \
    .withColumn("nas_flag", when(col("NAS_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("security_flag", when(col("SECURITY_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("late_aircraft_flag", when(col("LATE_AIRCRAFT_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("weather_flag", when(col("WEATHER_DELAY") > 0, 1).otherwise(0))
    
query = processed.writeStream \
    .outputMode("append") \
    .foreachBatch(write_batch) \
    .start()

query.awaitTermination()