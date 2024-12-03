## Prerequisites
Install all the pre-requisites given in the documentation folder

## Virtual Environment
Create a virtual environment and activate using the scripts given in the Instruction folder

## Hyper-IMU Setup
* Download Hyper-IMU from playstore
* Set the settings in app as shown in the pictures
![alt text](<Images/Screenshot 2024-12-03 174057.png>)
* Connect Laptop to phone's hotspot and put the IP shown in Hyper-IMU in the code

## Working
* After IP configuration, run the `prod2.py` file. This will receive values from the phone and publish it on a topic
![alt text](<Images/Screenshot from 2024-10-22 00-30-36.png>)

* Then run `cons2.py` to subscribe to the topic and recieve values. This will store the data received in a CSV file using HDFS
![alt text](<Images/Screenshot from 2024-10-22 00-29-50.png>)
![alt text](<Images/Screenshot from 2024-10-22 00-30-47.png>)

* Finally run the `guiqt.py` to run the Tkinter GUI
![alt text](<Images/Screenshot from 2024-10-22 00-29-14.png>)
![alt text](<Images/Screenshot from 2024-10-22 00-27-52.png>)
