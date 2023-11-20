from gpiozero import LED, Button
from datetime import datetime
import time
from picamera import PiCamera

PUL = LED(9)
DIR = LED(10)
ENA = LED(11)
LMR = Button(26)
LML = Button(27)
cam = PiCamera()

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

DIR.on()
time1 = datetime.now()
time2 = datetime.now()
while (time2 - time1).total_seconds() <= (diff/2 - 1.2):
	PUL.blink(0.008, 0.008,1, False)
	time2 = datetime.now()

cam.start_preview()
time.sleep(5)
cam.capture('/home/pi/Desktop/g.jpg')
cam.stop_preview()