## Module    >  server
## Functions >  flask_initialize

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Dependencies - Internal
#---------------------------------------------#
sys.path.append(os.path.normpath(os.path.join(app_root,'code','setup')))


# Dependencies - External
#---------------------------------------------#
import flask
import time
import json
import datetime

# Function Definition
#---------------------------------------------#

# flask_initialize
#---------------#
def flask_initialize(debug, secret_key, app_static, app_template):

	app            = flask.Flask(__name__, static_folder=app_static, template_folder=app_template)
	app.debug      = bool(debug)

	app.secret_key = secret_key

	return(app)


#---------------------------------------#
	
