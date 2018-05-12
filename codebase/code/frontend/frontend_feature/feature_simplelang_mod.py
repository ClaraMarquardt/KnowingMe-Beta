# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_simplelang_mod
# Purpose:      Module - Define simplelang insight functions
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
from analysis_conver_mod import response_balance
from analysis_freq_mod import date_freq

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#


# language
#---------------------------------------------#
def language_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - language")

	"""

	"""

	# insight generation successful
	try:

		# character, word, sentence count
		language = np.array([msg_text_data[x].lang for x in msg_id])
		english  = np.array([msg_text_data[x].eng for x in msg_id])
	
	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - language")
		print(e)

		# character, word, sentence count
		language = global_fun_mod.fill_array(len(msg_id), np.nan)
		english  = global_fun_mod.fill_array(len(msg_id), np.nan)

	# format
	language_df_tmp = pd.DataFrame({'link_id':link_id, 'language..language':language,'language..english':english})

	# return
	# print("Successfully Completed - language")
	return(language_df_tmp)

# talkative
#---------------------------------------------#

def talkative_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - talkative")

	"""

	"""

	# insight generation successful
	try:

		# character, word, sentence count
		character_count = np.array([msg_text_data[x].character_count for x in msg_id])
		word_count      = np.array([msg_text_data[x].word_count for x in msg_id])
		sentence_count  = np.array([msg_text_data[x].sentence_count for x in msg_id])
	
	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - talkative")
		print(e)

		# character, word, sentence count
		character_count = global_fun_mod.fill_array(len(msg_id), np.nan)
		word_count      = global_fun_mod.fill_array(len(msg_id), np.nan)
		sentence_count  = global_fun_mod.fill_array(len(msg_id), np.nan)


	# format
	talkative_df_tmp = pd.DataFrame({'link_id':link_id, 'talkative..character_count':character_count,'talkative..word_count':word_count, 
		'talkative..sentence_count':sentence_count})

	# return
	# print("Successfully Completed - talkative")
	return(talkative_df_tmp)

# lengthimbalance
#---------------------------------------------#

def lengthimbalance_feature(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date, contact_df):
	
	# print("Launching - lengthimbalance")

	"""

	"""

	# insight generation successful
	try:
			
		# response time 
		response_link_pair                          = np.array([link_data[x].link_response_id_pair for x in link_id])
		
		# balance
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			length_imbalance_character              = [np.nanmean([response_balance(y, msg_text_data, 'character_count') for y in x]) for x in response_link_pair]
			length_imbalance_word                   = [np.nanmean([response_balance(y, msg_text_data, 'word_count') for y in x]) for x in response_link_pair]
			length_imbalance_sentence               = [np.nanmean([response_balance(y, msg_text_data, 'sentence_count') for y in x]) for x in response_link_pair]


	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - lengthimbalance")
		print(e)
		
		length_imbalance_character = global_fun_mod.fill_array(len(msg_id), np.nan)
		length_imbalance_word      = global_fun_mod.fill_array(len(msg_id), np.nan)
		length_imbalance_sentence  = global_fun_mod.fill_array(len(msg_id), np.nan)


	# format
	lengthimbalance_df_tmp = pd.DataFrame({'link_id':link_id, 
		'lengthimbalance..length_imbalance_character':length_imbalance_character, 'lengthimbalance..length_imbalance_word':length_imbalance_word,
		'lengthimbalance..length_imbalance_sentence':length_imbalance_sentence})

	# return
	# print("Successfully Completed - lengthimbalance")
	return(lengthimbalance_df_tmp)





#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
