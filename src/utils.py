from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

def get_schema_df():
    schema = StructType([StructField('MONTH', IntegerType(), True),
                        StructField('DAY_OF_MONTH', IntegerType(), True),
                        StructField('DAY_OF_WEEK', IntegerType(), True),
                        StructField('FL_DATE', StringType(), True), StructField('OP_UNIQUE_CARRIER', StringType(), True),
                        StructField('ORIGIN', StringType(), True), StructField('ORIGIN_CITY_NAME', StringType(), True),
                        StructField('DEST', StringType(), True),
                        StructField('DEST_CITY_NAME', StringType(), True),
                        StructField('CRS_DEP_TIME', IntegerType(), True),
                        StructField('DEP_DELAY', DoubleType(), True),
                        StructField('CRS_ARR_TIME', IntegerType(), True),
                        StructField('ARR_DELAY', DoubleType(), True),
                        StructField('CANCELLED', DoubleType(), True),
                        StructField('DIVERTED', DoubleType(), True),
                        StructField('DISTANCE', DoubleType(), True),
                        StructField('CARRIER_DELAY', DoubleType(), True),
                        StructField('WEATHER_DELAY', DoubleType(), True),
                        StructField('NAS_DELAY', DoubleType(), True),
                        StructField('SECURITY_DELAY', DoubleType(), True),
                        StructField('LATE_AIRCRAFT_DELAY', DoubleType(), True)])
    return schema
