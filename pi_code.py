from gpiozero import LED, Button
from datetime import datetime
import time
import paho.mqtt.publish as publish # pip3 install paho-mqtt
import paho.mqtt.client as mqtt

PUL = LED(9)
DIR = LED(10)
ENA = LED(11)
button = Button(24)
LMR = Button(26)
LML = Button(27)

def calibrate():
    DIR.on()
    ENA.on()
    while not LMR.is_pressed:
        PUL.blink(0.008, 0.008,1, False)
    time1 = datetime.now()

    DIR.off()
    while not LML.is_pressed:
        PUL.blink(0.008, 0.008,1, False)
    time2 = datetime.now()

    diff = (time2 - time1).total_seconds()

    DIR.off()
    return diff

diff = calibrate()
print(diff)

def on_button_pressed():
    data_out = 'CLEAR'
    client.publish(Publish_Topic, data_out, retain= True)



global time_ran
time_ran = 0
global target_time
target_time = diff

def item_found():
    global target_time
    global diff
    target_time += diff + 5
    print(f'Found another item, current target time {target_time}')
    time.sleep(0.8)
    
def belt_control():
    global time_ran
    global target_time
    time1 = datetime.now()
    time2 = datetime.now()
    interval = 0
    while time_ran+interval <= (target_time):
        PUL.blink(0.008, 0.008,1, False)
        time2 = datetime.now()
        interval = (time2 - time1).total_seconds()
    time_ran += interval
    print(f'all items reached end of belt, time ran {time_ran}')

button.when_pressed = on_button_pressed
LMR.when_pressed = item_found

port = 1883 # default port
Server_ip = "broker.netpie.io" 

Alias = "Laptop"

Subscribe_Topic = "@msg/Pi/Msg"
Publish_Topic = "@msg/Laptop/Msg"

Client_ID = "9d0bf5ff-4c52-4c4c-adfd-e46661c31a89"
Token = "88FiMbPTC4NFjqBcbyCMCzmP1XjT3A27"
Secret = "sP9y2Tsu23pWsZhL2ZH8SjF1sBdzFPSQ"

MqttUser_Pass = {"username":Token,"password":Secret}
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=Client_ID, clean_session=True)
client.username_pw_set(Token,Secret)
client.connect(Server_ip, port)
client.loop_start()

try:
    while True:
        # DIR.off()
        # ENA.on()
        # PUL.blink(0.008, 0.008,1, False)
        belt_control()
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:    
    ENA.off()
