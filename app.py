import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

def load_data(n_samples):
    data = {
        'time': np.arange(0, n_samples),
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

st.title("Real-time Sensor Data Visualization with Time Range Selection")

n_samples = 1000
window_size = 100

graph_options = ['Linear Acceleration', 'Angular Velocity (Gyroscope)', 'Orientation']
selected_graphs = st.multiselect("Select which graphs to display", graph_options, default=graph_options)

if 'Linear Acceleration' in selected_graphs:
    st.subheader("Linear Acceleration Line Selection and Time Range")
    accel_chart = st.empty()
    show_accel_x = st.checkbox("Show Acceleration X", value=True, key='accel_x')
    show_accel_y = st.checkbox("Show Acceleration Y", value=True, key='accel_y')
    show_accel_z = st.checkbox("Show Acceleration Z", value=True, key='accel_z')
    accel_time_range = st.slider("Select Time Range for Linear Acceleration", 0, n_samples-1, (0, window_size), key='accel_time')

if 'Angular Velocity (Gyroscope)' in selected_graphs:
    st.subheader("Angular Velocity Line Selection and Time Range")
    gyro_chart = st.empty()
    show_gyro_x = st.checkbox("Show Gyroscope X", value=True, key='gyro_x')
    show_gyro_y = st.checkbox("Show Gyroscope Y", value=True, key='gyro_y')
    show_gyro_z = st.checkbox("Show Gyroscope Z", value=True, key='gyro_z')
    gyro_time_range = st.slider("Select Time Range for Gyroscope", 0, n_samples-1, (0, window_size), key='gyro_time')

if 'Orientation' in selected_graphs:
    st.subheader("Orientation Line Selection and Time Range")
    orient_chart = st.empty()
    show_orient_x = st.checkbox("Show Orientation X", value=True, key='orient_x')
    show_orient_y = st.checkbox("Show Orientation Y", value=True, key='orient_y')
    show_orient_z = st.checkbox("Show Orientation Z", value=True, key='orient_z')
    orient_time_range = st.slider("Select Time Range for Orientation", 0, n_samples-1, (0, window_size), key='orient_time')

for i in range(n_samples - window_size):
    df = load_data(n_samples)

    if 'Linear Acceleration' in selected_graphs:
        start_accel, end_accel = accel_time_range
        accel_fig = go.Figure()
        if show_accel_x:
            accel_fig.add_trace(go.Scatter(x=df['time'][start_accel:end_accel], y=df['lin_accel_x'][start_accel:end_accel], mode='lines', name='X', line=dict(color='red')))
        if show_accel_y:
            accel_fig.add_trace(go.Scatter(x=df['time'][start_accel:end_accel], y=df['lin_accel_y'][start_accel:end_accel], mode='lines', name='Y', line=dict(color='green')))
        if show_accel_z:
            accel_fig.add_trace(go.Scatter(x=df['time'][start_accel:end_accel], y=df['lin_accel_z'][start_accel:end_accel], mode='lines', name='Z', line=dict(color='blue')))
        accel_fig.update_layout(title='Linear Acceleration (X, Y, Z)', xaxis_title='Time', yaxis_title='Acceleration')
        accel_chart.plotly_chart(accel_fig)

    if 'Angular Velocity (Gyroscope)' in selected_graphs:
        start_gyro, end_gyro = gyro_time_range
        gyro_fig = go.Figure()
        if show_gyro_x:
            gyro_fig.add_trace(go.Scatter(x=df['time'][start_gyro:end_gyro], y=df['gyro_x'][start_gyro:end_gyro], mode='lines', name='X', line=dict(color='red')))
        if show_gyro_y:
            gyro_fig.add_trace(go.Scatter(x=df['time'][start_gyro:end_gyro], y=df['gyro_y'][start_gyro:end_gyro], mode='lines', name='Y', line=dict(color='green')))
        if show_gyro_z:
            gyro_fig.add_trace(go.Scatter(x=df['time'][start_gyro:end_gyro], y=df['gyro_z'][start_gyro:end_gyro], mode='lines', name='Z', line=dict(color='blue')))
        gyro_fig.update_layout(title='Angular Velocity (Gyroscope X, Y, Z)', xaxis_title='Time', yaxis_title='Angular Velocity')
        gyro_chart.plotly_chart(gyro_fig)

    if 'Orientation' in selected_graphs:
        start_orient, end_orient = orient_time_range
        orient_fig = go.Figure()
        if show_orient_x:
            orient_fig.add_trace(go.Scatter(x=df['time'][start_orient:end_orient], y=df['orient_x'][start_orient:end_orient], mode='lines', name='X', line=dict(color='red')))
        if show_orient_y:
            orient_fig.add_trace(go.Scatter(x=df['time'][start_orient:end_orient], y=df['orient_y'][start_orient:end_orient], mode='lines', name='Y', line=dict(color='green')))
        if show_orient_z:
            orient_fig.add_trace(go.Scatter(x=df['time'][start_orient:end_orient], y=df['orient_z'][start_orient:end_orient], mode='lines', name='Z', line=dict(color='blue')))
        orient_fig.update_layout(title='Orientation (X, Y, Z)', xaxis_title='Time', yaxis_title='Orientation')
        orient_chart.plotly_chart(orient_fig)

    time.sleep(0.1)
