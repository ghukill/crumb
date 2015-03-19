# crumbDB twisted server wrapper
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET
from twisted.web import server, resource
from twisted.python import log

# python modules
import json
import logging 
import time

# local
import localConfig

'''
This Twisted Server wraps the following:
	- crumbDB: core crumbDB modules
	- crumb_http: flask for HTTP and API access
	- crumb_kafka (future): Apache Kafka consumer that interacts with crumbDB

Each access point import crumbDB
'''

# import crumb_http flask app
from crumb_http import crumb_http_app

# import crumb_kafka consumer
import crumb_kafka

# future kafka consumer
# class kafkaworker(object):
# 	@defer.inlineCallbacks
# 	def run(self):
# 		print "This is listening to Kafka..."
# 		yield True


# crumb_http
resource = WSGIResource(reactor, reactor.getThreadPool(), crumb_http_app)
site = Site(resource)

# run as script
if __name__ == '__main__':

	# crumb_http
	print "Starting crumb_server"
	reactor.listenTCP( 5001, site, interface="::")
	

	# fire reactor
	reactor.run()