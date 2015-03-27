# crumb
Simple filesystem based key/value storage written in Python.
<a target="_blank" href="https://docs.google.com/drawings/d/13fF6OExvrzg-zclSGoFmAMkko-N6azliPfHQrX6yM2I/edit?usp=sharing">Overview Model</a>


## Overview
crumb is broken into the following components:
* crumbDB: core components, fs mechanics
* crumb_http:  Flask app that provides HTTP / API wrapper for crumbDB
* crumb_kafka:  Apache Kafka consumer that intiates crumbDB actions

Everything is wrapped in Twisted server, with end goal of providing crumbDB as standalone module.


## Requirements:
* Python Twisted Server (pip install)
* python flask
* python-kafka (pip install)


## To install:
* <a href="http://kafka.apache.org/downloads.html">download Apache Kafka</a>
* fire up zookeeper and apache kafka from unzipped / untarred kafka directory:
  * start zookeeper: bin/zookeeper-server-start.sh config/zookeeper.properties
  * start kafka server: bin/kafka-server-start.sh config/server.properties
  * create kafka topic ('crumb_air' is default): bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic crumb_air --partitions 1 --replication-factor 1
* start twisted server that houses most of the moving parts: python crumb_server.py


## Usage

### HTTP / REST Flask API 
* write crumb: http://[host]/[prefix if applicable]/write/[index]/?key=foo&value=bar
* get crumb: http://[host]/[prefix if applicable]/get/[index]/?key=foo
* update crumb: http://[host]/[prefix if applicable]/update/[index]/?key=foo&value=zag
* delete crumb: http://[host]/[prefix if applicable]/update/[index]/?key=foo

### Console API - through Kafka

```
# Apache Kafka
from kafka import KafkaClient, SimpleProducer

# init Kafka
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

# write crumb
trans_dict = { "action":"write", "key":"foo", "value":"bar", "index":"testing" }
result = producer.send_messages("crumb_air", json.dumps( trans_dict ))

# get crumb
trans_dict = { "action":"get", "key":"foo", "index":"testing" }
result = producer.send_messages("crumb_air", json.dumps( trans_dict ))

# update crumb
trans_dict = { "action":"udpate", "key":"foo", "value":"zag", "index":"testing" }
result = producer.send_messages("crumb_air", json.dumps( trans_dict ))

# delete crumb
trans_dict = { "action":"delete", "key":"foo", "index":"testing" }
result = producer.send_messages("crumb_air", json.dumps( trans_dict ))
```