# import matplotlib
# matplotlib.use('TkAgg')  # Ensure TkAgg backend is used
# import json
# import tkinter as tk
# from kafka import KafkaConsumer
# from threading import Thread
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import numpy as np

# # Rest of the code remains the same...


# # Kafka configuration
# kafka_broker = 'localhost:9092'
# topic = 'imu_data'

# # Create a Kafka consumer
# consumer = KafkaConsumer(
#     topic,
#     bootstrap_servers=kafka_broker,
#     value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON data
# )

# # Create the GUI
# class IMUGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("IMU Data Monitor")
        
#         # Left Frame for IMU Data
#         self.left_frame = tk.Frame(root)
#         self.left_frame.pack(side=tk.LEFT, padx=20)

#         # Labels to display the IMU data (Left Aligned)
#         self.label_accel_x = tk.Label(self.left_frame, text="Accel X: ", font=('Helvetica', 14), anchor='w')
#         self.label_accel_y = tk.Label(self.left_frame, text="Accel Y: ", font=('Helvetica', 14), anchor='w')
#         self.label_accel_z = tk.Label(self.left_frame, text="Accel Z: ", font=('Helvetica', 14), anchor='w')
#         self.label_angular_x = tk.Label(self.left_frame, text="Angular X: ", font=('Helvetica', 14), anchor='w')
#         self.label_angular_y = tk.Label(self.left_frame, text="Angular Y: ", font=('Helvetica', 14), anchor='w')
#         self.label_angular_z = tk.Label(self.left_frame, text="Angular Z: ", font=('Helvetica', 14), anchor='w')
#         self.label_orientation_x = tk.Label(self.left_frame, text="Orientation X: ", font=('Helvetica', 14), anchor='w')
#         self.label_orientation_y = tk.Label(self.left_frame, text="Orientation Y: ", font=('Helvetica', 14), anchor='w')
#         self.label_orientation_z = tk.Label(self.left_frame, text="Orientation Z: ", font=('Helvetica', 14), anchor='w')

#         # Pack the labels into the window
#         self.label_accel_x.pack(fill='both')
#         self.label_accel_y.pack(fill='both')
#         self.label_accel_z.pack(fill='both')
#         self.label_angular_x.pack(fill='both')
#         self.label_angular_y.pack(fill='both')
#         self.label_angular_z.pack(fill='both')
#         self.label_orientation_x.pack(fill='both')
#         self.label_orientation_y.pack(fill='both')
#         self.label_orientation_z.pack(fill='both')

#         # Right Frame for Graphs
#         self.right_frame = tk.Frame(root)
#         self.right_frame.pack(side=tk.RIGHT, padx=20)

#         # Graphs for Acceleration, Angular Velocity, and Orientation
#         self.fig, (self.ax_accel, self.ax_angular, self.ax_orientation) = plt.subplots(3, 1, figsize=(5, 8))
#         self.fig.tight_layout(pad=3.0)

#         # Initial Data for Graphs (empty for now)
#         self.accel_data = [[], [], []]  # Accel X, Y, Z
#         self.angular_data = [[], [], []]  # Angular X, Y, Z
#         self.orientation_data = [[], [], []]  # Orientation X, Y, Z
#         self.time_data = []  # To plot against time

#         # Create Matplotlib canvas and add to Tkinter
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
#         self.canvas.get_tk_widget().pack()

#         # Start the thread to fetch and display Kafka messages
#         self.consumer_thread = Thread(target=self.update_gui_with_kafka_data, daemon=True)
#         self.consumer_thread.start()

#     def update_gui_with_kafka_data(self):
#         """Fetch IMU data from Kafka and update the GUI and graphs."""
#         for message in consumer:
#             imu_data = message.value
#             print(f"Received from Kafka: {imu_data}")

#             # Update the labels with the received IMU data
#             self.label_accel_x.config(text=f"Accel X: {imu_data['accel_x']}")
#             self.label_accel_y.config(text=f"Accel Y: {imu_data['accel_y']}")
#             self.label_accel_z.config(text=f"Accel Z: {imu_data['accel_z']}")
#             self.label_angular_x.config(text=f"Angular X: {imu_data['angular_x']}")
#             self.label_angular_y.config(text=f"Angular Y: {imu_data['angular_y']}")
#             self.label_angular_z.config(text=f"Angular Z: {imu_data['angular_z']}")
#             self.label_orientation_x.config(text=f"Orientation X: {imu_data['orientation_x']}")
#             self.label_orientation_y.config(text=f"Orientation Y: {imu_data['orientation_y']}")
#             self.label_orientation_z.config(text=f"Orientation Z: {imu_data['orientation_z']}")

#             # Update graph data
#             self.time_data.append(len(self.time_data))  # Simulating time steps

