#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from database import *


def readRepeater(RptID):

    cmdstr = "python3 /home/poller/getRefpeatersInfoSingle.py "
    cmdstr += str(RptID)
    cmdstr += " &"
#    print(cmdstr)
    os.system(cmdstr);
#    print("x")
  
  
  
  
  
        
# START OF CODE

#Read the balance ID to read
BalanceID = int(sys.argv[1])

if (BalanceID <= 0):
    print("Usage: getRefpeatersInfoCallSingle.py <balanceid> (ID is > 0)")
    sys.exit(0)

# Open MySQL Connection
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from refpeaters where Status = '1' and BalanceID = %s",[BalanceID])
repeatersrec = curloop.fetchall()

#Loop Through All Repeaters
for repeater in repeatersrec:
    readRepeater(repeater[0])
#    time.sleep(10)



cnx.close()
