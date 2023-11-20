import paho.mqtt.publish as publish # pip3 install paho-mqtt
import paho.mqtt.client as mqtt
import time
import json
import random
import ssl

port = 1883 # default port
Server_ip = "broker.netpie.io" 

Alias = "Laptop"

Subscribe_Topic = "@msg/Pi/Msg"
Publish_Topic = "@msg/Laptop/Msg"

Client_ID = "9d0bf5ff-4c52-4c4c-adfd-e46661c31a89"
Token = "88FiMbPTC4NFjqBcbyCMCzmP1XjT3A27"
Secret = "sP9y2Tsu23pWsZhL2ZH8SjF1sBdzFPSQ"

MqttUser_Pass = {"username":Token,"password":Secret}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Subscribe_Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(Subscribe_Topic)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()
time.sleep(1)
while True:
        data_out = input("Enter your message: ")
        client.publish(Publish_Topic, data_out, retain= True)