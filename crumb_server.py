# crumb twisted server wrapper
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET
from twisted.web import server, resource
from twisted.python import log

import json
import logging 
import time

# local
from localConfig import *

# import crumb flask app
from crumb import app

# twisted liseners
logging.basicConfig(level=logging.DEBUG)

class kafkaworker(object):

	@defer.inlineCallbacks
	def run(self):
		print "This will be listening to Kafka..."
		yield True

	

if __name__ == '__main__':
	kafkaworker().run()
	reactor.run()