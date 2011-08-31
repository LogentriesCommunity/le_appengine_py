#!/usr/bin/env python
# coding: utf-8

#
# Logentries Python monitoring agent
# Copyright 2010,2011 Logentries, Jlizard
# Mark Lacomber <marklacomber@gmail.com>
#

VERSION = "1.0"

import httplib, time
from google.appengine.api import taskqueue

class LogentriesBackend():

    def __init__(self):
        self.addr = 'api.logentries.com'
	self.conn = None
	self.makeConn()

    def makeConn(self):
	self.conn = httplib.HTTPSConnection('api.logentries.com')

    def send(self, msg, location):
	if self.conn is None:
		self.makeConn()
	addr = "/%s/?realtime=1" %(location)
        self.conn.request('PUT', addr, msg, headers={'content-length':str(len(msg))})
	result = self.conn.getresponse()

    def close(self):
	self.conn.close()


# CUSTOMIZABLE BUFFER TIMES
# The following values are presets on how often the backend should check for messages in the buffer
# and send them to Logentries. These are broken down into light, medium and heavy loads to try and 
# efficiently use the backend and thus incur less costs for cpu usage by avoiding overworking when 
# not necessary. They have been given some default values, if required, please change them to suit your needs.

# The maximum amount of messages to grab from the buffer at any time is 1000.
# The next-check values are based on different loads between 0 and 1000 messages in the buffer.

###  Times below are given in seconds!  ###

# NEXT CHECK IF BUFFER IS EMPTY
NO_TASK_SLEEP = 60

# NEXT CHECK IF LIGHT LOAD   I.E   BETWEEN 1 - 299 LOGS IN BUFFER
LIGHT_LOAD_SLEEP = 50

# NEXT CHECK IF MEDIUM LOAD  I.E   BETWEEN 300 - 799 LOGS IN BUFFER
MEDIUM_LOAD_SLEEP = 35

# NEXT CHECK IF HEAVY LOAD   I.E   BETWEEN 800 - 1000 LOGS IN BUFFER
HEAVY_LOAD_SLEEP = 10


# These are the minimum number of messages in buffer that define heavy and medium loads. 

###  Must be less than 1000  ###

MIN_HEAVY = 800

MIN_MEDIUM = 300

########################### End of Customizable Variables!

http = LogentriesBackend()

queue = taskqueue.Queue('logentries-pull-queue')    #  Must match name of queue as set in queue.yaml file

while True:
	tasks = queue.lease_tasks(60, 1000)

	if len(tasks) == 0:
		time.sleep(NO_TASK_SLEEP)
		continue

	fullList = []
	for task in tasks:
		params = task.extract_params()
		msg = params['msg']
		addr = params['addr']
		fullList.append(msg)
		queue.delete_tasks(task)
	finalSend = ''.join(fullList)
	http.send(finalSend, addr)

	if len(tasks) >= MIN_HEAVY:
		time.sleep(HEAVY_LOAD_SLEEP)
		continue
	elif len(tasks) >= MIN_MEDIUM:
		time.sleep(MEDIUM_LOAD_SLEEP)
		continue
	else:
		time.sleep(LIGHT_LOAD_SLEEP)
		continue
		





