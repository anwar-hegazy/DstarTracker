from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import mysql.connector
 
def getHTML(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("Error opening webpage")
        return None
         
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
    except AttributeError as e:
        print("Error decoding web content")
        return None
         
    return bsObj
 
     
def getLinkedTo(bsObj):
    pData = bsObj.findAll("span",{"class":"style1"},True,"Linked to")[0].parent.parent.find_next_siblings("tr")
    for child in pData:
        tdarray = child.findAll("td")
        module = tdarray[0].span.get_text()
        linkedto = tdarray[1].span.get_text()
        print (module, linkedto)
 
 
def getRepeaterLinkedTo(bsObj):
    pData = bsObj.findAll("span",{"class":"style1"},True,"Module A")[0].parent.parent.find_next_siblings("tr")
    for child in pData:
        tdarray = child.findAll("td")
        modulea = tdarray[0].span.get_text()
        moduleb = tdarray[1].span.get_text()
        modulec = tdarray[2].span.get_text()
        moduled = tdarray[3].span.get_text()
        modulee = tdarray[4].span.get_text()
        print (modulea, moduleb, modulec, moduled, modulee)
                 
 
def getConnected(bsObj):
    pData = bsObj.findAll("span",{"class":"style1"},True,"Type")[0].parent.parent.find_next_siblings("tr")
    for child in pData:
        tdarray = child.findAll("td")
        callsign = tdarray[0].span.get_text()
        text = tdarray[1].span.get_text()
        port = tdarray[2].span.get_text()
        ctype = tdarray[3].span.get_text()
        print (callsign, text, port, ctype)
                 
                 
def getLastHeard(bsObj):
    pData = bsObj.findAll("span",{"class":"style1"},True,"Time")[0].parent.parent.find_next_siblings("tr")
    for child in pData:
        tdarray = child.findAll("td")
#       callsign = tdarray[0].strong.get_text()
        callsign = tdarray[0].span.get_text()
        text = tdarray[1].span.get_text()
        port = tdarray[2].span.get_text()
        lastheard = tdarray[3].span.get_text()
        print (callsign, text, port, lastheard)
        cur = cnx.cursor()
        cur.execute("INSERT Into LastHeardImport (RefpeaterID, Port, Callsign, CommentText, LastHeard, Lat, Lon, Handled) VALUES (%s, %s, %s, %s, %s, '0', '0', '0')",(1, port, callsign, text, lastheard))
#        cur.execute("INSERT Into LastHeardHistory (RefpeaterID, Port) VALUES ('1', '2')")

    cnx.commit()

 
cnx = mysql.connector.connect(user='root', password='newday!',
                              host='127.0.0.1',
                              database='dstar') 
 
bsObj = getHTML("http://ref025.dstargateway.org")
if bsObj == None:
    print("Exiting with errors....")
else:
#   getLinkedTo(bsObj)
    getRepeaterLinkedTo(bsObj)
    print("-=-=-")
    getConnected(bsObj)
    print("-=-=-")
    getLastHeard(bsObj)
