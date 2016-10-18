# DstarTracker
DstarTracker is a project to read the status of d-star repeaters and keep a running history of repeater connections and conversations for metric and status reporting.

There are 2 parts to the project.  There is the backend poller which is written in python and then there is the frontend which uses the sencha Ext 6.x framework for the visual display.

## Python Backend

### Files
Here are the different versions of the files in this directory:

argtest.py                              Testing argument passing in python

getRefpeaterInfo.py                     This was the first test to try to get repeater data

getRefpeatersInfoCallSingle.py          This is the current starting poller, it loops through all
                                        repeaters and starts a new process to poll for each

getRefpeaterInfoSerial.py               This will get data from each repeater one at a time serially.
                                        All code is in this one file.

getRefpeatersInfoSingle.py              This is the script that getRefpeatersInfoCallSingle.py calls
                                        to do the work.

getRefpeatersInfothread.py              This is an attempt at a threaded version of getRefpeaterInfoSerial.py

scrapetest.py.workingcopy               This was the learning on how to scrape data from web pages.
