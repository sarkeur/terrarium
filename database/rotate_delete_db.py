## remove old values in database IMPORT ##
import MySQLdb
import time

from time import sleep

## FUNCTIONS ##
def clean_db():
    db = MySQLdb.connect(host="localhost",user="root",passwd="nairolfuaebel", db="terrarium")
    cursor = db.cursor()
    try:
       cursor.execute("""DELETE FROM temperature
                         WHERE date_mesure < DATE_SUB(NOW(), INTERVAL 1 MONTH)""")
       db.commit()
    except:
       db.rollback()
    db.close()

#### MAIN ####
print ("\n=========================================================================\n")
print (" Start script \"rotate_delete_db.py\"")
print ("\n=========================================================================\n")

sleep(60)

while(1):
    clean_db()
    sleep(3600)

