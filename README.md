# crumbDB
Simple filesystem based key/value storage written in Python.

crumbDB is broken into the following components:
* crumbDB: core components, fs mechanics
* crumb_http:  Flask app that provides HTTP / API wrapper for crumbDB
* crumb_kafka (future):  Apache Kafka consumer that intiates crumbDB actions

Everything is wrapped in Twisted server, with end goal of providing crumbDB as standalone module.
