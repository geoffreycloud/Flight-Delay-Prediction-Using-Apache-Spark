from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.functions import when, col
from pyspark.sql.functions import floor

INPUT_FILE = "./data/sample.csv"
MODEL_PATH = "./models/flight_delay_model"

def load_model():
    """Load the trained model."""
    return PipelineModel.load(MODEL_PATH)

spark = SparkSession.builder \
    .appName("FlightDelayML") \
    .getOrCreate()
    
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(INPUT_FILE)

# ============Building the model=============

# Create target variable (is_delayed = 1 if arrival delay is greater than 15 minutes, else 0)
df = df.withColumn(
    "is_delayed",
    when(col("ARR_DELAY") > 15, 1).otherwise(0)
)

# Extract departure hour
df = df.withColumn(
    "departure_hour",
    floor(col("CRS_DEP_TIME") / 100)
)

# Features
df_features = df.select(
    "MONTH",
    "DAY_OF_MONTH",
    "DAY_OF_WEEK",
    "departure_hour",
    "DISTANCE",
    "DEP_DELAY",
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "is_delayed"
).na.fill({"DEP_DELAY": 0, "DISTANCE": 0})

# Encoding categorical features
carrier_indexer = StringIndexer(
    inputCol="OP_UNIQUE_CARRIER",
    outputCol="carrier_idx",
    handleInvalid="keep"
)

origin_indexer = StringIndexer(
    inputCol="ORIGIN",
    outputCol="origin_idx",
    handleInvalid="keep"
)

dest_indexer = StringIndexer(
    inputCol="DEST",
    outputCol="dest_idx",
    handleInvalid="keep"
)

# Assemble feature vector
assembler = VectorAssembler(
    inputCols=[
        "MONTH",
        "DAY_OF_MONTH",
        "DAY_OF_WEEK",
        "departure_hour",
        "DISTANCE",
        "DEP_DELAY",
        "carrier_idx",
        "origin_idx",
        "dest_idx"
    ],
    outputCol="features"
)

lr = LogisticRegression(
    labelCol="is_delayed",
    featuresCol="features",
    maxIter=10,
    regParam=0.01
)

# Build Pipeline
pipeline = Pipeline(stages=[
    carrier_indexer,
    origin_indexer,
    dest_indexer,
    assembler,
    lr
])

# Train/Test Split
train_df, test_df = df_features.randomSplit(
    [0.8, 0.2],
    seed=42
)

print(f"Training Records: {train_df.count()}")
print(f"Testing Records: {test_df.count()}")

# Train Model
model = pipeline.fit(train_df)

# Generate Predictions
predictions = model.transform(test_df)

print("\nSample Predictions:")
predictions.select(
    "is_delayed",
    "prediction",
    "probability"
).show(10, truncate=False)

# Save Model
model.write().overwrite().save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")