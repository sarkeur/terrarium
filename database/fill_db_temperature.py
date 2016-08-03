## rempli la base de donnee avec les temperatures IMPORT ##
import MySQLdb 
import time 

from time import sleep

### Pin definition ###
TerraLowSensor = "/sys/bus/w1/devices/28-0115921b25ff/w1_slave"
TerraColdSensor = "/sys/bus/w1/devices/28-0115921c81ff/w1_slave"
TerraWarmSensor = "/sys/bus/w1/devices/28-0115921d29ff/w1_slave"
RaspberrySensor = "/sys/bus/w1/devices/28-01159230eaff/w1_slave"
RoomSensor = "/sys/bus/w1/devices/28-0115923492ff/w1_slave"

## FUNCTIONS ##
def dump_db(TerraLowTemp, TerraColdTemp, TerraWarmTemp, Roomtemp, RaspberryTemp):
    db = MySQLdb.connect(host="localhost",user="root",passwd="nairolfuaebel", db="terrarium")
    cursor = db.cursor()
    try:
       cursor.execute("""INSERT INTO temperature
                         VALUES(CURRENT_TIMESTAMP,%s,%s,%s,%s,%s)""",
                     (TerraLowTemp,
                      TerraColdTemp,
                      TerraWarmTemp,
                      RoomTemp,
                      RaspberryTemp))
       db.commit()
    except:
       db.rollback()
    db.close()

#### MAIN ####
print ("\n=========================================================================\n") 
print (" Start script \"fill_db_temperature.py\"") 
print ("\n=========================================================================\n") 
sleep(60)
while(1):
    ### get temperature ###
    tempfile = open(TerraLowSensor)
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    TerraLowTemp = float(tempdata[2:])/1000

    tempfile = open(TerraColdSensor)
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    TerraColdTemp = float(tempdata[2:])/1000

    tempfile = open(TerraWarmSensor)
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    TerraWarmTemp = float(tempdata[2:])/1000

    tempfile = open(RaspberrySensor)
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    RaspberryTemp = float(tempdata[2:])/1000

    tempfile = open(RoomSensor)
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    RoomTemp = float(tempdata[2:])/1000

    dump_db(TerraLowTemp, TerraColdTemp, TerraWarmTemp, RoomTemp, RaspberryTemp)
    sleep(60)
