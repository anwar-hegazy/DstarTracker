#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta
from database import *


def releaseRepeater(rptid):
    cur = cnx.cursor()
    cur.execute("UPDATE refpeaters set Status='1' where uid=%s",[rptid])
    print("Repeater ID: ", rptid)


#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from refpeaters where NextStatusCheck < %s and Status <> '1'",[time.strftime('%Y-%m-%d %H:%M:%S')])
repeatersrec = curloop.fetchall()

for repeater in repeatersrec:
    releaseRepeater(repeater[0])

cnx.commit()

cnx.close()
