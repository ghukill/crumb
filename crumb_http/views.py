# crumb_http flask app views

# python modules
from flask import request
import logging
import time
import json

# crumb modeules
import localConfig
import crumbDB
from crumb_http import crumb_http_app, utilities

# Apache Kafka
from kafka import KafkaClient, SimpleProducer

# init Kafka
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)



# write crumb
@crumb_http_app.route("/write/<index>/", methods=['GET', 'POST'])
def write(index):

	try:
		result = writeCrumb(index, request, write_type="write")
		return "crumb written"
	except Exception, e:
		return str(e)



# update crumb value
@crumb_http_app.route("/update/<index>/", methods=['GET', 'POST'])
def update(index):

	try:
		result = writeCrumb(index, request, write_type="update")
		return "crumb updated"
	except Exception, e:
		return str(e)
	


# get crumb value
@crumb_http_app.route("/get/<index>/", methods=['GET', 'POST'])
def get(index):

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key,False,index)

	# straight through
	try:
		crumb_handle.io.get()
		return crumb_handle.value
	except Exception, e:
		logging.debug(str(e))
		crumb_handle.release_crumb_lock()
		return str(e)



# update crumb value
@crumb_http_app.route("/delete/<index>/", methods=['GET', 'POST'])
def delete(index):

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key,False,index)

	try:
		result = producer.send_messages("crumb_air", json.dumps( { "action":"delete", "key":key, "value":value, "index":index } ))
		return "crumb deleted"
	except Exception, e:
		logging.debug(str(e))
		crumb_handle.release_crumb_lock()
		return str(e)



# abstracted function to write / update crumbs
def writeCrumb(index, request, write_type):

	# function to return key / value tuple
	key,value = utilities.extractKV(request)
	crumb_handle = crumbDB.models.Crumb(key,value,index)

	# determine if write OR update
	if write_type == "write":
		if crumb_handle.exists == True:
			raise IOError("crumb already exists")

	# perform write
	try:
		result = producer.send_messages("crumb_air", json.dumps( { "action":write_type, "key":key, "value":value, "index":index } ))
	except Exception, e:
		logging.debug(str(e))
		crumb_handle.release_crumb_lock()
		return str(e)








