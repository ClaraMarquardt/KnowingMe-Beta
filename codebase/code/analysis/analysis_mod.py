# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         feature_generation_mod
# Purpose:      Module - Define analysis functions
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
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *
from __init_setting__ import *
from __init_global__ import *

# Dependencies - Internal
from analysis_helper import *  

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# feature_generation
#---------------------------------------------#
def analysis(email_file_array, user_address, output_dir, current_date, earliest_date, latest_date):
	
	# global variables
	global global_var
	
	# initialize
	global_var['status_analysis_max'] = 9
	feature_dict_file                 = os.path.normpath(os.path.join(output_dir, "other", 'feature_'+ 
		datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '_' +
		datetime.datetime.strptime(earliest_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '_' +
		datetime.datetime.strptime(latest_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))

	# Import & basic processing > email_df
	# -------------------------------------------#
	if (not os.path.exists(feature_dict_file)):


		# load
		# ---------------------------#	

		print("Emails - files: " + str(len(email_file_array)))

		print("Launch - load")
		email_df             		  = analysis_load_mod.load_email(email_file_array)
		
		## status
		print("Emails - loaded: " + str(len(email_df)))

		print("Successfully completed - loading")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# response structure
		# ---------------------#	
		email_df = analysis_conver_mod.response_structure(email_df)

		print("Successfully completed - response_structure")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# Message & Conversation Processing > objects
		# -------------------------------------------#	

		# parse conversations
		conver_parser       = analysis_msg_class_mod.conver
		msg_threadid        = np.unique(np.array(email_df['msg_threadid']))
		conver_parsed       = [conver_parser(email_df.loc[email_df['msg_threadid']==x]) for x in msg_threadid]
		conver_parsed       = dict([(x,y) for (x,y) in zip(msg_threadid, conver_parsed)])

		print("Successfully completed - conversation object creation")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# parse messages (1)
		msg_parser          = analysis_msg_class_mod.msg
		msg_id              = np.unique(np.array(email_df['msg_id']))
		msg_parsed          = [msg_parser(email_df.loc[email_df['msg_id']==x], conver_parsed) for x in msg_id]
		msg_parsed          = dict([(x,y) for (x,y) in zip(msg_id, msg_parsed)])

		print("Successfully completed - message object creation")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# parse links 
		link_parser         = analysis_msg_class_mod.link
		link_parsed         = sum([analysis_dimension_mod.email_to_link(msg_parsed[x], msg_parsed, user_address) for x in msg_parsed.keys()], [])
		link_parsed         = [link_parser(x) for x in link_parsed]
		link_id             = np.array([x.link_id for x in link_parsed])
		link_parsed         = dict([(x,y) for (x,y) in zip(link_id, link_parsed)])

		print("Successfully completed - link object creation")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		contact_parser      = analysis_msg_class_mod.contact
		contact_list        = list(set([link_parsed[x].link_contact for x in link_id]))
		contact_parsed      = [contact_parser(x, link_parsed, msg_parsed) for x in contact_list]
		contact_parsed      = dict([(x,y) for (x,y) in zip(contact_list, contact_parsed)])

		print("Successfully completed - contact object creation")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1


		# Text Processing
		# -------------------------------------------#	
		
		print("Launching - text analysis ")

		# store message text > msg_text
		msg_id              = msg_parsed.keys()
		msg_text            = [np.array(email_df.loc[email_df['msg_id']==x, 'msg_text'])[0] for x in msg_id]

		# parse message text > msg class
		msg_text_parser     = analysis_msg_class_mod.text
		msg_text_parsed     = [msg_text_parser(x,y) for (x,y) in zip(msg_text, msg_id)]
		msg_text_parsed     = dict([(x,y) for (x,y) in zip(msg_id, msg_text_parsed)])
		
		print("Successfully completed - text analysis")
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# Contact aggregation & labelling
		# -------------------------------------------#	

		print("Launching - contact aggregation & labelling ")

		# contact lists & gender labelling
		agg_contact_df                   = analysis_contact_mod.contact_list(msg_parsed, user_address)
		agg_contact_df['contact_gender'] = analysis_gender_mod.gender_labeler(agg_contact_df['contact_name'],agg_contact_df['contact'])

		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# Generate output
		# -------------------------------------------#	
		
		# basic 
		email_link_df = pd.merge(global_fun_mod.dict_key_df(conver_parsed, "msg_threadid","msg_id"), global_fun_mod.dict_key_df(msg_parsed, "msg_id","link_id"), 
			on='msg_id', how='right')
		email_link_df = email_link_df.reset_index(drop=True, inplace=False)

		# extract data
		conver_data     = global_fun_mod.dict_key_df(conver_parsed, id_name_1="msg_threadid", incl_data=True)
		msg_data        = global_fun_mod.dict_key_df(msg_parsed, id_name_1="msg_id", incl_data=True)
		msg_text_data   = global_fun_mod.dict_key_df(msg_text_parsed, id_name_1="msg_id", incl_data=True)
		link_data       = global_fun_mod.dict_key_df(link_parsed, id_name_1="link_id", incl_data=True)

		# merge
		insight_df      = pd.merge(email_link_df, conver_data, on='msg_threadid', how='left')
		insight_df      = pd.merge(insight_df, msg_data, on='msg_id', how='left')
		insight_df      = pd.merge(insight_df, msg_text_data, on='msg_id', how='left')
		insight_df      = pd.merge(insight_df, link_data, on='link_id', how='left')
		
		global_var['status_analysis_load'] = global_var['status_analysis_load'] + 1

		# save output
		feature_dict = dict(email_link_df=insight_df, agg_contact_df=agg_contact_df,  conver_parsed=conver_parsed, msg_parsed=msg_parsed, msg_text_parsed=msg_text_parsed, link_parsed=link_parsed, contact_parsed=contact_parsed)
		
		with open(feature_dict_file, "wb") as file:
			dill.dump(feature_dict, file)

	# Load previously processed features
	# -------------------------------------------#
	else:

		# load
		with open(feature_dict_file, "rb") as file:
			feature_dict = dill.load(file)
		time.sleep(5)

		# update status
		global_var['status_analysis_load'] = global_var['status_analysis_max']

		
	# Return Output
	# -------------------------------------------#	
	return(feature_dict)

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

