# import streamlit as st
# import time
# from kafka import KafkaConsumer
# import json
# import threading
# import pandas as pd
# import plotly.express as px

# # Kafka configuration
# kafka_broker = 'localhost:9092'
# topic = 'imu_data'

# # Create a Kafka consumer
# consumer = KafkaConsumer(
#     topic,
#     bootstrap_servers=kafka_broker,
#     value_deserializer=lambda v: v.decode('utf-8')
# )

# # Initialize a dictionary to store the latest IMU values
# latest_imu_values = {}

# # Initialize DataFrames to store historical data for plotting
# accel_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])
# gyro_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])
# orient_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])

# # Create placeholders for dynamic content
# accel_graph_placeholder = st.empty()
# gyro_graph_placeholder = st.empty()
# orient_graph_placeholder = st.empty()

# # Placeholders for IMU values
# accel_x_placeholder = st.empty()
# accel_y_placeholder = st.empty()
# accel_z_placeholder = st.empty()

# gyro_x_placeholder = st.empty()
# gyro_y_placeholder = st.empty()
# gyro_z_placeholder = st.empty()

# orient_x_placeholder = st.empty()
# orient_y_placeholder = st.empty()
# orient_z_placeholder = st.empty()

# def consume_kafka_topic():
#     global latest_imu_values
#     for message in consumer:
#         imu_values = message.value
#         imu_values = json.loads(imu_values)
#         latest_imu_values = imu_values

# def display_imu_values():
#     st.title("IMU Values")
#     st.write("Received IMU values from Kafka topic")

#     while True:
#         # Update the display values
#         if latest_imu_values:
#             current_time = time.time()
#             accel_x = latest_imu_values.get('accel_x', 'N/A')
#             accel_y = latest_imu_values.get('accel_y', 'N/A')
#             accel_z = latest_imu_values.get('accel_z', 'N/A')

#             gyro_x = latest_imu_values.get('angular_x', 'N/A')
#             gyro_y = latest_imu_values.get('angular_y', 'N/A')
#             gyro_z = latest_imu_values.get('angular_z', 'N/A')

#             orient_x = latest_imu_values.get('orientation_x', 'N/A')
#             orient_y = latest_imu_values.get('orientation_y', 'N/A')
#             orient_z = latest_imu_values.get('orientation_z', 'N/A')

#             # Update placeholders for IMU values
#             accel_x_placeholder.write(f"Accelerometer X: {accel_x}")
#             accel_y_placeholder.write(f"Accelerometer Y: {accel_y}")
#             accel_z_placeholder.write(f"Accelerometer Z: {accel_z}")

#             gyro_x_placeholder.write(f"Gyroscope X: {gyro_x}")
#             gyro_y_placeholder.write(f"Gyroscope Y: {gyro_y}")
#             gyro_z_placeholder.write(f"Gyroscope Z: {gyro_z}")

#             orient_x_placeholder.write(f"Orientation X: {orient_x}")
#             orient_y_placeholder.write(f"Orientation Y: {orient_y}")
#             orient_z_placeholder.write(f"Orientation Z: {orient_z}")

#             # Create a new DataFrame for the current values
#             new_accel_data = pd.DataFrame({'Time': [current_time], 'X': [accel_x], 'Y': [accel_y], 'Z': [accel_z]})
#             new_gyro_data = pd.DataFrame({'Time': [current_time], 'X': [gyro_x], 'Y': [gyro_y], 'Z': [gyro_z]})
#             new_orient_data = pd.DataFrame({'Time': [current_time], 'X': [orient_x], 'Y': [orient_y], 'Z': [orient_z]})

#             # Concatenate the new data with the existing DataFrames
#             global accel_df, gyro_df, orient_df
#             accel_df = pd.concat([accel_df, new_accel_data], ignore_index=True)
#             gyro_df = pd.concat([gyro_df, new_gyro_data], ignore_index=True)
#             orient_df = pd.concat([orient_df, new_orient_data], ignore_index=True)

#             # Update the graphs
#             with accel_graph_placeholder.container():
#                 st.subheader("Acceleration Data")
#                 fig = px.line(accel_df, x='Time', y=['X', 'Y', 'Z'], title='Acceleration Data')
#                 st.plotly_chart(fig, use_container_width=True)

#             with gyro_graph_placeholder.container():
#                 st.subheader("Gyroscope Data")
#                 fig = px.line(gyro_df, x='Time', y=['X', 'Y', 'Z'], title='Gyroscope Data')
#                 st.plotly_chart(fig, use_container_width=True)

#             with orient_graph_placeholder.container():
#                 st.subheader("Orientation Data")
#                 fig = px.line(orient_df, x='Time', y=['X', 'Y', 'Z'], title='Orientation Data')
#                 st.plotly_chart(fig, use_container_width=True)

#         # Wait for 1 second before updating the display
#         time.sleep(1)

