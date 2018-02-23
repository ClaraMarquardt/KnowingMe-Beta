# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_load_mod
# Purpose:      Module - Define load analysis functions
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
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','analysis')))
from analysis_helper import analysis_clean_mod

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#


# load_email
#---------------------------------------------#

def load_email(file_array, verbose=True):
	
	# print("Launching - load_email")

	"""
		
	"""

	# initialize arrays
	msg_id       		  = []
	msg_id_mime      	  = []
	msg_reply_to_id_mime  = []
	msg_threadid  	 	  = []
	msg_date     	 	  = []
	msg_to       	 	  = []
	msg_from     	 	  = []
	msg_cc       	 	  = []
	msg_bcc      	 	  = []
	msg_subject      	  = []
	msg_text     	 	  = []
	msg_label     	 	  = []
	msg_inbox_outbox      = []

	# loop over 'file_array' > load and parse json files 
	for i in range(0,len(file_array)):

		file_path = file_array[i]
		
		# loading successful
		try:	
		
			# load
			data = pickle.load(open(file_path, "rb" ) )

			# parse
			msg_id_tmp            	   = str(data['msg_id'])
			msg_id_mime_tmp      	   = str(data['msg_id_mime'])
			msg_reply_to_id_mime_tmp   = str(data['msg_reply_to_id_mime'])
			msg_threadid_tmp      	   = str(data['msg_threadid'])
			msg_date_tmp          	   = analysis_clean_mod.clean_date(data['msg_date'])
			
			msg_label_tmp         	   = [str(x) for x in data['msg_label']]
			msg_inbox_outbox_tmp       = str(data['msg_inbox_outbox'])

			msg_to_tmp            	   = str(data['msg_to'])
			msg_from_tmp      	  	   = str(data['msg_from'])
			msg_cc_tmp        	  	   = str(data['msg_cc'])
			msg_bcc_tmp       	  	   = str(data['msg_bcc'])
	
			msg_subject_tmp       	   = str(data['msg_subject'].decode("utf-8","ignore").encode("utf-8"))
			msg_text_tmp          	   = str(data['msg_text'].decode("utf-8","ignore").encode("utf-8"))

			# append
			msg_id.append(msg_id_tmp)
			msg_id_mime.append(msg_id_mime_tmp)
			msg_reply_to_id_mime.append(msg_reply_to_id_mime_tmp)
			msg_threadid.append(msg_threadid_tmp)
			msg_date.append(msg_date_tmp)
			msg_to.append(msg_to_tmp)
			msg_from.append(msg_from_tmp)
			msg_cc.append(msg_cc_tmp)
			msg_bcc.append(msg_bcc_tmp)
			msg_subject.append(msg_subject_tmp)
			msg_text.append(msg_text_tmp)
			msg_label.append(msg_label_tmp)
			msg_inbox_outbox.append(msg_inbox_outbox_tmp)

		# loading unsuccessful
		except Exception as e: 

			if verbose==True:
				
				# error message
				print("Error Encountered - load_email")
				print(e)
				print(file_path)

	# combine arrays > data.frame 
	email_df = pd.DataFrame({'msg_id':msg_id, 'msg_threadid':msg_threadid,
		'msg_date':msg_date, 'msg_to':msg_to,'msg_from':msg_from,
		'msg_cc':msg_cc,'msg_bcc':msg_bcc,
		'msg_subject':msg_subject,'msg_label':msg_label,'msg_text':msg_text, 
		'msg_id_mime':msg_id_mime,'msg_reply_to_id_mime':msg_reply_to_id_mime, 
		'msg_inbox_outbox': msg_inbox_outbox})

	# drop invalid emails
	email_df = omit_invalid(email_df,file_array)
	
	# order
	email_df = email_df.sort_values(by=['msg_threadid', 'msg_date'], ascending=[True,True])
	email_df = email_df.reset_index(drop=True, inplace=False)


	# return
	# print("Successfully Completed - load_email")
	return(email_df)


# omit_invalid
#---------------------------------------------#

def omit_invalid(df,file_array):

	# print("Launching - omit_invalid")

	"""
		
	"""

	## [0] omit > unable to load
	print("[0] Omit (Unable to Load Json): " + str(len(file_array)-len(df)))

	## [1] omit > missing ids
	print("[1] Omit (Missing IDs): " + str(len(df.loc[pd.isnull(df['msg_id'])])))
	df = df.loc[pd.notnull(df['msg_id'])]
	
	## [2] omit > missing/invalid dates
	print("[2] Omit (Missing/Invalid Dates): " + str(len(df.loc[df['msg_date'] == pd.to_datetime(datetime.datetime(1990, 1, 1, 1, 1, 1),errors='ignore',utc=True)])))
	df = df.loc[~(df['msg_date']== pd.to_datetime(datetime.datetime(1990, 1, 1, 1, 1, 1),errors='ignore',utc=True))]


	# return
	# print("Successfully Completed - omit_invalid")
	return(df)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#