"""
Evaluation script to compute confusion matrix, precision, recall, and F1 score for the batch predictions.
Assumes that the batch predictions are stored in "outputs/batch_*/ml_predictions/part-*.csv".

Run this after the streaming job has processed all batches and generated predictions.
"""

from pyspark.sql import SparkSession
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import glob

spark = SparkSession.builder.appName("Evaluate").getOrCreate()

# Load all batch ml_predictions outputs
paths = glob.glob("outputs/batch_*/ml_predictions/part-*.csv")
predictions = spark.read.option("header", True).option("inferSchema", True).csv(paths)
# Confusion matrix
print("\nConfusion Matrix:")
predictions.groupBy("is_delayed", "prediction").count().orderBy("is_delayed", "prediction").show()

# Precision / Recall / F1
evaluator = MulticlassClassificationEvaluator(
    labelCol="is_delayed", predictionCol="prediction"
)

accuracy = evaluator.setMetricName("accuracy").evaluate(predictions)
precision = evaluator.setMetricName("weightedPrecision").evaluate(predictions)
recall = evaluator.setMetricName("weightedRecall").evaluate(predictions)
f1 = evaluator.setMetricName("f1").evaluate(predictions)

count = predictions.count()
print(f"Total predictions: {count}")

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}\n")