import cv2
from ultralytics import YOLO
import requests
import paho.mqtt.publish as publish # pip3 install paho-mqtt
import paho.mqtt.client as mqtt
import requests
import time
import json
import random
import ssl
from config import laptop_Client_ID,laptop_Secret,laptop_Token
port = 1883 # default port
Server_ip = "broker.netpie.io" 

Alias = "Pi"

Subscribe_Topic = "@msg/Laptop/Msg"
Publish_Topic = "@msg/Pi/Msg"

Client_ID = laptop_Client_ID
Token = laptop_Secret
Secret = laptop_Token

MqttUser_Pass = {"username":Token,"password":Secret}


def on_connect(client, userdata, flags, rc):
    '''
    Callback function for when the client initially connects to the server
    '''
    print("Connected with result code "+str(rc))
    client.subscribe(Subscribe_Topic)

def on_message(client, userdata, msg):
    '''
    Callback function that is called when a message is received
    '''
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    text=msg.payload.decode("utf-8")
    if text == "CLEAR":
        response = requests.get(url='http://0.0.0.0:6969/clearitems')

client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.on_connect = on_connect # links connection event to function
client.on_message = on_message # links the message event to function

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()

# Load the YOLOv8 model
model = YOLO('best-n.pt') # nano model, runs quickest without GPU acceleration
model = YOLO('best-s.pt') # small model, performs quite well but might be slow with many objects

# clear the cart as a precaution
response = requests.get(url='http://0.0.0.0:6969/clearitems') 

# get the camera feed from the camera
cap = cv2.VideoCapture(1)

# Define a line for detection
line_x_coord = 1300

# Set to keep track of unique object IDs that crossed the line
crossed_ids = set()

# Dictionary to store count of each class crossing the line
class_counts = {}

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True,conf = 0.5)
        # Check if there are detections and the id attribute is not None
        if results[0].boxes and results[0].boxes.id is not None:
            # Get the boxes, track IDs, and class names
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_names = [results[0].names[i] for i in results[0].boxes.cls.int().cpu().tolist()]

            # Iterate over detected objects
            for box, track_id, class_name in zip(boxes, track_ids, class_names):
                x_center = box[0] + (box[2] / 2)  # Calculate center x-coordinate from box (x, y, w, h)

                # Check if this object has crossed the line and is not already counted
                if x_center > line_x_coord and track_id not in crossed_ids:
                    crossed_ids.add(track_id)
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                    try:
                        r = requests.post(url='http://0.0.0.0:6969/add',json={"name": f"{class_name}"}) # add item to cart
                    except:
                        print("Error")
                    print(f"Object ID {track_id} ({class_name}) has crossed the line.")

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Draw the detection line on the frame
        cv2.line(annotated_frame, (line_x_coord, 0), (line_x_coord, frame.shape[0]), (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

# Print the final class counts
print("Final class counts of objects that crossed the line:", class_counts)
