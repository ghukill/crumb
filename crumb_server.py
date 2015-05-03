# -*- coding: utf-8 -*-

# crumbDB twisted server wrapper
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater, LoopingCall
from twisted.web.server import NOT_DONE_YET
from twisted.web import server, resource
from twisted.python import log

# python modules
import json
import logging
import time
import lmdb

# local
import localConfig

# import crumb_http flask app
from crumb_http import crumb_http_app

# import crumb_kafka consumer
import crumb_kafka
'''
This Twisted Server wraps the following:
	- crumbDB: core crumbDB modules
	- crumb_http: flask for HTTP and API access
	- crumb_kafka: Apache Kafka consumer that interacts with crumbDB

Each access point import crumbDB
'''


# crumb_http
resource = WSGIResource(reactor, reactor.getThreadPool(), crumb_http_app)
site = Site(resource)

# run as script
if __name__ == '__main__':

    # crumb_http
    print '''
 ██████╗██████╗ ██╗   ██╗███╗   ███╗██████╗ ██████╗ ██████╗ 
██╔════╝██╔══██╗██║   ██║████╗ ████║██╔══██╗██╔══██╗██╔══██╗
██║     ██████╔╝██║   ██║██╔████╔██║██████╔╝██║  ██║██████╔╝
██║     ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██║  ██║██╔══██╗
╚██████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║██████╔╝██████╔╝██████╔╝
╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═════╝ ╚═════╝ 
'''

    # crumb_http
    reactor.listenTCP(localConfig.crumb_http_port, site, interface="::")

    # looping listener for crumb_kafka
    lc = LoopingCall(crumb_kafka.crumb_kafka_looper().consume)
    lc.start(.1)

    # fire reactor
    reactor.run()
