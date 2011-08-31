#!/usr/bin/env python
# coding: utf-8

#
# Logentries Python monitoring agent
# Copyright 2010,2011 Logentries, Jlizard
# Mark Lacomber <marklacomber@gmail.com>
#

VERSION = "1.0"

import logging
from google.appengine.api import taskqueue

class PushQueue(logging.Handler):

    def __init__(self, key, location):

        logging.Handler.__init__(self)
        self.addr = 'https://api.logentries.com/%s/hosts/%s/?realtime=1' %(key, location)
	format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
	self.setFormatter(format)
  

    def send(self, msg):

        taskqueue.add(url='/logentriesworker', params={'msg':msg, 'addr':self.addr})


    def handleError(self, record):
        pass


    def emit(self, record):

	msg = self.format(record)
        self.send(msg+'\n')


    def flush(self):
	pass

    def close(self):

        logging.Handler.close(self)
