from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from pyspark.sql.types import StructType, StructField, DoubleType

# Create a SparkSession with the Kafka package
spark = SparkSession.builder \
    .appName("IMU Data Processor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
    .getOrCreate()

# Kafka configuration
kafka_broker = 'localhost:9092'  # Replace with your Kafka broker
topic = 'imu_data'  # Replace with your Kafka topic

# Define the schema for the IMU data (manual parsing, not from JSON)
imu_schema = StructType([
    StructField("accel_x", DoubleType(), True),
    StructField("accel_y", DoubleType(), True),
    StructField("accel_z", DoubleType(), True),
    StructField("angular_x", DoubleType(), True),
    StructField("angular_y", DoubleType(), True),
    StructField("angular_z", DoubleType(), True),
    StructField("gyro_x", DoubleType(), True),
    StructField("gyro_y", DoubleType(), True),
    StructField("gyro_z", DoubleType(), True)
    # StructField("timestamp", DoubleType(), True)
])

# Read data from the Kafka topic as a streaming DataFrame
imu_data_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic) \
    .load()

# Convert the Kafka value field (received as string) to individual fields by splitting the comma-separated string
imu_data_df = imu_data_df.selectExpr("CAST(value AS STRING) as value_string") \
    .select(
        split(col("value_string"), ",").getItem(0).cast(DoubleType()).alias("accel_x"),
        split(col("value_string"), ",").getItem(1).cast(DoubleType()).alias("accel_y"),
        split(col("value_string"), ",").getItem(2).cast(DoubleType()).alias("accel_z"),
        split(col("value_string"), ",").getItem(3).cast(DoubleType()).alias("angular_x"),
        split(col("value_string"), ",").getItem(4).cast(DoubleType()).alias("angular_y"),
        split(col("value_string"), ",").getItem(5).cast(DoubleType()).alias("angular_z"),
        split(col("value_string"), ",").getItem(5).cast(DoubleType()).alias("gyro_z"),
        split(col("value_string"), ",").getItem(5).cast(DoubleType()).alias("gyro_z"),
        split(col("value_string"), ",").getItem(5).cast(DoubleType()).alias("gyro_z"),


        # split(col("value_string"), ",").getItem(6).cast(DoubleType()).alias("timestamp")
    )

# Start the query to write the output to the console (for debugging)
console_query = imu_data_df.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Define the output path for the CSV file
csv_path = "data/imu_data"  # Change the path as needed
checkpoint_path = "data/checkpoints/imu_data"  # Checkpointing for fault tolerance

# Write to a single CSV file (ensure coalesce to avoid multiple output files)
csv_query = imu_data_df \
    .coalesce(1) \
    .writeStream \
    .format("csv") \
    .option("path", csv_path) \
    .option("checkpointLocation", checkpoint_path) \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .start()

# Wait for the streaming to finish
csv_query.awaitTermination()
