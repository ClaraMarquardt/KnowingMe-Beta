# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_nonlang_mod
# Purpose:      Module - Define nonlang insight functions
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
from __init_setting__ import *

# Dependencies - Internal
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_helper')))
from analysis_conver_mod import conver_timediff
from analysis_contact_mod import contact_labeller

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# responsiveness
#---------------------------------------------#

def responsiveness_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - responsiveness")

	"""

	"""
	
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
			responsiveness_df_tmp['response_time']   = [np.nanmean([conver_timediff(y,msg_data) for y in x]) for x in response_link_pair]
			
	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - responsiveness")
		print(e)

		responsiveness_df_tmp['link_reply']           = global_fun_mod.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_reply_count']     = global_fun_mod.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_response']        = global_fun_mod.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['link_response_count']  = global_fun_mod.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['msg_response']         = global_fun_mod.fill_array(len(msg_id), np.nan)
		responsiveness_df_tmp['response_time']        = global_fun_mod.fill_array(len(msg_id), np.nan)

	# format
	responsiveness_df_tmp = responsiveness_df_tmp[['link_id', 'link_reply','link_reply_count','link_response','link_response_count','msg_response','response_time']] 
	responsiveness_df_tmp = responsiveness_df_tmp.rename(columns={'link_reply':'responsiveness..reply','link_reply_count':'responsiveness..reply_count','link_response':'responsiveness..response','link_response_count':'responsiveness..response_count', 'msg_response':'responsiveness.__msg_response', 'response_time':'responsiveness..response_time'})

	# return
	# print("Successfully Completed - responsiveness")
	return(responsiveness_df_tmp)

# firstlast
#---------------#

def firstlast_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - firstlast")

	"""

	"""
	
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
		
		firstlast_df_tmp['conversation']     	  = global_fun_mod.fill_array(len(msg_id), np.nan)				
		firstlast_df_tmp['first']     			  = global_fun_mod.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['last']     			  = global_fun_mod.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['msg_first']     		  = global_fun_mod.fill_array(len(msg_id), np.nan)
		firstlast_df_tmp['msg_last']      		  = global_fun_mod.fill_array(len(msg_id), np.nan)


	# format
	firstlast_df_tmp = firstlast_df_tmp[['link_id', 'first','last','msg_first','msg_last','conversation']] 
	firstlast_df_tmp = firstlast_df_tmp.rename(columns={'first':'firstlast..first', 'last':'firstlast..last', 'msg_first':'firstlast.__msg_first','msg_last':'firstlast.__msg_last','conversation':'firstlast.__conversation'})

	# return
	# print("Successfully Completed - firstlast")
	return(firstlast_df_tmp)

# contact
#---------------#

def contact_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - contact")

	"""

	"""
	
	# initialize
	contact_df_tmp = pd.DataFrame({'link_id':link_id, 'msg_id':msg_id})

	# insight generation successful
	try:

		# initialize
		user_group_male           = np.array(contact_df.loc[contact_df['contact_gender']=='M','contact'])
		user_group_female         = np.array(contact_df.loc[contact_df['contact_gender']=='F','contact'])
		user_group_unknown_gender = np.array(contact_df.loc[contact_df['contact_gender']=='I','contact'])

		contact_xwalk_contact 	  = np.concatenate([user_group_male, user_group_female, user_group_unknown_gender])
		contact_xwalk_label       = np.concatenate([np.array(global_fun_mod.fill_array(len(user_group_male), "M")), np.array(global_fun_mod.fill_array(len(user_group_female), "F")), np.array(global_fun_mod.fill_array(len(user_group_unknown_gender), "I"))])

		# generate contact flag, etc.
		contact_flag, contact_flag_msg, contact_flag_thread = contact_labeller(contact_xwalk_contact, contact_xwalk_label,
		email_link_df['link_contact'] ,email_link_df['msg_id'] ,email_link_df['msg_threadid'] )
		
		# merge in 
		contact_df_tmp['contact_group']        = contact_flag
		contact_df_tmp['contact_group_msg']    = contact_flag_msg
		contact_df_tmp['contact_group_thread'] = contact_flag_thread


	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - contact")
		print(e)
		
		contact_df_tmp['contact_group']        = global_fun_mod.fill_array(len(msg_id), np.nan)
		contact_df_tmp['contact_group_msg']    = global_fun_mod.fill_array(len(msg_id), np.nan)
		contact_df_tmp['contact_group_thread'] = global_fun_mod.fill_array(len(msg_id), np.nan)


	# format
	contact_df_tmp = contact_df_tmp[['link_id', 'contact_group','contact_group_msg','contact_group_thread']] 

	# return
	# print("Successfully Completed - contact")
	return(contact_df_tmp)


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
