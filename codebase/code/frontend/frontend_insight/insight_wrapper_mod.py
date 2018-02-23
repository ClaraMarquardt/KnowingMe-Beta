# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_wrapper_mod
# Purpose:      Module - Define insight wrapper functions
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

sys.path.append(os.path.normpath(os.path.join(app_root, 'code', 'frontend','frontend_insight')))
from insight_sample_mod import *

# Define dictionary - insight_name / insight_function
insight_function = dict()

## sample
insight_function['date_dist']         = date_dist
insight_function['time_dist']         = time_dist
insight_function['network']           = network
insight_function['sample_sentiment']  = sample_sentiment

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# generate_insight
#---------------------------------------------#
def generate_insight_wrapper(insight_list, email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range): 

	## initialize
	insight_dict = dict()

	## loop over insights
	for insight_name in insight_list:

		print(insight_name)
		
		insight_temp               = insight_function[insight_name](email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range)
		insight_dict[insight_name] = insight_temp

	return(insight_dict)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
