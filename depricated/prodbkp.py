# import time
# import json
# import socket  # For TCP connection
# from kafka import KafkaProducer

# # Kafka configuration
# kafka_broker = 'localhost:9092'
# topic = 'imu_data'

# # Create a Kafka producer with JSON serialization
# producer = KafkaProducer(
#     bootstrap_servers=kafka_broker,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Ensure the data is serialized as JSON
# )

# # TCP server configuration
# tcp_host = '192.168.171.181'  # Listen on all available interfaces
# tcp_port = 12345       # Change to the port your app sends data to

# def start_tcp_server():
#     """Start a TCP server to receive IMU data from phone."""
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((tcp_host, tcp_port))
#     server_socket.listen(1)
#     print(f"Listening for connections on {tcp_host}:{tcp_port}...")

#     # Accept a single connection
#     client_socket, client_address = server_socket.accept()
#     print(f"Connection established with {client_address}")

#     while True:
#         try:
#             # Receive data from the phone
#             data = client_socket.recv(2048)  # Buffer size is 1024 bytes
#             if not data:
#                 break

#             # Decode the received data
#             data_str = data.decode('utf-8').strip()  # Decode and remove any surrounding whitespace
#             print(f"Received: {data_str}")

#             # Assuming the IMU data is comma-separated (e.g., "9.8,1.2,3.4,0.1,0.2,0.3,1616161616")
#             imu_values = data_str.split(',')

#             if len(imu_values) == 9:  # Expecting 7 values: accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, timestamp
#                 imu_data = {
#                     'accel_x': float(imu_values[0]),
#                     'accel_y': float(imu_values[1]),
#                     'accel_z': float(imu_values[2]),
#                     'angular_x': float(imu_values[3]),
#                     'angular_y': float(imu_values[4]),
#                     'angular_z': float(imu_values[5]),
#                     'orientation_x': float(imu_values[6]),
#                     'orientation_y': float(imu_values[7]),
#                     'orientation_z': float(imu_values[8])
#                 }
#                 print(f"Parsed IMU data: {imu_data}")

#                 # Send the IMU data to Kafka
#                 producer.send(topic, value=imu_data)
#                 producer.flush()
#                 print(f"Sent to Kafka: {imu_data}")
#             # else:
#             #     print(f"Unexpected number of values received: {imu_values}")

#         except ValueError:
#             print("Error parsing the data. Skipping this packet.")
#         except ConnectionResetError:
#             print("Connection closed by client.")
#             break

#     client_socket.close()

# if __name__ == '__main__':
#     start_tcp_server()

