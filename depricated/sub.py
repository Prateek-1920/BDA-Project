import json
from kafka import KafkaConsumer

# Kafka configuration
kafka_broker = 'localhost:9092'  # Change this to your Kafka broker address
topic = 'imu_data'  # Change this to your desired Kafka topic

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=kafka_broker,
    group_id='imu_data_consumer',
    auto_offset_reset='earliest'  # Read from the beginning if no offset is found
)

def print_imu_data(imu_data):
    """ Print the parsed IMU data. """
    print(f"Received IMU data at {imu_data['timestamp']}:")
    print(f"  Acceleration: x={imu_data['accel_x']:.2f}, y={imu_data['accel_y']:.2f}, z={imu_data['accel_z']:.2f}")
    print(f"  Gyroscope: x={imu_data['gyro_x']:.2f}, y={imu_data['gyro_y']:.2f}, z={imu_data['gyro_z']:.2f}")

def main():
    for message in consumer:
        print(f"Received message: {message.value}")  # Debug output
        imu_data_json = message.value.decode('utf-8')
        imu_data = json.loads(imu_data_json)
        print_imu_data(imu_data)

if __name__ == '__main__':
    main()