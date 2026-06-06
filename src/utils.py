from pyspark.sql import functions as F

# -----------------------------
# Schema (write to text file)
# -----------------------------
def get_schema_df(df, spark):
    schema_str = df._jdf.schema().treeString()
    return spark.createDataFrame([(schema_str,)], ["schema"])


# -----------------------------
# Row count (as dataframe)
# -----------------------------
def get_row_count_df(df, spark):
    return spark.createDataFrame([(df.count(),)], ["row_count"])


# -----------------------------
# Summary statistics (Spark DF)
# -----------------------------
def get_summary_stats(df):
    return df.select(
        "DEP_DELAY",
        "ARR_DELAY",
        "DISTANCE"
    ).describe()


# -----------------------------
# Missing values (as dataframe)
# -----------------------------
def get_missing_values(df):
    return df.select([
        F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c in df.columns
    ])