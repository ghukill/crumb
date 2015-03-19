# crumb_http flask app views

# python modules

# crumb modeules
import localConfig
import crumbDB
from crumb_http import crumb_http_app


# write crumb
@crumb_http_app.route("/write/<key>/<value>", methods=['GET', 'POST'])
def write(key,value):
	
	crumb_handle = crumbDB.models.Crumb(key,value)
	
	if crumb_handle.io.write() == True:
		return "Crumb written"


# get crumb value
@crumb_http_app.route("/get/<key>", methods=['GET', 'POST'])
def get(key):
	
	crumb_handle = crumbDB.models.Crumb(key)
	crumb_handle.io.get()
	return crumb_handle.value


# update crumb value
@crumb_http_app.route("/update/<key>/<value>", methods=['GET', 'POST'])
def update(key,value):
	
	crumb_handle = crumbDB.models.Crumb(key,value)
	
	if crumb_handle.io.update(value) == True:
		return "Crumb updated"


# update crumb value
@crumb_http_app.route("/delete/<key>", methods=['GET', 'POST'])
def delete(key):
	
	crumb_handle = crumbDB.models.Crumb(key)

	if crumb_handle.io.delete() == True:
		return "Crumb deleted"
