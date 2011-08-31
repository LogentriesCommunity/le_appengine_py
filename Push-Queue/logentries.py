#!/usr/bin/env python
# coding: utf-8

#
# Logentries Python monitoring agent
# Copyright 2010,2011 Logentries, Jlizard
# Mark Lacomber <marklacomber@gmail.com>
#

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue

import logging

def init(key, location):
	if len(logging.getLogger('').handlers) <= 1:
		logging.getLogger('').addHandler(PushQueue(key, location))


class PushQueue(logging.Handler):

    def __init__(self, key, location):

        logging.Handler.__init__(self)
        self.addr = 'https://api.logentries.com/%s/hosts/%s/?realtime=1' %(key, location)
	format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
	self.setFormatter(format)
  

    def send(self, msg):

        taskqueue.add(queue_name='logentries-push-queue', url='/logentriesworker', params={'msg':msg, 'addr':self.addr})


    def handleError(self, record):
        pass


    def emit(self, record):

	msg = self.format(record)
        self.send(msg+'\n')


    def flush(self):
	pass

    def close(self):

        logging.Handler.close(self)


class LogentriesWorker(webapp.RequestHandler):

   	def post(self):
      		rpc = urlfetch.create_rpc()
      		msg = self.request.get('msg')
      		addr = self.request.get('addr')
      		urlfetch.make_fetch_call(rpc, addr, payload = msg, method=urlfetch.PUT, headers={'content-length':str(len(msg))})
		self.response.set_status(200)


