from google.appengine.ext import webapp
from google.appengine.api import urlfetch

import logging, le

def init(key, location):
	if len(logging.getLogger('').handlers) <= 1:
		logging.getLogger('').addHandler(le.PushQueue(key, location))


class LogentriesWorker(webapp.RequestHandler):

   	def post(self):
      		rpc = urlfetch.create_rpc()
      		msg = self.request.get('msg')
      		addr = self.request.get('addr')
      		urlfetch.make_fetch_call(rpc, addr, payload = msg, method=urlfetch.PUT, headers={'content-length':str(len(msg))})
		self.response.set_status(200)


