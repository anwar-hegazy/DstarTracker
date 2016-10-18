#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta


def insertRefpeater(Callsign, URL):

    currep = cnx.cursor()
    currep.execute("insert into refpeaters (CallSign, URL, Type, Status, BalanceID, OpStatus, NextStatusCheck, AddMethod) VALUES (%s,%s,1,1,1,1,'2015-01-01 00:00:00',1);", (Callsign, URL))


def getCallsign(CallSignID):
    currep = cnx.cursor()
    currep.execute("SELECT * from CallSigns where uid = %s LIMIT 1", [CallSignID])
    Callsignrec = currep.fetchone()

    return Callsignrec[1]




#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar')

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from RefpeaterConnections")
connectedrec = curloop.fetchall()

#Loop Through All Repeaters
for connection in connectedrec:

    Callsign = getCallsign(connection[3])
    URL = "http://"
    URL += Callsign.strip()
    URL += ".dstargateway.org"

    curcheck = cnx.cursor()
    curcheck.execute("Select * from refpeaters where CallSign=%s",[Callsign])
    CheckRecord = curcheck.fetchall()

    if (curcheck.rowcount <= 0):
        insertRefpeater(Callsign, URL)
        print(Callsign, URL)


cnx.commit()

cnx.close()
