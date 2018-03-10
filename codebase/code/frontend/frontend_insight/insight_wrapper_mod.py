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
from insight_main_mod import *
from insight_other_mod import *

# Define dictionary - insight_name / insight_function
insight_function = dict()

## sample
insight_function['date_dist']         = date_dist
insight_function['time_dist']         = time_dist
insight_function['network']           = network
insight_function['sample_sentiment']  = sample_sentiment

## main
insight_function['talkative']         = talkative
insight_function['responsiveness']    = responsiveness
insight_function['firstlast']         = firstlast


insight_function['politeness']        = politeness
insight_function['sentiment']         = sentiment
insight_function['coordination']      = coordination

## setting
insight_function['date_dist_setting'] = date_dist
insight_function['group_setting']     = group_setting

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# generate_insight
#---------------------------------------------#
def generate_insight_wrapper(insight_list, email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range): 

	print(insight_list)
	
	# generate unique copy of the email_link_df
	email_link_df_unique       = email_link_df.drop_duplicates(subset="msg_id", keep='first', inplace=False)

	# generate insight
	insight_temp               = insight_function[insight_list](email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range)

	return(insight_temp)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
