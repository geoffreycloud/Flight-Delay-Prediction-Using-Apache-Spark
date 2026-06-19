#!/bin/bash
echo "Starting Spark Stream..."

spark-submit src/streaming.py &

echo "Waiting 10 seconds..."
sleep 10

echo "Starting ingestion..."
python src/ingestion.py

echo "Ingestion finished."
wait