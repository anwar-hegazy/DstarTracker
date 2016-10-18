#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta
from database import *



def updateImportList(uid):
    currep = cnx.cursor()
    currep.execute("UPDATE RefpeaterConnectionsImport set Handled=1 where uid = %s", [uid])



def insertNewConnectionRecord(RefpeaterID, Port, DestinationID, DestinationPorts):
    currep = cnx.cursor()
    currep.execute("INSERT into RefpeaterConnections (RefpeaterID, Port, DestinationID, DestinationPort) VALUES (%s, %s, %s, %s)", (RefpeaterID, Port, DestinationID, DestinationPorts)) 
    #print("Destination Port Set To: ", DestinationPorts)
    


def updateRepeater(RefpeaterID):
    currep = cnx.cursor()
    currep.execute("Update refpeaters set OpStatus=1, LastStatus=1, LastPoll=%s where uid=%s", (time.strftime('%Y-%m-%d %H:%M:%S') , RefpeaterID)) 



def getCallsignID(CallSign):
    currep = cnx.cursor()
    currep.execute("SELECT * from CallSigns where CallSign = %s LIMIT 1", [CallSign[:6]])
    Callsignrec = currep.fetchone()

#    print(currep.rowcount)
    if (currep.rowcount <= 0):
#        print("Inserting new callsign:", CallSign[:6])
        currep.execute("INSERT into CallSigns (CallSign) VALUES (%s)", [CallSign[:6]])
        cnx.commit()
#        print("looking up new callsign")
        currep.execute("SELECT * from CallSigns where CallSign = %s LIMIT 1", [CallSign[:6]])
        Callsignrec = currep.fetchone()

    return Callsignrec[0]




#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from RefpeaterConnectionsImport where handled = '0' order by RefpeaterID")
connectedrec = curloop.fetchall()

CurrentRefpeaterID = -1;

#Loop Through All Repeaters
for connection in connectedrec:
    if (CurrentRefpeaterID != connection[1]):
       curdel = cnx.cursor()
       curdel.execute("Delete from RefpeaterConnections where RefpeaterID=%s",[connection[1]])
       CurrentRefpeaterID = connection[1]

    CallsignID = getCallsignID(connection[3])
    DestinationID = connection[3][7:]
    #print(connection[3][7:])

    if (DestinationID != 'd') and (DestinationID != ""):
        insertNewConnectionRecord(connection[1], connection[2], CallsignID, DestinationID)

    updateImportList(connection[0])
    updateRepeater(connection[1])

cnx.commit()

cnx.close()
