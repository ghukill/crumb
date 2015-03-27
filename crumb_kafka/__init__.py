#crumb_kafka

# python module
import logging
import json

# apache kafka
from kafka import KafkaConsumer

# local
import crumbDB


# kafka consumer
class crumb_kafka_looper(object):
	def __init__(self):
		try:
			self.consumer = KafkaConsumer("crumb_air",
									  group_id="crumb_consumer",
									  metadata_broker_list=["localhost:9092"])
			logging.info("Initialized Apache Kafka connection.")
		except:
			logging.warning("Could not initialize Apache Kafka connection.")

	def consume(self):
		messages = self.consumer.fetch_messages()
		for message in messages:
			logging.info("Kafka message received: {msg}".format(msg=message))
			result = self.processMessage(message)

	# process message from consumer
	def processMessage(self, message):

		try:
			# retrieve payload and parse
			payload = json.loads(message.value)
			logging.debug(payload)

			# prepare
			action = payload['action'].lower()
			key = payload['key']
			if "value" in payload.keys():
				value = payload['value']
			else:
				value = False
			index = payload['index']

			# act
			crumb_handle = crumbDB.models.Crumb(key, value, index)
			crumb_action = getattr(crumb_handle.io, action)
			result = crumb_action()
			return result

		except Exception, e:
			crumb_handle.release_crumb_lock()
			logging.debug(str(e))
			return str(e)
