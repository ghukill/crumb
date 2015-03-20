#crumb_kafka

# python module
import logging
import json

# local
import crumbDB

# process message from consumer
def processMessage(message):
	
	'''
	Need some kind of checking here?
	'''

	# retrieve payload and parse
	payload = json.loads(message.value)
	print payload

	# prepare
	action = payload['action'].lower()
	key = payload['key']
	value = payload['value']

	# act
	crumb_handle = crumbDB.models.Crumb(key,value)
	crumb_action = getattr(crumb_handle.io, action)
	result = crumb_action()
	return result