#             # Append IMU values for acceleration, angular velocity, and orientation
#             self.accel_data[0].append(imu_data['accel_x'])
#             self.accel_data[1].append(imu_data['accel_y'])
#             self.accel_data[2].append(imu_data['accel_z'])
#             self.angular_data[0].append(imu_data['angular_x'])
#             self.angular_data[1].append(imu_data['angular_y'])
#             self.angular_data[2].append(imu_data['angular_z'])
#             self.orientation_data[0].append(imu_data['orientation_x'])
#             self.orientation_data[1].append(imu_data['orientation_y'])
#             self.orientation_data[2].append(imu_data['orientation_z'])

#             # Limit data points to the last 100
#             if len(self.time_data) > 100:
#                 self.time_data = self.time_data[-100:]
#                 self.accel_data = [d[-100:] for d in self.accel_data]
#                 self.angular_data = [d[-100:] for d in self.angular_data]
#                 self.orientation_data = [d[-100:] for d in self.orientation_data]

#             # Update the graphs
#             self.update_graphs()

#     def update_graphs(self):
#         """Update the graphs with the latest IMU data."""
#         # Clear previous plots
#         self.ax_accel.clear()
#         self.ax_angular.clear()
#         self.ax_orientation.clear()

#         # Plot Acceleration Data
#         self.ax_accel.plot(self.time_data, self.accel_data[0], label='Accel X', color='r')
#         self.ax_accel.plot(self.time_data, self.accel_data[1], label='Accel Y', color='g')
#         self.ax_accel.plot(self.time_data, self.accel_data[2], label='Accel Z', color='b')
#         self.ax_accel.set_title('Acceleration')
#         self.ax_accel.legend()

#         # Plot Angular Velocity Data
#         self.ax_angular.plot(self.time_data, self.angular_data[0], label='Angular X', color='r')
#         self.ax_angular.plot(self.time_data, self.angular_data[1], label='Angular Y', color='g')
#         self.ax_angular.plot(self.time_data, self.angular_data[2], label='Angular Z', color='b')
#         self.ax_angular.set_title('Angular Velocity')
#         self.ax_angular.legend()

#         # Plot Orientation Data
#         self.ax_orientation.plot(self.time_data, self.orientation_data[0], label='Orientation X', color='r')
#         self.ax_orientation.plot(self.time_data, self.orientation_data[1], label='Orientation Y', color='g')
#         self.ax_orientation.plot(self.time_data, self.orientation_data[2], label='Orientation Z', color='b')
#         self.ax_orientation.set_title('Orientation')
#         self.ax_orientation.legend()

#         # Redraw the canvas
#         self.canvas.draw()

# if __name__ == "__main__":
#     # Set up the root Tkinter window
#     root = tk.Tk()
#     gui = IMUGUI(root)

#     # Start the Tkinter main loop
#     root.mainloop()



import matplotlib
matplotlib.use('TkAgg')  # Ensure TkAgg backend is used
import json
import tkinter as tk
from kafka import KafkaConsumer
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
import time

# Kafka configuration
kafka_broker = 'localhost:9092'
topic = 'imu_data'

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=kafka_broker,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON data
)

