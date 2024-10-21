import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Function to simulate real-time data for 9 sensor values
def load_data(n_samples):
    data = {
        'time': range(n_samples),
        'lin_accel_x': np.random.randn(n_samples) * 10,
        'lin_accel_y': np.random.randn(n_samples) * 10,
        'lin_accel_z': np.random.randn(n_samples) * 10,
        'gyro_x': np.random.randn(n_samples),
        'gyro_y': np.random.randn(n_samples),
        'gyro_z': np.random.randn(n_samples),
        'orient_x': np.random.randn(n_samples) * 50,
        'orient_y': np.random.randn(n_samples) * 50,
        'orient_z': np.random.randn(n_samples) * 50
    }
    return pd.DataFrame(data)

# Streamlit app layout
st.title("Real-time Sensor Data Visualization with Dropdown and Line Toggling")

# Parameters for the moving window
n_samples = 1000   # Total number of data points to simulate
window_size = 100  # Size of the moving window

# Dropdown menu to select graphs
graph_options = ['Linear Acceleration', 'Angular Velocity (Gyroscope)', 'Orientation']
selected_graphs = st.multiselect("Select which graphs to display", graph_options, default=graph_options)

# Initialize placeholders for each graph
accel_chart, gyro_chart, orient_chart = None, None, None

if 'Linear Acceleration' in selected_graphs:
    accel_chart = st.empty()
    st.subheader("Linear Acceleration Line Selection")
    show_accel_x = st.checkbox("Show Acceleration X", value=True, key='accel_x')
    show_accel_y = st.checkbox("Show Acceleration Y", value=True, key='accel_y')
    show_accel_z = st.checkbox("Show Acceleration Z", value=True, key='accel_z')

if 'Angular Velocity (Gyroscope)' in selected_graphs:
    gyro_chart = st.empty()
    st.subheader("Angular Velocity Line Selection")
    show_gyro_x = st.checkbox("Show Gyroscope X", value=True, key='gyro_x')
    show_gyro_y = st.checkbox("Show Gyroscope Y", value=True, key='gyro_y')
    show_gyro_z = st.checkbox("Show Gyroscope Z", value=True, key='gyro_z')

if 'Orientation' in selected_graphs:
    orient_chart = st.empty()
    st.subheader("Orientation Line Selection")
    show_orient_x = st.checkbox("Show Orientation X", value=True, key='orient_x')
    show_orient_y = st.checkbox("Show Orientation Y", value=True, key='orient_y')
    show_orient_z = st.checkbox("Show Orientation Z", value=True, key='orient_z')

# Simulate real-time data and update the plots
for i in range(n_samples - window_size):
    # Load the next window of data
    df = load_data(n_samples)[i:i+window_size]

    # 2D Line Plot for Linear Acceleration (X, Y, Z)
    if 'Linear Acceleration' in selected_graphs and accel_chart:
        accel_fig = go.Figure()
        if show_accel_x:
            accel_fig.add_trace(go.Scatter(x=df['time'], y=df['lin_accel_x'], mode='lines', name='X', line=dict(color='red')))
        if show_accel_y:
            accel_fig.add_trace(go.Scatter(x=df['time'], y=df['lin_accel_y'], mode='lines', name='Y', line=dict(color='green')))
        if show_accel_z:
            accel_fig.add_trace(go.Scatter(x=df['time'], y=df['lin_accel_z'], mode='lines', name='Z', line=dict(color='blue')))
        accel_fig.update_layout(title='Linear Acceleration (X, Y, Z)', xaxis_title='Time', yaxis_title='Acceleration')
        accel_chart.plotly_chart(accel_fig)

    # 2D Line Plot for Angular Velocity (Gyroscope X, Y, Z)
    if 'Angular Velocity (Gyroscope)' in selected_graphs and gyro_chart:
        gyro_fig = go.Figure()
        if show_gyro_x:
            gyro_fig.add_trace(go.Scatter(x=df['time'], y=df['gyro_x'], mode='lines', name='X', line=dict(color='red')))
        if show_gyro_y:
            gyro_fig.add_trace(go.Scatter(x=df['time'], y=df['gyro_y'], mode='lines', name='Y', line=dict(color='green')))
        if show_gyro_z:
            gyro_fig.add_trace(go.Scatter(x=df['time'], y=df['gyro_z'], mode='lines', name='Z', line=dict(color='blue')))
        gyro_fig.update_layout(title='Angular Velocity (Gyroscope X, Y, Z)', xaxis_title='Time', yaxis_title='Angular Velocity')
        gyro_chart.plotly_chart(gyro_fig)

    # 2D Line Plot for Orientation (X, Y, Z)
    if 'Orientation' in selected_graphs and orient_chart:
        orient_fig = go.Figure()
        if show_orient_x:
            orient_fig.add_trace(go.Scatter(x=df['time'], y=df['orient_x'], mode='lines', name='X', line=dict(color='red')))
        if show_orient_y:
            orient_fig.add_trace(go.Scatter(x=df['time'], y=df['orient_y'], mode='lines', name='Y', line=dict(color='green')))
        if show_orient_z:
            orient_fig.add_trace(go.Scatter(x=df['time'], y=df['orient_z'], mode='lines', name='Z', line=dict(color='blue')))
        orient_fig.update_layout(title='Orientation (X, Y, Z)', xaxis_title='Time', yaxis_title='Orientation')
        orient_chart.plotly_chart(orient_fig)

    # Pause to simulate real-time updates
    time.sleep(0.1)  # Adjust this to control the speed of the updates
