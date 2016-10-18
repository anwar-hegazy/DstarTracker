#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta
from database import *



#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("DELETE from RefpeaterConnectedImport where handled = '1'")
curloop.execute("DELETE from RefpeaterConnectionsImport where Handled = '1'")
curloop.execute("DELETE from OpIssues where Handled = '1'")
curloop.execute("DELETE from LastHeardImport where Handled = '1'")


cnx.commit()

cnx.close()
