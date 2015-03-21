# crumb_http flask app views

# python modules
from flask import request
import logging

# crumb modeules
import localConfig
import crumbDB
from crumb_http import crumb_http_app, utilities

# Apache Kafka
from kafka import SimpleProducer


# init Kafka
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)


# write crumb
@crumb_http_app.route("/write", methods=['GET', 'POST'])
def write():

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key,value)
	
	# routed through kafka
	# producer.send_messages("crumb", json.loads( { "action": } ))

	# direct crumb
	try:
		crumb_transaction = crumb_handle.io.write()
		return "crumb written"
	except Exception, e:
		logging.debug(str(e))
		return str(e)	


# get crumb value
@crumb_http_app.route("/get", methods=['GET', 'POST'])
def get():

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key)

	try:
		crumb_handle.io.get()
		return crumb_handle.value
	except Exception, e:
		logging.debug(str(e))
		return str(e)


# update crumb value
@crumb_http_app.route("/update", methods=['GET', 'POST'])
def update():
	
	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key,value)
	
	try:
		crumb_handle.io.update(value)
		return "crumb updated"
	except Exception, e:
		logging.debug(str(e))
		return str(e)


# update crumb value
@crumb_http_app.route("/delete", methods=['GET', 'POST'])
def delete():

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key)

	try:
		crumb_handle.io.delete()
		return "crumb deleted"
	except:
		logging.debug(str(e))
		return str(e)














