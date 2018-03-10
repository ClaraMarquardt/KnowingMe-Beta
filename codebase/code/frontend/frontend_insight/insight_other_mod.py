# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_other_mod
# Purpose:      Module - Define other insight functions
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
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *

# Dependencies - Internal
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# talkative
#---------------------------------------------#
def group_setting(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	group_setting_dict     = dict()
	
	return(group_setting_dict)

	
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
