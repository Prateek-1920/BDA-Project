import time
import random
import json
from kafka import KafkaProducer

# Kafka configuration
kafka_broker = 'localhost:9092'
topic = 'imu_data'

# Create a Kafka producer with JSON serialization
producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Ensure the data is serialized as JSON
)

def generate_dummy_imu_data():
    """Generate dummy IMU data."""
    return {
        'accel_x': random.uniform(-10.0, 10.0),
        'accel_y': random.uniform(-10.0, 10.0),
        'accel_z': random.uniform(-10.0, 10.0),
        'gyro_x': random.uniform(-180.0, 180.0),
        'gyro_y': random.uniform(-180.0, 180.0),
        'gyro_z': random.uniform(-180.0, 180.0),
        'timestamp': time.time()
    }

def main():
    while True:
        # Generate dummy IMU data
        imu_data = generate_dummy_imu_data()
        # Send data to Kafka
        producer.send(topic, value=imu_data)
        print(f"Sent: {imu_data}")  # Optional: Log the sent data
        producer.flush()  # Ensure all buffered records are sent
        time.sleep(1)  # Pause for a second before sending next message

if __name__ == '__main__':
    main()
