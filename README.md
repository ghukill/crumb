# crumb
Simple filesystem based key/value storage written in Python.
<a target="_blank" href="https://docs.google.com/drawings/d/13fF6OExvrzg-zclSGoFmAMkko-N6azliPfHQrX6yM2I/edit?usp=sharing">Overview Model</a>

crumb is broken into the following components:
* crumbDB: core components, fs mechanics
* crumb_http:  Flask app that provides HTTP / API wrapper for crumbDB
* crumb_kafka (future):  Apache Kafka consumer that intiates crumbDB actions

Everything is wrapped in Twisted server, with end goal of providing crumbDB as standalone module.



