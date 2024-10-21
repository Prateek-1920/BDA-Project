from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("Hello World").getOrCreate()

# Print "Hello" using PySpark
print("Hello")

# Stop the SparkSession
spark.stop()