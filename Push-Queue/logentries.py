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
from google.appengine.runtime import apiproxy_errors

import logging
import sys

def init(key, location):
    if len(logging.getLogger('').handlers) <= 1:
        logging.getLogger('').addHandler(PushQueue(key, location))

class LogentriesWorker(webapp.RequestHandler):

    def post(self):
        rpc = urlfetch.create_rpc()
        msg = self.request.get('msg')
        addr = self.request.get('addr')
        try:
            urlfetch.make_fetch_call(rpc, addr, payload = msg, method=urlfetch.PUT, headers={'content-length':str(len(msg))})
            # for debugging, enable this:
            # result = urlfetch.fetch(addr, payload = msg, method=urlfetch.PUT, headers={'content-length':str(len(msg))})
            # if result.status_code != 200:
            #     logging.error("%r", result.content)
        except apiproxy_errors.OverQuotaError, message:
            sys.stderr.write(message + '\n')
            sys.stderr.write("URLFetch API Quota reached, unable to transmit logs to Logentries\n")


class PushQueue(logging.Handler):

    def __init__(self, key, location):

        logging.Handler.__init__(self)
        self.addr = 'https://api.logentries.com/%s/hosts/%s/?realtime=1' %(key, location)
        format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
        self.setFormatter(format)


    def send(self, msg):
        try:
            taskqueue.add(queue_name='logentries-push-queue', url='/logentriesworker', params={'msg':msg, 'addr':self.addr})
        except apiproxy_errors.OverQuotaError, message:
            sys.stderr.write(message + '\n')
            sys.stderr.write("TaskQueue API Quota reached, unable to transmit logs to Logentries\n")

    def handleError(self, record):
        pass

    def emit(self, record):
        msg = self.format(record)
        self.send(msg+'\n')

    def flush(self):
        pass

    def close(self):
        logging.Handler.close(self)
