# crumbDB tests

# tests for crumbDB

#python
import random
import requests
import sys
import json

import localConfig

# crumbDB
from crumbDB import models, utilities

# Apache Kafka
from kafka import KafkaClient, SimpleProducer

# init Kafka
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)



##### Raw crumbDB Tests #####

@utilities.timing
def writeNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		g = models.Crumb(x, x, index)
		g.io.write()



@utilities.timing
def getNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		g = models.Crumb(x, False, index)
		g.io.get()



@utilities.timing
def updateNumRange(start, end, index, new_value):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for key, "new_value" as new value, and "index" as new index
	'''
	for x in range(start,end):
		g = models.Crumb(x, new_value, index)
		g.io.update()



@utilities.timing
def deleteNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for key, "new_value" as new value, and "index" as new index
	'''
	for x in range(start,end):
		g = models.Crumb(x, x, index)
		g.io.delete()


@utilities.timing
def run_crumbDB_tests():
	
	start = 1
	end = 500
	new_value = 'updated'
	index = str(int(random.random() * 100000))

	writeNumRange(start,end,index)
	getNumRange(start,end,index)
	updateNumRange(start,end,index,new_value)
	deleteNumRange(start,end,index)

	print "Finished range tests with these params:",start,end,new_value,index


##### Raw crumbDB through Apache Kafka Tests #####

@utilities.timing
def kafka_writeNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		result = producer.send_messages("crumb_air", json.dumps( { "action":"write", "key":x, "value":x, "index":index } ))



@utilities.timing
def kafka_getNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		result = producer.send_messages("crumb_air", json.dumps( { "action":"get", "key":x, "index":index } ))



@utilities.timing
def kafka_updateNumRange(start, end, index, new_value):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for key, "new_value" as new value, and "index" as new index
	'''
	for x in range(start,end):
		result = producer.send_messages("crumb_air", json.dumps( { "action":"update", "key":x, "value":new_value, "index":index } ))



@utilities.timing
def kafka_deleteNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for key, "new_value" as new value, and "index" as new index
	'''
	for x in range(start,end):
		result = producer.send_messages("crumb_air", json.dumps( { "action":"delete", "key":x, "index":index } ))


@utilities.timing
def run_kafka_tests():
	
	start = 1
	end = 500
	new_value = 'updated'
	index = str(int(random.random() * 100000))

	kafka_writeNumRange(start,end,index)
	kafka_getNumRange(start,end,index)
	kafka_updateNumRange(start,end,index,new_value)
	kafka_deleteNumRange(start,end,index)

	print "Finished range tests with these params:",start,end,new_value,index



##### crumb_http HTTP / API Flask Tests #####

# GET
@utilities.timing
def http_writeNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:{port}/write/{index}/?key={x}&value={x}".format(index=index,x=x, port=localConfig.crumb_http_port))



@utilities.timing
def http_getNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:{port}/write/{index}/?key={x}&value={x}".format(index=index,x=x, port=localConfig.crumb_http_port))



@utilities.timing
def http_updateNumRange(start, end, index, new_value):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:{port}/update/{index}/?key={x}&value={new_value}".format(index=index,x=x, new_value=new_value, port=localConfig.crumb_http_port))


@utilities.timing
def http_deleteNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:{port}/delete/{index}/?key={x}&value={x}".format(index=index,x=x, port=localConfig.crumb_http_port))


# POST
@utilities.timing
def http_post_writeNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.post("http://localhost:{port}/write/{index}/".format(index=index, port=localConfig.crumb_http_port), data={'key':x, 'value':x, 'index':index})



@utilities.timing
def http_post_getNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.post("http://localhost:{port}/get/{index}/".format(index=index, port=localConfig.crumb_http_port), data={'key':x, 'value':x, 'index':index})



@utilities.timing
def http_post_updateNumRange(start, end, index, new_value):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.post("http://localhost:{port}/update/{index}/".format(index=index, port=localConfig.crumb_http_port), data={'key':x, 'value':new_value, 'index':index})



@utilities.timing
def http_post_deleteNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.post("http://localhost:{port}/delete/{index}/".format(index=index, port=localConfig.crumb_http_port), data={'key':x, 'value':x, 'index':index})



@utilities.timing
def run_crumb_http_tests():
	
	start = 1
	end = 500
	new_value = 'updated'
	index = str(int(random.random() * 100000))

	# GET
	http_writeNumRange(start,end,index)
	http_getNumRange(start,end,index)
	http_updateNumRange(start,end,index,new_value)
	http_deleteNumRange(start,end,index)

	# POST
	http_post_writeNumRange(start,end,index)
	http_post_getNumRange(start,end,index)
	http_post_updateNumRange(start,end,index,new_value)
	http_post_deleteNumRange(start,end,index)

	print "Finished range tests with these params:",start,end,new_value,index



# run all tests as script
if __name__ == '__main__':

	if len(sys.argv) > 1:
		perform = sys.argv[1].lower()

		if perform in ['crumbdb','all']:
			print "Running crumbDB tests"
			run_crumbDB_tests()

		if perform in ['kafka','all']:
			print "Running kafka tests"
			run_kafka_tests()

		if perform in ['crumb_http','all']:
			print "Running crumb_http GET tests"
			run_crumb_http_tests()

	else:
		print "Please type either 'crumbDB', 'kafka', crumb_http', or 'all'"

	
