import paho.mqtt.publish as publish # pip3 install paho-mqtt
import paho.mqtt.client as mqtt
import requests
import time
import json
import random
import ssl

port = 1883 # default port
Server_ip = "broker.netpie.io" 

Alias = "Pi"

Subscribe_Topic = "@msg/Laptop/Msg"
Publish_Topic = "@msg/Pi/Msg"

Client_ID = "bfbe9214-872f-4e3b-910a-15dc576ce93d"
Token = "cndGpgj2Tu8oA8QZvQmsUKRBEfED7vzk"
Secret = "nPKG5CD6ddontJgp8vwv7KAJFNskmGd8"

MqttUser_Pass = {"username":Token,"password":Secret}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Subscribe_Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    text=msg.payload.decode("utf-8")
    if text == "CLEAR":
        response = requests.get(url='http://0.0.0.0:6969/clearitems')

client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()

while True:
        time.sleep(2)

