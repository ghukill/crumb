# crumb server flask app

# python
import flask

# crumb
import localConfig
import models
import server


# create app
app = flask.Flask(__name__)

# get handlers
import server