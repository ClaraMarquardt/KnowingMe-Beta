# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_wrapper_mod
# Purpose:      Module - Define feature wrapper functions
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
from __init_global__ import *

sys.path.append(os.path.normpath(os.path.join(app_root, 'code', 'frontend','frontend_feature')))
from feature_nlp_mod import *
from feature_nonlang_mod import *
from feature_simplelang_mod import *

# Define dictionary - feature_name / feature_function
feature_function = dict()

## nlp
feature_function['sentiment']         = sentiment
feature_function['politeness']        = politeness
feature_function['coordination']      = coordination

## simplelang
feature_function['talkative']         = talkative
feature_function['lengthimbalance']   = lengthimbalance
feature_function['birthday']          = birthday

## nonlang
feature_function['responsiveness']    = responsiveness
feature_function['firstlast']         = firstlast

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# generate_insight_feature
#---------------------------------------------#
def generate_feature_wrapper(feature_list, email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date): 

	## initialize
	feature_dict = dict()
	
	## loop over features
	for feature_name in feature_list:
		
		print(feature_name)
		
		feature_temp   = feature_function[feature_name](email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date)
		email_link_df  = pd.merge(feature_temp, email_link_df, on='link_id', how='outer')

	return(email_link_df)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
