# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         __init_global__  
# Purpose:      Initialize global variables, i.e. variables used across screens, 
#               threads, functions
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialize
# ------------------------------------------------------------------------ #

# Path
import os, sys
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *

# Global var - initialize
global_var = dict()

# ------------------------------------------------------------------------ #
# Variables - Track email downloading/overview
# ------------------------------------------------------------------------ #
global_var['status_email_load']  		 = 0
global_var['status_email_max']           = 0

global_var['status_overview_load']       = 0
global_var['status_overview_max']        = 0

global_var['status_analysis_load']       = 0
global_var['status_analysis_max']        = 0

# ------------------------------------------------------------------------ #
# Variables - Errors
# ------------------------------------------------------------------------ #
global_var['error']  				     = "General Error"
global_var['error_msg']                  = "General Error"

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
