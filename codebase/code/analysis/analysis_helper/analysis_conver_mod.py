# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_conver_mod
# Purpose:      Module - Define conversation analysis functions
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
app_root             = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *
from __init_setting__ import *

# Dependencies - Internal
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#


# response_structure
#---------------------------------------------#

def response_structure(df):
	
	# print("Launching - response_structure")

	"""

	"""

	# initialize
	# ----------------

	## map mime to gmail ids (reply to id)
	mime_id_xwalk                 = df[['msg_id', 'msg_id_mime']].drop_duplicates()
	mime_id_xwalk.columns         = np.array(['msg_reply_id', 'msg_reply_to_id_mime'])
	df                      	  = pd.merge(df, mime_id_xwalk, on='msg_reply_to_id_mime', how='left') 
	df                            = df.drop(['msg_id_mime', 'msg_reply_to_id_mime'], axis=1, inplace=False)
	df['msg_reply_id']            = [str(x) for x in df['msg_reply_id']]

	## ensure that reply ids are in dataset
	df.loc[df['msg_reply_id'].apply(lambda x: x in df['msg_id']), 'msg_reply_id'] = str(np.nan)

	## sort & re-index 
	df['id_tmp']  				  = range(0, len(df))

	# response analysis successful 
	try: 

		# determine the 'msg_response_id', 'msg_response_inbox_outbox', 'msg_reply_inbox_outbox'
		
		## response link
		df_xwalk 			  = df[['msg_id', 'msg_reply_id', 'msg_inbox_outbox']].drop_duplicates()
		df_xwalk.columns      = np.array(['msg_response_id', 'msg_id','msg_response_inbox_outbox'])
		df_xwalk              = df_xwalk.loc[pd.notnull(df_xwalk['msg_id'])]
		df                    = pd.merge(df, df_xwalk, on='msg_id', how='left') 
		df['msg_response_id'] = [str(x) for x in df['msg_response_id']]

		## reply link
		df_xwalk 			  = df[['msg_id', 'msg_inbox_outbox']].drop_duplicates()
		df_xwalk.columns      = np.array(['msg_reply_id','msg_reply_inbox_outbox'])
		df_xwalk              = df_xwalk.loc[pd.notnull(df_xwalk['msg_reply_id'])]
		df                    = pd.merge(df, df_xwalk, on='msg_reply_id', how='left') 

		# impose conditions - response (a) inbox (msg): response == outbox & (b) outbox (msg): response == inbox
		df.loc[((pd.notnull(df['msg_response_id'])) & (df['msg_inbox_outbox']=='inbox') & (df['msg_response_inbox_outbox']=='inbox')), 'msg_response_id'] = str(np.nan)
		df.loc[((pd.notnull(df['msg_response_id'])) & (df['msg_inbox_outbox']=='outbox') & (df['msg_response_inbox_outbox']=='outbox')), 'msg_response_id'] = str(np.nan)

		# impose conditions - reply (a) inbox (msg): reply == outbox & (b) outbox (msg): reply == inbox
		df.loc[((pd.notnull(df['msg_reply_id'])) & (df['msg_inbox_outbox']=='inbox') & (df['msg_reply_inbox_outbox']=='inbox')), 'msg_reply_id'] = str(np.nan)
		df.loc[((pd.notnull(df['msg_reply_id'])) & (df['msg_inbox_outbox']=='outbox') & (df['msg_reply_inbox_outbox']=='outbox')), 'msg_reply_id'] = str(np.nan)

		# drop and combine (one msg > potentially multiple responses (msg_response_id) (vs. only one msg_reply_id))
		df   		   		  = df.drop(['msg_response_inbox_outbox','msg_reply_inbox_outbox'], axis=1, inplace=False)
		temp 		   		  = pd.DataFrame(df.groupby('msg_id')['msg_response_id'].apply(lambda x: np.array([y for y in x if y!="nan"])))
		temp['msg_id'] 		  = temp.index
		temp				  = temp.drop_duplicates('msg_id')
		df   		   		  = df.drop(['msg_response_id'], axis=1, inplace=False)
		df             		  = pd.merge(df, temp, on=['msg_id'], how='inner')
		df   		   		  = df.drop_duplicates('msg_id')

	# response analysis unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - response_structure")
		print(e)

		df['msg_response_id']     = global_fun_mod.fill_array(len(df), [np.nan])

	# format (original order)
	df        = df.sort_values(by=['id_tmp'], ascending=[True])
	df        = df.drop(['id_tmp'],axis=1, inplace=False)


	# return
	# print("Successfully Completed - response_structure")
	return(df)

# conver_timediff
#---------------------------------------------#

def conver_timediff(msg_id_pair, msg_data):

	# print("Launching - conver_timediff")

	"""

	"""
	time_msg      				   = msg_data[msg_id_pair[0]].date['msg_date']
	time_msg_response              = msg_data[msg_id_pair[1]].date['msg_date']
	timediff    				   = pd.to_datetime(time_msg_response) - pd.to_datetime(time_msg)
	timediff    				   = pd.Timedelta(timediff).seconds/60

	# return
	# print("Successfully Completed - conver_timediff")
	return(timediff)


# response_balance
#---------------------------------------------#

def response_balance(msg_id_pair, data_obj, attr_name):
	
	# print("Launching - response_balance")

	"""

	"""

	# initialise
	attr_msg      					= getattr(data_obj[msg_id_pair[0]],attr_name)
	attr_msg_response       		= getattr(data_obj[msg_id_pair[1]],attr_name)
	if attr_msg!=0:
		attr_ratio  				= float(attr_msg_response)/attr_msg
	else:
		attr_ratio  				= np.nan

	# return
	# print("Successfully Completed - response_balance")
	return(attr_ratio)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
