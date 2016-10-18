#!/usr/bin/python3

import mysql.connector
import sys
import os
import time
from datetime import datetime, timedelta



#### START OF CODE ####

# Open MySQL Connection
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar')

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("DELETE from RefpeaterConnectedImport where handled = '1'")
curloop.execute("DELETE from RefpeaterConnectionsImport where Handled = '1'")
curloop.execute("DELETE from OpIssues where Handled = '1'")
curloop.execute("DELETE from LastHeardImport where Handled = '1'")


cnx.commit()

cnx.close()
