#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta



def updateHandled(uid):
    currep = cnx.cursor()
    currep.execute("UPDATE LastHeardImport set Handled=1 where uid = %s", [uid])



def insertNewLastHeard(RefpeaterID, CallSignID, UserMessage, LastHeardTime, Port, Lat, Lon):
    currep = cnx.cursor()
    currep.execute("INSERT into LastHeardHistory (RefpeaterID, CallsignID, CommentText, LastHeard, Port, Lat, Lon) VALUES (%s, %s, %s, %s, %s, %s, %s)", (RefpeaterID, CallSignID, UserMessage, LastHeardTime, Port, Lat, Lon)) 
    #print("CallSignID: ", CallSignID);
    


def LastHeardExists(RefpeaterID, CallSignID, UserMessage, LastHeardTime, Port):

    currep = cnx.cursor()
    currep.execute("SELECT * from LastHeardHistory where Refpeaterid = %s and CallsignID = %s and CommentText = %s and LastHeard = %s and Port = %s LIMIT 1", (RefpeaterID, CallSignID, UserMessage, LastHeardTime, Port))
    Callsignrec = currep.fetchone()

#    print(currep.rowcount)
    if (currep.rowcount <= 0):
        #print("No Match")
        return 0
    else:
        #print("Match Found")
        return 1


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
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar')

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from LastHeardImport where Handled = '0'")
heardrec = curloop.fetchall()

#Loop Through All Repeaters
for heardrec in heardrec:

    CallSignID = getCallsignID(heardrec[2])

    #check to see if this last heard already exists, if does just mark it as handled
    if (LastHeardExists(heardrec[1], CallSignID, heardrec[3], heardrec[4], heardrec[5]) != 1):
        insertNewLastHeard(heardrec[1], CallSignID, heardrec[3], heardrec[4], heardrec[5], heardrec[6], heardrec[7])
#        updateRefpeaterRecord(heardrec[1])

    updateHandled(heardrec[0])

cnx.commit()

cnx.close()
