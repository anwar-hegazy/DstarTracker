#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta
from database import *


def getRepeater(repeaterID):
    currep = cnx.cursor()
    currep.execute("SELECT * from refpeaters where uid = %s", [repeaterID])
    repeatersrec = currep.fetchone()

    return (repeatersrec[4], repeatersrec[8], repeatersrec[9], repeatersrec[2])



def updateRepeater(repeaterID, NewStatus, NextStatusCheck, LastPoll, newURL):

    currep = cnx.cursor()
    currep.execute("UPDATE refpeaters set Status=%s, LastStatus=%s, OpStatus=0, NextStatusCheck=%s, LastPoll=%s, URL=%s where uid = %s", ( NewStatus, NewStatus, NextStatusCheck, LastPoll, newURL, repeaterID))



def updateOpIssues(uid):

    currep = cnx.cursor()
    currep.execute("UPDATE OpIssues set Handled=1 where uid = %s", [uid])



def calculateNextTry(newstatus):
    
    if (newstatus == 2):	# 1 Minute
        NewTime = datetime.now() + timedelta(minutes=1)
        NewMinutes = 1
    elif (newstatus == 3):	# 2 Minutes
        NewTime = datetime.now() + timedelta(minutes=2)
        NewMinutes = 2
    elif (newstatus == 4): 	# 5 Minutes
        NewTime = datetime.now() + timedelta(minutes=5)
        NewMinutes = 5
    elif (newstatus == 5):	# 10 Minutes
        NewTime = datetime.now() + timedelta(minutes=10)
        NewMinutes = 10
    elif (newstatus == 6):	# 15 Minutes
        NewTime = datetime.now() + timedelta(minutes=15)
        NewMinutes = 15
    elif (newstatus == 7):	# 30 Minutes
        NewTime = datetime.now() + timedelta(minutes=30)
        NewMinutes = 30
    elif (newstatus == 8):	# 60 Minutes
        NewTime = datetime.now() + timedelta(hours=1)
        NewMinutes = 60
    elif (newstatus == 9):	# 120 Minutes
        NewTime = datetime.now() + timedelta(hours=2)
        NewMinutes = 120
    elif (newstatus == 10):	# 240 Minutes
        NewTime = datetime.now() + timedelta(hours=4)
        NewMinutes = 240
    elif (newstatus == 11):	# 480 Minutes
        NewTime = datetime.now() + timedelta(hours=8)
        NewMinutes = 480
    elif (newstatus == 12):	# 960 Minutes
        NewTime = datetime.now() + timedelta(hours=16)
        NewMinutes = 960
    else:			#1440 Minutes (24 hours)
        NewTime = datetime.now() + timedelta(hours=24)
        NewMinutes = 1440

    return NewTime.strftime('%Y-%m-%d %H:%M:%S')



#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from OpIssues where Handled = '0'")
repeatersrec = curloop.fetchall()

#Loop Through All Repeaters
for repeater in repeatersrec:
    RepeaterInfo = getRepeater(repeater[1])

#    print(repeater)
#    print(repeater[2])

    if (repeater[2] == 1) or (repeater[2] == 2):
        try:
            NewStatus = int(RepeaterInfo[2]) + 1
        except TypeError:
#            print("Assuming 2 minutes")
            NewStatus = 2

        URL = RepeaterInfo[3]
        if (RepeaterInfo[3][4] == ":"):
            URL = "https://"
            URL += RepeaterInfo[3][7:]
        else:
            URL = "http://"
            URL += RepeaterInfo[3][8:]
        if (NewStatus >= 13):		#maximum is 13 tries, if it goes over 13, flip from http to https
            NewStatus = 13

        NextStatusCheck = calculateNextTry(NewStatus)
#        print(URL)
        updateRepeater(repeater[1], NewStatus, NextStatusCheck, repeater[3], URL)

    updateOpIssues(repeater[0])

cnx.commit()

cnx.close()
