import wsgiref.handlers, logentries
from google.appengine.ext import webapp

def main():

	application = webapp.WSGIApplication([('/logentriesworker', LogentriesWorker)], debug=True)

	wsgiref.handlers.CGIHandler().run(application)

if __name__ =='__main__':
	main()
