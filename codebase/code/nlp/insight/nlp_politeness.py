## Module    >  nlp_politeness
## Functions >  politeness

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
from conver import response_balance

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import pandas as pd
import numpy as np
import warnings

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# politeness
#---------------------------------------------#
def politeness(link_id,msg_id, msg_threadid,msg_data, link_data, conver_data, msg_text_data):
	
	# print("Launching - politeness")

	"""
				
	"""
	global global_var

	# initialize
	politeness_df_tmp = {}
	
	# insight generation successful
	try:
	   
	   	politeness     = np.array([msg_text_data[x].polite for x in msg_id])
		request   	   = np.array([msg_text_data[x].request for x in msg_id])
		request_agg    = np.array([min(sum(msg_text_data[x].request),1) for x in msg_id])
		
		# response time 
		response_link_pair                          = np.array([link_data[x].link_response_id_pair for x in link_id])
		
		# balance
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			politeness_balance              		= [np.mean([response_balance(y, msg_text_data, 'polite') for y in x]) for x in response_link_pair]


	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - politeness")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("politeness")
		
		request            	= global_fun.fill_array(len(msg_id), np.nan)
		politeness         	= global_fun.fill_array(len(msg_id), np.nan)
		request_agg        	= global_fun.fill_array(len(msg_id), np.nan)
		politeness_balance 	= global_fun.fill_array(len(msg_id), np.nan)

	# format
	politeness_df_tmp = pd.DataFrame({'link_id':link_id, 'politeness..politeness':politeness,'politeness..politeness_imbalance':politeness_balance,'politeness..request_sentence':request, 'politeness..request':request_agg})

	# return
	# print("Successfully Completed - politeness")
	return(politeness_df_tmp)


#---------------------------------------------#