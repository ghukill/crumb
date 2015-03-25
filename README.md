# crumb
Simple filesystem based key/value storage written in Python.
<a target="_blank" href="https://docs.google.com/drawings/d/13fF6OExvrzg-zclSGoFmAMkko-N6azliPfHQrX6yM2I/edit?usp=sharing">Overview Model</a>

crumb is broken into the following components:
* crumbDB: core components, fs mechanics
* crumb_http:  Flask app that provides HTTP / API wrapper for crumbDB
* crumb_kafka:  Apache Kafka consumer that intiates crumbDB actions

Everything is wrapped in Twisted server, with end goal of providing crumbDB as standalone module.

Requirements:
* Python Twisted Server (pip install)
* python flask
* python-kafka (pip install)

To install / use:
* <a href="http://kafka.apache.org/downloads.html">download Apache Kafka</a>
* fire up zookeeper and apache kafka from unzipped / untarred kafka directory:
  * start zookeeper: bin/zookeeper-server-start.sh config/zookeeper.properties
  * start kafka server: bin/kafka-server-start.sh config/server.properties
  * create kafka topic ('crumb_air' is default): bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic crumb_air --partitions 1 --replication-factor 1
* start twisted server that houses most of the moving parts: python crumb_server.py



