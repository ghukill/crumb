# crumb server flask app

# python
import flask

# crumb
import localConfig

# create app
crumb_http_app = flask.Flask(__name__)

# get handlers
import views