#!/usr/bin/env python
# coding: utf-8

#
# Logentries Python monitoring agent
# Copyright 2010,2011 Logentries, Jlizard
# Mark Lacomber <marklacomber@gmail.com>
#

VERSION = "1.0"

import logging, random
from google.appengine.api import taskqueue

def init(key, location):
	if len(logging.getLogger('').handlers) <= 1:
		logging.getLogger('').addHandler(PullQueue(key, location))

class PullQueue(logging.Handler):

    def __init__(self, key, location):

        logging.Handler.__init__(self)
        self.addr = '%s/hosts/%s' %(key, location)
	self.queue = taskqueue.Queue('logentries-pull-queue')
	format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
	self.setFormatter(format)


    def send(self, msg):
	try:
		task = taskqueue.Task(method='PULL', name = str(random.randrange(1,10000000000)), params={'msg':msg, 'addr':self.addr})
		self.queue.add(task)
	except apiproxy_errors.OverQuotaError, message:
		logging.error(message)
		logging.error("URLFetch API Quota reached, unable to transmit logs to Logentries") 


    def handleError(self, record):
        pass


    def emit(self, record):

	msg = self.format(record)
        self.send(msg+'\n')


    def flush(self):
	pass

    def close(self):

        logging.Handler.close(self)


