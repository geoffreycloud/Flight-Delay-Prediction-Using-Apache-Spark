from pyspark.sql import SparkSession
from pyspark.sql.functions import floor, col, when
from ml_pipeline import load_model
from utils import get_schema_df
from transformations import write_batch

# Initialize the Spark session
spark = SparkSession.builder.appName("FlightDelayStream").getOrCreate()

# Get the schema for the streaming data
schema = get_schema_df()

# Read the streaming data
stream_df = spark.readStream \
    .option("header", True) \
    .option("maxFilesPerTrigger", 1) \
    .schema(schema) \
    .csv("stream_input/")
    
# Process the streaming data
processed = stream_df \
    .withColumn("departure_hour", floor(col("CRS_DEP_TIME") / 100)) \
    .withColumn("is_delayed", when(col("ARR_DELAY") > 15, 1).otherwise(0)) \
    .withColumn("carrier_flag", when(col("CARRIER_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("nas_flag", when(col("NAS_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("security_flag", when(col("SECURITY_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("late_aircraft_flag", when(col("LATE_AIRCRAFT_DELAY") > 0, 1).otherwise(0)) \
    .withColumn("weather_flag", when(col("WEATHER_DELAY") > 0, 1).otherwise(0))
    
# Load model
model = load_model()

query = processed.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, batch_id: write_batch(df, batch_id, model)) \
    .start()

query.awaitTermination()