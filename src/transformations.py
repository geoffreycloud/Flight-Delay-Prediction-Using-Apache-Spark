from pyspark.sql.functions import avg, col, when, floor, count, round, desc

def write_batch(batch_df, batch_id, model):
    """
    Write the batch data to a CSV file.

    :param batch_df: The DataFrame containing the batch data.
    :param batch_id: The ID of the batch.
    """

    print(f"\n===== Flight Batch {batch_id} =====")

    # Delay rate by airport
    airport_delays = batch_df.groupBy("ORIGIN", "ORIGIN_CITY_NAME").agg(
        count("*").alias("total_flights"),
        count(when(col("ARR_DELAY") >= 15, True)).alias("delayed_flights")
    ).withColumn(
        "delay_rate",
        round(col("delayed_flights") / col("total_flights") * 100, 2)
    ).orderBy(desc("delay_rate"))
    
    # Save the airport delays to a CSV file
    airport_delays.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(f"outputs/batch_{batch_id}/airport_delays")

    # Delay rates by airline
    airline_delays = batch_df.groupBy("OP_UNIQUE_CARRIER").agg(
        count("*").alias("total_flights"),
        count(when(col("ARR_DELAY") >= 15, True)).alias("delayed_flights")
    ).withColumn(
        "delay_rate",
        round(col("delayed_flights") / col("total_flights") * 100, 2)
    ).orderBy(desc("delay_rate"))
    
    # Save the airline delays to a CSV file
    airline_delays.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(f"outputs/batch_{batch_id}/airline_delays")

    # Delay rate by departure hour
    hourly = batch_df.withColumn(
        "departure_hour",
        floor(col("CRS_DEP_TIME") / 100)
    ).groupBy("departure_hour").agg(
        count("*").alias("total_flights"),
        round(avg(when(col("ARR_DELAY") >= 15, 1).otherwise(0)), 2).alias("delay_rate")
    ).orderBy("departure_hour")
    
    # Save the hourly delays to a CSV file
    hourly.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(f"outputs/batch_{batch_id}/hourly_delays")
        
    
    # Show the average delay rate for each type of delay
    delay_rates = batch_df.agg(
        round(avg("carrier_flag"), 4).alias("carrier_rate"),
        round(avg("nas_flag"), 4).alias("nas_rate"),
        round(avg("security_flag"), 4).alias("security_rate"),
        round(avg("late_aircraft_flag"), 4).alias("late_aircraft_rate"),
        round(avg("weather_flag"), 4).alias("weather_rate")
    )
    
    # Save the delay type rates to a CSV file
    delay_rates.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(f"outputs/batch_{batch_id}/delay_rates")
    
    # Make predictions using the trained model
    predictions = model.transform(batch_df)

    ml_output = predictions.select(
        "ORIGIN",
        "DEST",
        "OP_UNIQUE_CARRIER",
        "ARR_DELAY",
        "prediction",
    )

    ml_output.coalesce(1).write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(f"outputs/batch_{batch_id}/ml_predictions")

    # Print the results
    print("\nAIRPORT DELAYS")
    airport_delays.show()

    print("\nAIRLINE DELAYS")
    airline_delays.show()

    print("\nHOURLY DELAYS")
    hourly.show()

    print("\nDELAY TYPE RATES")
    delay_rates.show()
