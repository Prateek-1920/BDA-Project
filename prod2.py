import time
import json
import socket  # For TCP connection
from kafka import KafkaProducer

# Kafka configuration
kafka_broker = 'localhost:9092'
topic = 'imu_data'

# Create a Kafka producer with JSON serialization
producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Ensure the data is serialized as JSON
)

# TCP server configuration
tcp_host = '192.168.171.181'  # Connect laptop to phone hotspot, go to laptop wifi setting, put that IP
tcp_port = 12345       # Change to the port your app sends data to

def start_tcp_server():
    """Start a TCP server to receive IMU data from phone."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid 'address already in use' errors
    server_socket.bind((tcp_host, tcp_port))
    server_socket.listen(1)
    print(f"Listening for connections on {tcp_host}:{tcp_port}...")

    # Accept a single connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Set a timeout to avoid hanging indefinitely
    client_socket.settimeout(5.0)

    # Use a buffer to collect incoming data chunks
    buffer_size = 4096  # Increased buffer size to handle larger data
    data_buffer = ""

    while True:
        try:
            # Receive data in chunks from the phone
            data = client_socket.recv(buffer_size)  # Larger buffer size
            if not data:
                break

            # Append the received data to the buffer and decode it
            data_buffer += data.decode('utf-8')
            
            # Check for complete data messages by splitting on newline or another delimiter
            while '\n' in data_buffer:
                # Split the data buffer into messages (assuming newline-delimited data)
                message, data_buffer = data_buffer.split('\n', 1)  # Split into message and remaining buffer
                process_data(message)

        except socket.timeout:
            print("Socket timed out. No data received.")
        except ValueError:
            print("Error parsing the data. Skipping this packet.")
        except ConnectionResetError:
            print("Connection closed by client.")
            break

    client_socket.close()

def process_data(data_str):
    """Process the IMU data and send it to Kafka."""
    data_str = data_str.strip()  # Remove any surrounding whitespace
    print(f"Received: {data_str}")

    imu_values = data_str.split(',')

    if len(imu_values) == 9:  
        try:
            imu_data = {
                'accel_x': float(imu_values[0]),
                'accel_y': float(imu_values[1]),
                'accel_z': float(imu_values[2]),
                'angular_x': float(imu_values[3]),
                'angular_y': float(imu_values[4]),
                'angular_z': float(imu_values[5]),
                'orientation_x': float(imu_values[6]),
                'orientation_y': float(imu_values[7]),
                'orientation_z': float(imu_values[8])
            }
            print(f"Parsed IMU data: {imu_data}")

            # Send the IMU data to Kafka
            producer.send(topic, value=imu_data)
            producer.flush()  # Ensure data is sent immediately
            print(f"Sent to Kafka: {imu_data}")
        
        except ValueError as e:
            print(f"Error converting data to float: {e}")
    else:
        print(f"Unexpected number of values received: {imu_values}")

if __name__ == '__main__':
    start_tcp_server()
