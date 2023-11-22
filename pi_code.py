from gpiozero import LED, Button
from datetime import datetime
import time
import paho.mqtt.publish as publish # pip3 install paho-mqtt
import paho.mqtt.client as mqtt
from config import pi_Client_ID,pi_Secret,pi_Token
PUL = LED(9) # PULSE pin
DIR = LED(10) # DIRECTION pin, off for forward, on for backwards
ENA = LED(11) # ENABLE pin for motor driver
button = Button(24) # Order clear button
LMR = Button(26) # light sensor right
LML = Button(27) # light sensor left

def calibrate():
    '''
    Calibration process for the conveyor belt, 
    returns the time it takes for the belt to move through 1 length
    '''
    DIR.on()
    ENA.on()
    while not LMR.is_pressed: # rear edge of the belt
        PUL.blink(0.008, 0.008,1, False)
    time1 = datetime.now()

    DIR.off()
    while not LML.is_pressed: # front edge of the belt
        PUL.blink(0.008, 0.008,1, False)
    time2 = datetime.now()
    
    # calculate time it takes
    diff = (time2 - time1).total_seconds()

    DIR.off()
    return diff

diff = calibrate()
print(diff)

def on_button_pressed():
    '''
    Callback function for when the clear order button is pressed
    '''
    data_out = 'CLEAR'
    client.publish(Publish_Topic, data_out, retain= True)

global time_ran
time_ran = 0 # used for tracking time the belt has been running
global target_time
target_time = 7 # used to set the target time for the belt to run

def item_found():
    '''
    Callback function for when new item has been placed on the belt
    '''
    global target_time
    global diff
    target_time += diff + 5
    print(f'Found another item, current target time {target_time}')
    time.sleep(0.8)
    
def belt_control():
    '''
    Infinite loop function to control the conveyor belt movement
    '''
    global time_ran
    global target_time
    time1 = datetime.now()
    time2 = datetime.now()
    interval = 0
    while time_ran+interval <= (target_time):
        # runs the belt until the target time is reached
        PUL.blink(0.008, 0.008,1, False)
        time2 = datetime.now()
        interval = (time2 - time1).total_seconds()
    time_ran += interval
    print(f'all items reached end of belt, time ran {time_ran}')

button.when_pressed = on_button_pressed # connects the button event to the callback function
LMR.when_pressed = item_found # connects the light sensor event to the callback function

port = 1883 # default port
Server_ip = "broker.netpie.io" 

Alias = "Laptop"

Subscribe_Topic = "@msg/Pi/Msg"
Publish_Topic = "@msg/Laptop/Msg"

Client_ID = pi_Client_ID
Token = pi_Token
Secret = pi_Secret

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
