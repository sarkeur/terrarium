# Import modules
import RPi.GPIO as GPIO
import time
import json
import sys
import logging

from logging.handlers import RotatingFileHandler

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
GPIO.setup(CablePin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(CeramicPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(NeonPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IncandescentPin, GPIO.OUT, initial=GPIO.HIGH)

# create a rotating log
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
# add a rotating handler
handler = RotatingFileHandler("log.log", maxBytes=200000, backupCount=1)
logger.addHandler(handler)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
	# Read JSON file
	### Get current time ###
	Year = time.strftime("%Y")
	MonthDay = time.strftime("%m%d")
	HourMinute = time.strftime("%H%M")
	
	print ("Year: " + Year)
	print ("MonthDay: " + MonthDay)
	print ("HourMinute: " + HourMinute)
	
	### Open calendar ###
	try:
    	    CalendarFile = json.load(open("data/calendar.json"))
	except:
    	     print("Failed to Read json calendar file")
	     sys.exit(0)
	
        ### Get calendar name ###
        if CalendarFile.has_key('name'):
            print("Reading calendar: " + CalendarFile['name'])
        else: 
            print("Reading unnamed calendar")
	
        ### Get time parameters ###
        if CalendarFile.has_key(MonthDay):
            for MonthDayArray in CalendarFile[MonthDay]:
                if MonthDayArray.has_key("rise"):
                    Sunrise = MonthDayArray["rise"]
                    print("Sunrise: " + Sunrise)
                else:
                    print("ERROR: no sunrise for this day")
                if MonthDayArray.has_key("set"):
                    Sunset = MonthDayArray["set"]
                    print("Sunset: " + Sunset)
                else:
                    print("ERROR: no sunset for this day")  
                if MonthDayArray.has_key("length"):
                    DayLength = MonthDayArray["length"]
                    print("DayLength: {} minutes = {}h{}".format(DayLength, DayLength/60, DayLength%60))
                else:
                    print("ERROR: no sunset for this day")
        else: 
            print("ERROR : impossible to read MonthDay in the calendar")

        ### get temperature ###
	tempfile = open(TerraLowSensor)
	thetext = tempfile.read()
	tempfile.close()
	tempdata = thetext.split("\n")[1].split(" ")[9]
	TerraLowTemp = float(tempdata[2:])/1000
	print ("TerraLowTemp = %.1f" %(TerraLowTemp))

        tempfile = open(TerraColdSensor)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        TerraColdTemp = float(tempdata[2:])/1000
	print ("TerraColdTemp = %.1f" %(TerraColdTemp))

        tempfile = open(TerraWarmSensor)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        TerraWarmTemp = float(tempdata[2:])/1000
        print ("TerraWarmTemp = %.1f" %(TerraWarmTemp))

        tempfile = open(RaspberrySensor)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        RaspberryTemp = float(tempdata[2:])/1000
        print ("RaspberryTemp = %.1f" %(RaspberryTemp))

        tempfile = open(RoomSensor)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        RoomTemp = float(tempdata[2:])/1000
        print ("RoomTemp = %.1f" %(RoomTemp))

        ### Check day / night ###
        if Sunrise <= HourMinute <= Sunset:
            DayStatus = "day"
        else:
            DayStatus = "night"
            
        print ("DayStatus: " + DayStatus)

        ### Neon && Incandescent lamp ###
        if DayStatus == "day":
            GPIO.output(NeonPin, GPIO.LOW)
	    GPIO.output(IncandescentPin, GPIO.LOW)
            print("Neon on")
            print("Incandescent lamp on")
        else:
            GPIO.output(NeonPin, GPIO.HIGH)
	    GPIO.output(IncandescentPin, GPIO.HIGH)
            print("Neon off")
            print("Incandescent lamp off")

        ### Ceramic lamp ###
        if DayStatus == "day":
            if TerraLowTemp < 24 or TerraColdTemp < 26 or TerraWarmTemp < 34:
		GPIO.output(CeramicPin, GPIO.LOW)
                print("Ceramic lamp on")
            else:
		GPIO.output(CeramicPin, GPIO.HIGH)
                print("Ceramic lamp off")
        else:
            if TerraLowTemp < 21 or TerraColdTemp < 21 or TerraWarmTemp < 21:
                GPIO.output(CeramicPin, GPIO.LOW)
		print("Ceramic lamp on")
            else:
                GPIO.output(CeramicPin, GPIO.HIGH)
		print("Ceramic lamp off")
            
        ### Heating cable ###
        if DayStatus == "day":
            if TerraLowTemp < 24:
                GPIO.output(CablePin, GPIO.LOW)
		print("Heating cable on")
            else:
                GPIO.output(CablePin, GPIO.HIGH)
		print("Heating cable off")
        else:
            if TerraLowTemp < 21:
                GPIO.output(CablePin, GPIO.LOW)
		print("Heating cable on")
            else:
		GPIO.output(CablePin, GPIO.HIGH)
                print("Heating cable off")

	# log informations
	logger.info('time=%s%s%s; '
                    'TerraLowTemp=%.1f; '
                    'TerraColdTemp=%.1f; '
                    'TerraWarmTemp=%.1f; '
                    'RaspberryTemp=%.1f; '
                    'RoomTemp=%.1f; '
                    %(Year,MonthDay,HourMinute,
		    TerraLowTemp,
                    TerraColdTemp,
		    TerraWarmTemp,
		    RaspberryTemp,
	            RoomTemp)
                    ) 

        time.sleep(15)
### Cleanup all GPIO ###
# If CTRL+C is pressed, exit cleanly:
except KeyboardInterrupt: 
    GPIO.cleanup()
