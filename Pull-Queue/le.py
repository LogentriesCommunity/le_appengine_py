import logging, random
from google.appengine.api import taskqueue

class PullQueue(logging.Handler):

    def __init__(self, key, location):

        logging.Handler.__init__(self)
        self.addr = '%s/hosts/%s' %(key, location)
	self.queue = taskqueue.Queue('pull-queue')
	format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
	self.setFormatter(format)


    def send(self, msg):

	task = taskqueue.Task(method='PULL', name = str(random.randrange(1,10000000000)), params={'msg':msg, 'addr':self.addr})
	self.queue.add(task)


    def handleError(self, record):
        pass


    def emit(self, record):

	msg = self.format(record)
        self.send(msg+'\n')


    def flush(self):
	pass

    def close(self):

        logging.Handler.close(self)