# Create the GUI
class IMUGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IMU Data Monitor")
        
        # Left Frame for IMU Data
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=20)

        # Labels to display the IMU data (Left Aligned)
        self.label_accel_x = tk.Label(self.left_frame, text="Accel X: ", font=('Helvetica', 14), anchor='w')
        self.label_accel_y = tk.Label(self.left_frame, text="Accel Y: ", font=('Helvetica', 14), anchor='w')
        self.label_accel_z = tk.Label(self.left_frame, text="Accel Z: ", font=('Helvetica', 14), anchor='w')
        self.label_angular_x = tk.Label(self.left_frame, text="Angular X: ", font=('Helvetica', 14), anchor='w')
        self.label_angular_y = tk.Label(self.left_frame, text="Angular Y: ", font=('Helvetica', 14), anchor='w')
        self.label_angular_z = tk.Label(self.left_frame, text="Angular Z: ", font=('Helvetica', 14), anchor='w')
        self.label_orientation_x = tk.Label(self.left_frame, text="Orientation X: ", font=('Helvetica', 14), anchor='w')
        self.label_orientation_y = tk.Label(self.left_frame, text="Orientation Y: ", font=('Helvetica', 14), anchor='w')
        self.label_orientation_z = tk.Label(self.left_frame, text="Orientation Z: ", font=('Helvetica', 14), anchor='w')

        # Pack the labels into the window
        self.label_accel_x.pack(fill='both')
        self.label_accel_y.pack(fill='both')
        self.label_accel_z.pack(fill='both')
        self.label_angular_x.pack(fill='both')
        self.label_angular_y.pack(fill='both')
        self.label_angular_z.pack(fill='both')
        self.label_orientation_x.pack(fill='both')
        self.label_orientation_y.pack(fill='both')
        self.label_orientation_z.pack(fill='both')

        # Right Frame for Graphs
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        # Graphs for Acceleration, Angular Velocity, and Orientation
        self.fig, (self.ax_accel, self.ax_angular, self.ax_orientation) = plt.subplots(3, 1, figsize=(5, 8))
        self.fig.tight_layout(pad=3.0)

        # Initial Data for Graphs (empty for now)
        self.accel_data = [[], [], []]  # Accel X, Y, Z
        self.angular_data = [[], [], []]  # Angular X, Y, Z
        self.orientation_data = [[], [], []]  # Orientation X, Y, Z
        self.time_data = []  # To plot against time

        # Create Matplotlib canvas and add to Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack()

        # Start the thread to fetch and display Kafka messages
        self.consumer_thread = Thread(target=self.update_gui_with_kafka_data, daemon=True)
        self.consumer_thread.start()

    def update_gui_with_kafka_data(self):
        """Fetch IMU data from Kafka and update the GUI and graphs."""
        for message in consumer:
            imu_data = message.value
            print(f"Received from Kafka: {imu_data}")

            # Update the labels with the received IMU data
            self.label_accel_x.config(text=f"Accel X: {imu_data['accel_x']}")
            self.label_accel_y.config(text=f"Accel Y: {imu_data['accel_y']}")
            self.label_accel_z.config(text=f"Accel Z: {imu_data['accel_z']}")
            self.label_angular_x.config(text=f"Angular X: {imu_data['angular_x']}")
            self.label_angular_y.config(text=f"Angular Y: {imu_data['angular_y']}")
            self.label_angular_z.config(text=f"Angular Z: {imu_data['angular_z']}")
            self.label_orientation_x.config(text=f"Orientation X: {imu_data['orientation_x']}")
            self.label_orientation_y.config(text=f"Orientation Y: {imu_data['orientation_y']}")
            self.label_orientation_z.config(text=f"Orientation Z: {imu_data['orientation_z']}")

            # Trigger an alert if data crosses a certain threshold
            if imu_data['accel_x'] > 10 or imu_data['accel_y'] > 10 or imu_data['accel_z'] > 10:
                alert_thread = Thread(target=self.show_alert, args=("High Acceleration Alert!",), daemon=True)
                alert_thread.start()

            # Update graph data
            self.time_data.append(len(self.time_data))  # Simulating time steps

            # Append IMU values for acceleration, angular velocity, and orientation
            self.accel_data[0].append(imu_data['accel_x'])
            self.accel_data[1].append(imu_data['accel_y'])
            self.accel_data[2].append(imu_data['accel_z'])
            self.angular_data[0].append(imu_data['angular_x'])
            self.angular_data[1].append(imu_data['angular_y'])
            self.angular_data[2].append(imu_data['angular_z'])
            self.orientation_data[0].append(imu_data['orientation_x'])
            self.orientation_data[1].append(imu_data['orientation_y'])
            self.orientation_data[2].append(imu_data['orientation_z'])

            # Limit data points to the last 100
            # if len(self.time_data) > 100:
            #     self.time_data = self.time_data[-100:]
            #     self.accel_data = [d[-100:] for d in self.accel_data]
            #     self.angular_data = [d[-100:] for d in self.angular_data]
            #     self.orientation_data = [d[-100:] for d in self.orientation_data]

            # Update the graphs
            self.update_graphs()

    def update_graphs(self):
        """Update the graphs with the latest IMU data."""
        # Clear previous plots
        self.ax_accel.clear()
        self.ax_angular.clear()
        self.ax_orientation.clear()

        # Plot Acceleration Data
        self.ax_accel.plot(self.time_data, self.accel_data[0], label='Accel X', color='r')
        self.ax_accel.plot(self.time_data, self.accel_data[1], label='Accel Y', color='g')
        self.ax_accel.plot(self.time_data, self.accel_data[2], label='Accel Z', color='b')
        self.ax_accel.set_title('Acceleration')
        self.ax_accel.legend()

        # Plot Angular Velocity Data
        self.ax_angular.plot(self.time_data, self.angular_data[0], label='Angular X', color='r')
        self.ax_angular.plot(self.time_data, self.angular_data[1], label='Angular Y', color='g')
        self.ax_angular.plot(self.time_data, self.angular_data[2], label='Angular Z', color='b')
        self.ax_angular.set_title('Angular Velocity')
        self.ax_angular.legend()

        # Plot Orientation Data
        self.ax_orientation.plot(self.time_data, self.orientation_data[0], label='Orientation X', color='r')
        self.ax_orientation.plot(self.time_data, self.orientation_data[1], label='Orientation Y', color='g')
        self.ax_orientation.plot(self.time_data, self.orientation_data[2], label='Orientation Z', color='b')
        self.ax_orientation.set_title('Orientation')
        self.ax_orientation.legend()

        # Redraw the canvas
        self.canvas.draw()

    def show_alert(self, message):
        """Show an alert message in a non-blocking way."""
        # Using tkinter's messagebox to show alerts
        messagebox.showwarning("Warning", message)

if __name__ == "__main__":
    # Set up the root Tkinter window
    root = tk.Tk()
    gui = IMUGUI(root)

    # Start the Tkinter main loop
    root.mainloop()
