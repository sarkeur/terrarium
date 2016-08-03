# Import modules
import RPi.GPIO as GPIO
import time
import json
import sys

### Pin definition ###
TerraLowSensor = "/sys/bus/w1/devices/28-0115921b25ff/w1_slave"
TerraColdSensor = "/sys/bus/w1/devices/28-0115921c81ff/w1_slave"
TerraWarmSensor = "/sys/bus/w1/devices/28-0115921d29ff/w1_slave"
RaspberrySensor = "/sys/bus/w1/devices/28-01159230eaff/w1_slave"
RoomSensor = "/sys/bus/w1/devices/28-0115923492ff/w1_slave"

CablePin = 15
CeramicPin = 17
NeonPin = 18
IncandescentPin = 27

### Pin setup ###
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
# inputs
# outputs
GPIO.setup(CablePin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(CeramicPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(NeonPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IncandescentPin, GPIO.OUT, initial=GPIO.LOW)

# Read JSON file

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        print("on")
        GPIO.output(NeonPin, GPIO.HIGH)
	GPIO.output(IncandescentPin, GPIO.HIGH)
	GPIO.output(CeramicPin, GPIO.HIGH)
	GPIO.output(CablePin, GPIO.HIGH)

	time.sleep(10)

	print("off")
        GPIO.output(NeonPin, GPIO.LOW)
	GPIO.output(IncandescentPin, GPIO.LOW)
        GPIO.output(CeramicPin, GPIO.LOW)
        GPIO.output(CablePin, GPIO.LOW)
        
        time.sleep(10)
### Cleanup all GPIO ###
# If CTRL+C is pressed, exit cleanly:
except KeyboardInterrupt: 
    GPIO.cleanup()
