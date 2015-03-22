# tests for crumbDB

#python
import random
import requests

# crumbDB
import utilities
import models


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
		g = models.Crumb(x, x, index)
		g.io.update(new_value)


@utilities.timing
def runAllRangeTests():
	start = 1
	end = 500
	new_value = 'updated'
	index = str(int(random.random() * 100000))

	

	writeNumRange(start,end,index)
	getNumRange(start,end,index)
	updateNumRange(start,end,index,new_value)

	print "Finished range tests with these params:",start,end,new_value,index



##### HTTP / API Flask Tests #####

@utilities.timing
def http_writeNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:5001/write/{index}/?key={x}&value={x}".format(index=index,x=x))



@utilities.timing
def http_getNumRange(start, end, index):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for both key and value, and "index" as new index
	'''
	for x in range(start,end):
		requests.get("http://localhost:5001/write/{index}/?key={x}&value={x}".format(index=index,x=x))



@utilities.timing
def http_updateNumRange(start, end, index, new_value):
	'''
	arguments: (start, end, index), where "start" and "end" as integers for key, "new_value" as new value, and "index" as new index
	'''
	for x in range(start,end):
		g = models.Crumb(x, x, index)
		g.io.update(new_value)


@utilities.timing
def http_runAllRangeTests():
	start = 1
	end = 500
	new_value = 'updated'
	index = str(int(random.random() * 100000))

	

	writeNumRange(start,end,index)
	getNumRange(start,end,index)
	updateNumRange(start,end,index,new_value)

	print "Finished range tests with these params:",start,end,new_value,index
