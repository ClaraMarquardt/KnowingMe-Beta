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
try:
	global_var
except NameError:
	global_var=dict()


# Setting var - initialize
try:
	setting_var
except NameError:
	setting_var=dict()


# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #