# Automatic Cashier system

## Description

### web application

- Displays order summary from the server. Allows user to pay via cash or Thai Promptpay QR code.

### cv/cv_main.py

- main program for the computer vision system, used to get feed from camera and perform object recognition and tracking.

### server.py

- used to run the Flask server, handling the communication between the cv program, webapp, and MQTT broker.

### pi_code.py

- code used on Raspberry Pi, used to control the belt and for MQTT communication.
