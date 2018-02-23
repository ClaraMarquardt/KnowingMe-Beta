# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         app_init_mod
# Purpose:      Module - Define app init functions
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialization
# ------------------------------------------------------------------------ #

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *

#----------------------------------------------------------------------------#
#			                     Functions                                   #
#----------------------------------------------------------------------------#

# flask_initialize
#---------------#
def flask_initialize(debug, secret_key, app_static, app_template):

	app            = flask.Flask(__name__, static_folder=app_static, template_folder=app_template)
	app.debug      = bool(debug)
	app.secret_key = secret_key

	return(app)


#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
	