# if __name__ == '__main__':
#     # Start a separate thread to consume the Kafka topic
#     threading.Thread(target=consume_kafka_topic).start()

#     display_imu_values()


import streamlit as st
import time
from kafka import KafkaConsumer
import json
import threading
import pandas as pd
import plotly.express as px

# Kafka configuration
kafka_broker = 'localhost:9092'
topic = 'imu_data'

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=kafka_broker,
    value_deserializer=lambda v: v.decode('utf-8')
)

# Initialize a dictionary to store the latest IMU values
latest_imu_values = {}

# Initialize DataFrames to store historical data for plotting
accel_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])
gyro_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])
orient_df = pd.DataFrame(columns=['Time', 'X', 'Y', 'Z'])

# Create placeholders for dynamic content
accel_x_placeholder = st.empty()
accel_y_placeholder = st.empty()
accel_z_placeholder = st.empty()

gyro_x_placeholder = st.empty()
gyro_y_placeholder = st.empty()
gyro_z_placeholder = st.empty()

orient_x_placeholder = st.empty()
orient_y_placeholder = st.empty()
orient_z_placeholder = st.empty()

# Create placeholders for graphs
accel_graph_placeholder = st.empty()
gyro_graph_placeholder = st.empty()
orient_graph_placeholder = st.empty()

def consume_kafka_topic():
    global latest_imu_values
    for message in consumer:
        imu_values = message.value
        imu_values = json.loads(imu_values)
        latest_imu_values = imu_values

def display_imu_values():
    st.title("IMU Values")
    st.write("Received IMU values from Kafka topic")

    while True:
        # Update the display values
        if latest_imu_values:
            current_time = time.time()
            accel_x = latest_imu_values.get('accel_x', 'N/A')
            accel_y = latest_imu_values.get('accel_y', 'N/A')
            accel_z = latest_imu_values.get('accel_z', 'N/A')

            gyro_x = latest_imu_values.get('angular_x', 'N/A')
            gyro_y = latest_imu_values.get('angular_y', 'N/A')
            gyro_z = latest_imu_values.get('angular_z', 'N/A')

            orient_x = latest_imu_values.get('orientation_x', 'N/A')
            orient_y = latest_imu_values.get('orientation_y', 'N/A')
            orient_z = latest_imu_values.get('orientation_z', 'N/A')

            # Update placeholders for IMU values
            accel_x_placeholder.write(f"Accelerometer X: {accel_x}")
            accel_y_placeholder.write(f"Accelerometer Y: {accel_y}")
            accel_z_placeholder.write(f"Accelerometer Z: {accel_z}")

            gyro_x_placeholder.write(f"Gyroscope X: {gyro_x}")
            gyro_y_placeholder.write(f"Gyroscope Y: {gyro_y}")
            gyro_z_placeholder.write(f"Gyroscope Z: {gyro_z}")

            orient_x_placeholder.write(f"Orientation X: {orient_x}")
            orient_y_placeholder.write(f"Orientation Y: {orient_y}")
            orient_z_placeholder.write(f"Orientation Z: {orient_z}")

            # Create a new DataFrame for the current values
            new_accel_data = pd.DataFrame({'Time': [current_time], 'X': [accel_x], 'Y': [accel_y], 'Z': [accel_z]})
            new_gyro_data = pd.DataFrame({'Time': [current_time], 'X': [gyro_x], 'Y': [gyro_y], 'Z': [gyro_z]})
            new_orient_data = pd.DataFrame({'Time': [current_time], 'X': [orient_x], 'Y': [orient_y], 'Z': [orient_z]})

            # Concatenate the new data with the existing DataFrames
            global accel_df, gyro_df, orient_df
            accel_df = pd.concat([accel_df, new_accel_data], ignore_index=True)
            gyro_df = pd.concat([gyro_df, new_gyro_data], ignore_index=True)
            orient_df = pd.concat([orient_df, new_orient_data], ignore_index=True)

            # Update the graphs
            with accel_graph_placeholder.container():
                st.subheader("Acceleration Data")
                fig = px.line(accel_df, x='Time', y=['X', 'Y', 'Z'], title='Acceleration Data')
                st.plotly_chart(fig, use_container_width=True)

            with gyro_graph_placeholder.container():
                st.subheader("Gyroscope Data")
                fig = px.line(gyro_df, x='Time', y=['X', 'Y', 'Z'], title='Gyroscope Data')
                st.plotly_chart(fig, use_container_width=True)

            with orient_graph_placeholder.container():
                st.subheader("Orientation Data")
                fig = px.line(orient_df, x='Time', y=['X', 'Y', 'Z'], title='Orientation Data')
                st.plotly_chart(fig, use_container_width=True)

        # Wait for 1 second before updating the display
        time.sleep(1)

if __name__ == '__main__':
    # Start a separate thread to consume the Kafka topic
    threading.Thread(target=consume_kafka_topic).start()

    display_imu_values()