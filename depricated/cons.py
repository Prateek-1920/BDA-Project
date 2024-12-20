from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, DoubleType

# Create a SparkSession with the Kafka package
spark = SparkSession.builder \
    .appName("IMU Data Processor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
    .getOrCreate()

# Kafka configuration
kafka_broker = 'localhost:9092'
topic = 'imu_data'

# Define the schema for the IMU data
imu_schema = StructType([
    StructField("accel_x", DoubleType(), True),
    StructField("accel_y", DoubleType(), True),
    StructField("accel_z", DoubleType(), True),
    StructField("gyro_x", DoubleType(), True),
    StructField("gyro_y", DoubleType(), True),
    StructField("gyro_z", DoubleType(), True),
    StructField("timestamp", DoubleType(), True)
])

# Read data from the Kafka topic as a streaming DataFrame
imu_data_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic) \
    .load()

# Convert the Kafka value field to string and parse the JSON data
imu_data_df = imu_data_df.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), imu_schema).alias("imu_data")) \
    .select("imu_data.*")

# Start the query and write the output to the console
query = imu_data_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Wait for the streaming to finish
query.awaitTermination()
