#!/usr/bin/python3

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import mysql.connector
import sys
import time

def getHTML(url):
    try:
        html = urlopen(url)
    except Exception:
        print("Error opening webpage")
        return None

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
    except AttributeError as e:
        print("Error decoding web content")
        return None

    return bsObj


def getLinkedTo(bsObj):
    try:
       pData = bsObj.findAll("span",{"class":"style1"},True,"Linked to")[0].parent.parent.find_next_siblings("tr")
       cur = cnx.cursor()
       for child in pData:
           tdarray = child.findAll("td")
           module = tdarray[0].span.get_text()
           linkedto = tdarray[1].span.get_text()
           #print (module, linkedto)
           cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, module, linkedto))


    except Exception:
            print("Error Retrieving linked to repeater data")
            return None

    cnx.commit()
    return 1


def getRepeaterLinkedTo(bsObj):

    try:
        pData = bsObj.findAll("span",{"class":"style1"},True,"Module A")[0].parent.parent.find_next_siblings("tr")
        for child in pData:
            tdarray = child.findAll("td")
            modulea = tdarray[0].span.get_text()
            moduleb = tdarray[1].span.get_text()
            modulec = tdarray[2].span.get_text()
            moduled = tdarray[3].span.get_text()
            modulee = tdarray[4].span.get_text()
            #print (modulea, moduleb, modulec, moduled, modulee)
            cur = cnx.cursor()
            cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, 'A', modulea))
            cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, 'B', moduleb))
            cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, 'C', modulec))
            cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, 'D', moduled))
            cur.execute("INSERT Into RefpeaterConnectionsImport (RefpeaterID, Port, Destination, Handled) VALUES (%s, %s, %s, '0')",(1, 'E', modulee))

    except Exception:
            print("Error Retrieving linked to repeater data")
            return None

    cnx.commit()
    return 1


def getConnected(bsObj):

    try:
        pData = bsObj.findAll("span",{"class":"style1"},True,"Type")[0].parent.parent.find_next_siblings("tr")
        for child in pData:
            tdarray = child.findAll("td")
            callsign = tdarray[0].span.get_text()
            text = tdarray[1].span.get_text()
            port = tdarray[2].span.get_text()
            ctype = tdarray[3].span.get_text()
            #print (callsign, text, port, ctype)
            cur = cnx.cursor()
            cur.execute("INSERT Into RefpeaterConnectedImport (RefpeaterID, Callsign, UserMessage, LastTX, Type, Handled) VALUES (%s, %s, %s, %s, %s, '0')",(1, callsign, text, port, ctype))


    except Exception:
            print("Error Retrieving repeater connected data")
            return None

    cnx.commit()
    return 1

def getLastHeard(bsObj):

    try:
        pData = bsObj.findAll("span",{"class":"style1"},True,"Time")[0].parent.parent.find_next_siblings("tr")
        for child in pData:
            tdarray = child.findAll("td")
#           callsign = tdarray[0].strong.get_text()
            callsign = tdarray[0].span.get_text()
            text = tdarray[1].span.get_text()
            port = tdarray[2].span.get_text()
            lastheard = tdarray[3].span.get_text()
            #print (callsign, text, port, lastheard)
            cur = cnx.cursor()
            cur.execute("INSERT Into LastHeardImport (RefpeaterID, Port, Callsign, CommentText, LastHeard, Lat, Lon, Handled) VALUES (%s, %s, %s, %s, %s, '0', '0', '0')",(1, port, callsign, text, lastheard))
#            cur.execute("INSERT Into LastHeardHistory (RefpeaterID, Port) VALUES ('1', '2')")


    except Exception:
            print("Error Retrieving repeater Last Heard data")
            return None

    cnx.commit()
    return 1

def readRepeater(RptID, URL, rType):

    if (URL == ""):
        print("Invalid Repeater ID")
        sys.exit(0)

    print("Reading Repeater: ", URL)
    
    bsObj = getHTML(URL)
    if (bsObj == None):
        print("Unable To Read Repeater: ", URL)
        curerror = cnx.cursor()
        curerror.execute("INSERT into OpIssues (RefpeaterID, Status, LogDateTime, Description) VALUES (%s, '1', %s, 'Unable To Access Repeater Web Interface')",(RptID, time.strftime('%Y-%m-%d %H:%M:%S')))
        cnx.commit()
    else:
        if (rType == 1):
            print("Repeater Type: Repeater")
            st = getLinkedTo(bsObj)
        else:
            print("Repeater Type: Reflector")
            st = getRepeaterLinkedTo(bsObj)
   
        if (st == None):
            curerror = cnx.cursor()
            curerror.execute("INSERT into OpIssues (RefpeaterID, Status, LogDateTime, Description) VALUES (%s, '2', %s, 'No Linked Data Returned')",(RptID, time.strftime('%Y-%m-%d %H:%M:%S')))
            cnx.commit()

        st = getConnected(bsObj)
        if (st == None):
            curerror = cnx.cursor()
            curerror.execute("INSERT into OpIssues (RefpeaterID, Status, LogDateTime, Description) VALUES (%s, '3', %s, 'No Connected Data Returned')",(RptID, time.strftime('%Y-%m-%d %H:%M:%S')))
            cnx.commit()

    
        st = getLastHeard(bsObj)
        if (st == None):
            curerror = cnx.cursor()
            curerror.execute("INSERT into OpIssues (RefpeaterID, Status, LogDateTime, Description) VALUES (%s, '4', %s, 'No Last Heard Data Returned')",(RptID, time.strftime('%Y-%m-%d %H:%M:%S')))
            cnx.commit()

  
  
  
  
  
        
# START OF CODE

#Read the balance ID to read
BalanceID = int(sys.argv[1])

if (BalanceID <= 0):
    print("Usage: getRefpeatersInfo.py <balanceid> (ID is > 0)")
    sys.exit(0)

# Open MySQL Connection
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar')

# Read repeaters in the current balance ID
curloop = cnx.cursor()
curloop.execute("SELECT * from refpeaters where Status = '1' and BalanceID = %s",[BalanceID])
repeatersrec = curloop.fetchall()

#Loop Through All Repeaters
for repeater in repeatersrec:
    readRepeater(repeater[0], repeater[2], repeater[3])



cnx.close()
