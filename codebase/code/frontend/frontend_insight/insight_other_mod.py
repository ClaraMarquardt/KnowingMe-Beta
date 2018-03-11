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
	
	## raw data
	contact_df_temp                         		   = contact_df      							   
	contact_df_temp['contact_gender']				   = contact_df_temp['contact_gender'].replace({'F': 1, 'M':2, 'I':3})
	contact_df_temp   								   = contact_df_temp.sort_values(by=['contact_gender'], ascending=[True])
	contact_df_temp['contact_gender']				   = contact_df_temp['contact_gender'].replace({1:'F', 2:'M', 3:'I'})

	group_setting_dict['contact_name']        		   = list(np.array(contact_df_temp['contact_name']))
	group_setting_dict['contact_email']        		   = list(np.array(contact_df_temp['contact']))

	map_gender 	                                       = {'F':1,'M':2,'I':3}	
	group_setting_dict['contact_gender']        	   = list(np.array(contact_df_temp['contact_gender']))
	group_setting_dict['contact_gender']               = list(np.array(pd.Series(group_setting_dict['contact_gender']).map(map_gender)))
	
	return(group_setting_dict)

	
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
