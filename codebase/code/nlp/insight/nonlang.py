## Module    > nonlang 
## Functions > volume, responsiveness, firstlast

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
from conver import conver_timediff

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

# volume
#---------------------------------------------#

def volume(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data):
	
	# print("Launching - volume")

	"""

	"""
	global global_var

	# initialize
	volume_df_tmp = {}

	link_inbox_outbox = np.array([msg_data[x].inbox_outbox for x in msg_id])
	link_contact      = np.array([link_data[x].link_contact for x in link_id])

	# insight generation successful
	try:

		# email level
		volume_df_tmp['overall_email']            = len(np.unique(msg_id))
		volume_df_tmp['overall_sent_email']       = len(np.unique(msg_id[link_inbox_outbox=="outbox"]))
		volume_df_tmp['overall_received_email']   = len(np.unique(msg_id[link_inbox_outbox=="inbox"]))
	
		# link level
		volume_df_tmp['overall_link']             = len(np.unique(link_id))
		volume_df_tmp['overall_sent_link']        = len(np.unique(link_id[link_inbox_outbox=="outbox"]))
		volume_df_tmp['overall_received_link']    = len(np.unique(link_id[link_inbox_outbox=="inbox"]))

		# link level
		volume_df_tmp['overall_contact']          = len(np.unique(link_contact))
		volume_df_tmp['overall_sent_contact']     = len(np.unique(link_contact[link_inbox_outbox=="outbox"]))
		volume_df_tmp['overall_received_contact'] = len(np.unique(link_contact[link_inbox_outbox=="inbox"]))

	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - volume")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("volume")

		# email level
		volume_df_tmp['overall_email']              = np.nan
		volume_df_tmp['overall_sent_email']         = np.nan
		volume_df_tmp['overall_received_email']     = np.nan
	
		# link level
		volume_df_tmp['overall_link']               = np.nan
		volume_df_tmp['overall_sent_link']          = np.nan
		volume_df_tmp['overall_received_link']      = np.nan

		# link level
		volume_df_tmp['overall_contact']            = np.nan
		volume_df_tmp['overall_sent_contact']       = np.nan
		volume_df_tmp['overall_received_contact']   = np.nan


	# return
	# print("Successfully Completed - volume")
	return(volume_df_tmp)

# responsiveness
#---------------------------------------------#

def responsiveness(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data):
	
	# print("Launching - responsiveness")

	"""

	"""
	global global_var
	
	# initialize
	responsiveness_df_tmp = pd.DataFrame({'link_id':link_id, 'msg_id':msg_id})

	# insight generation successful
	try:

		# reply - (i) link
		responsiveness_df_tmp['link_reply']          = np.array([link_data[x].link_reply for x in link_id])
		responsiveness_df_tmp['link_reply_count']    = np.array([link_data[x].link_reply_count for x in link_id])

		# response - (i) link > (ii) message
		responsiveness_df_tmp['link_response']       = np.array([link_data[x].link_response for x in link_id])
		responsiveness_df_tmp['link_response_count'] = np.array([link_data[x].link_response_count for x in link_id])

		responsiveness_df_tmp_agg                    = pd.DataFrame(responsiveness_df_tmp.groupby('msg_id')['link_response'].aggregate(np.max))
		responsiveness_df_tmp_agg['msg_id']          = responsiveness_df_tmp_agg.index
		responsiveness_df_tmp_agg.columns            = np.array(['msg_response','msg_id'])
		responsiveness_df_tmp                        = pd.merge(responsiveness_df_tmp, responsiveness_df_tmp_agg, on='msg_id', how='inner')
		
		# response time 
		response_link_pair                           = np.array([link_data[x].link_response_id_pair for x in link_id])
		
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			responsiveness_df_tmp['response_time']   = [np.mean([conver_timediff(y,msg_data) for y in x]) for x in response_link_pair]
			
	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - responsiveness")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("responsiveness")

		responsiveness_df_tmp['link_reply']           = global_fun.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_reply_count']     = global_fun.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_response']        = global_fun.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_response_count']  = global_fun.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['msg_response']         = global_fun.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['response_time']        = global_fun.fill_array(len(msg_id), np.nan)

	# format
	responsiveness_df_tmp = responsiveness_df_tmp[['link_id', 'link_reply','link_reply_count','link_response','link_response_count','msg_response','response_time']] 
	responsiveness_df_tmp = responsiveness_df_tmp.rename(columns={'link_reply':'responsiveness..reply','link_reply_count':'responsiveness..reply_count','link_response':'responsiveness..response','link_response_count':'responsiveness..response_count', 'msg_response':'responsiveness.__msg_response', 'response_time':'responsiveness..response_time'})

	# return
	# print("Successfully Completed - responsiveness")
	return(responsiveness_df_tmp)

# firstlast
#---------------#

def firstlast(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data):
	
	# print("Launching - firstlast")

	"""

	"""
	global global_var
	
	# initialize
	firstlast_df_tmp = pd.DataFrame({'link_id':link_id, 'msg_id':msg_id})

	# insight generation successful
	try:

		# first - last - link
		firstlast_df_tmp['conversation'] 		  = np.array([conver_data[x].conversation for x in msg_threadid])
		firstlast_df_tmp['first'] 				  = np.array([msg_data[x].conversation_first for x in msg_id])
		firstlast_df_tmp['last']  				  = np.array([msg_data[x].conversation_last for x in msg_id])
		
		# first - last - msg
		firstlast_df_tmp_agg                  	  = pd.DataFrame(firstlast_df_tmp.groupby('msg_id')['first','last'].aggregate(np.max))
		firstlast_df_tmp_agg['msg_id']            = firstlast_df_tmp_agg.index
		firstlast_df_tmp_agg.columns              = np.array(['msg_first','msg_last','msg_id'])
		firstlast_df_tmp                          = pd.merge(firstlast_df_tmp, firstlast_df_tmp_agg, on='msg_id', how='inner')


	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - firstlast")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("firstlast")

		firstlast_df_tmp['conversation']     	  = global_fun.fill_array(len(msg_id), np.nan)				
		firstlast_df_tmp['first']     			  = global_fun.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['last']     			  = global_fun.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['msg_first']     		  = global_fun.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['msg_last']      		  = global_fun.fill_array(len(msg_id), np.nan)


	# format
	firstlast_df_tmp = firstlast_df_tmp[['link_id', 'first','last','msg_first','msg_last','conversation']] 
	firstlast_df_tmp = firstlast_df_tmp.rename(columns={'first':'firstlast..first', 'last':'firstlast..last', 'msg_first':'firstlast.__msg_first','msg_last':'firstlast.__msg_last','conversation':'firstlast.__conversation'})

	# return
	# print("Successfully Completed - firstlast")
	return(firstlast_df_tmp)

#---------------------------------------------#