#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta



def updateImportList(uid):
    currep = cnx.cursor()
    currep.execute("UPDATE RefpeaterConnectedImport set handled=1 where uid = %s", [uid])



def insertNewConnectedRecord(RefpeaterID, CallSignID, UserMessage, LastTX, Type):
    currep = cnx.cursor()
    currep.execute("INSERT into RefpeaterConnected (RefpeaterID, CallsignID, UserMessage, LastTX, Type) VALUES (%s, %s, %s, %s, %s)", (RefpeaterID, CallSignID, UserMessage, LastTX, Type)) 
    


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


def GetNextListValue(ListID):
    currep2 = cnx.cursor()
    currep2.execute("SELECT * from ListItems where ListID=%s order by ValueInt1 DESC LIMIT 1", [ListID])
    listrec = currep2.fetchone()
    try:
        newid = int(listrec[3]) + 1
    except TypeError:
       newid = 1

    return newid    


def getLastTX(TXTxt):

    currep3 = cnx.cursor()
    currep3.execute("SELECT * from ListItems where ListID=3 and Name = %s LIMIT 1", [TXTxt])
    Callsignrec = currep3.fetchone()

    if (currep3.rowcount <= 0):
        NewValue = GetNextListValue(3)
        currep3.execute("INSERT into ListItems (ListID, Name, ValueInt1) VALUES ('3', %s, %s)", (TXTxt, NewValue))
        cnx.commit()
        currep3.execute("SELECT * from ListItems where ListID = 3 and Name = %s LIMIT 1", [TXTxt])
        Callsignrec = currep3.fetchone()

#    print(Callsignrec)
    return Callsignrec[3]


def getTypeID(TypeTxt):

    currep = cnx.cursor()
    currep.execute("SELECT * from ListItems where ListID=4 and Name = %s LIMIT 1", [TypeTxt])
    Callsignrec = currep.fetchone()

#    print(currep.rowcount)
    if (currep.rowcount <= 0):
#        print("Inserting TypeID: ", TypeTxt)
        NewValue = GetNextListValue(4)
        currep.execute("INSERT into ListItems (ListID, Name, ValueInt1) VALUES ('4', %s, %s)", (TypeTxt, NewValue))
        cnx.commit()
        currep.execute("SELECT * from ListItems where ListID = 4 and Name = %s LIMIT 1", [TypeTxt])
        Callsignrec = currep.fetchone()

    return Callsignrec[3]




#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar')

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from RefpeaterConnectedImport where handled = '0' order by RefpeaterID")
connectedrec = curloop.fetchall()

CurrentRefpeaterID = -1;

#Loop Through All Repeaters
for connection in connectedrec:
    if (CurrentRefpeaterID != connection[1]):
       curdel = cnx.cursor()
       curdel.execute("Delete from RefpeaterConnected where RefpeaterID=%s",[connection[1]])
       CurrentRefpeaterID = connection[1]

    CallsignID = getCallsignID(connection[7])
    LastTXID = getLastTX(connection[5])
    TypeID = getTypeID(connection[6])

    insertNewConnectedRecord(connection[1], CallsignID, connection[4], LastTXID, TypeID)

    updateImportList(connection[0])

cnx.commit()

cnx.close()
