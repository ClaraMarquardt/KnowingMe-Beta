## Module    > simplelang 
## Functions > talkative, lengthimbalance

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
from freq import date_freq

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

# talkative
#---------------------------------------------#

def talkative(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data):
	
	# print("Launching - talkative")

	"""

	"""
	global global_var

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

		# append to error list
		global_var['status_feature_error'].append("talkative")

		# character, word, sentence count
		character_count = global_fun.fill_array(len(msg_id), np.nan)
		word_count      = global_fun.fill_array(len(msg_id), np.nan)
		sentence_count  = global_fun.fill_array(len(msg_id), np.nan)


	# format
	talkative_df_tmp = pd.DataFrame({'link_id':link_id, 'talkative..character_count':character_count,'talkative..word_count':word_count, 
		'talkative..sentence_count':sentence_count})

	# return
	# print("Successfully Completed - talkative")
	return(talkative_df_tmp)

# lengthimbalance
#---------------------------------------------#

def lengthimbalance(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data):
	
	# print("Launching - lengthimbalance")

	"""

	"""
	global global_var

	# insight generation successful
	try:
			
		# response time 
		response_link_pair                          = np.array([link_data[x].link_response_id_pair for x in link_id])
		
		# balance
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			length_imbalance_character              = [np.mean([response_balance(y, msg_text_data, 'character_count') for y in x]) for x in response_link_pair]
			length_imbalance_word                   = [np.mean([response_balance(y, msg_text_data, 'word_count') for y in x]) for x in response_link_pair]
			length_imbalance_sentence               = [np.mean([response_balance(y, msg_text_data, 'sentence_count') for y in x]) for x in response_link_pair]


	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - lengthimbalance")
		print(e)
		
		# append to error list
		global_var['status_feature_error'].append("lengthimbalance")

		length_imbalance_character = global_fun.fill_array(len(msg_id), np.nan)
		length_imbalance_word      = global_fun.fill_array(len(msg_id), np.nan)
		length_imbalance_sentence  = global_fun.fill_array(len(msg_id), np.nan)


	# format
	lengthimbalance_df_tmp = pd.DataFrame({'link_id':link_id, 
		'lengthimbalance..length_imbalance_character':length_imbalance_character, 'lengthimbalance..length_imbalance_word':length_imbalance_word,
		'lengthimbalance..length_imbalance_sentence':length_imbalance_sentence})

	# return
	# print("Successfully Completed - lengthimbalance")
	return(lengthimbalance_df_tmp)



# birthday
#---------------------------------------------#

def birthday(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, date_data):

	# print("Launching - birthday")

	"""

	"""
	global global_var

	# insight generation successful
	try:
		birthday_guess   =  date_freq(date_data)
		birthday_guess_1 =  global_fun.fill_array(len(msg_id), birthday_guess[0])
		birthday_guess_2 =  global_fun.fill_array(len(msg_id), birthday_guess[1])
		birthday_guess_3 =  global_fun.fill_array(len(msg_id), birthday_guess[2])
		birthday_guess_4 =  global_fun.fill_array(len(msg_id), birthday_guess[3])
		birthday_guess_5 =  global_fun.fill_array(len(msg_id), birthday_guess[4])
		birthday_guess_1_freq =  global_fun.fill_array(len(msg_id), birthday_guess[5])
		birthday_guess_2_freq =  global_fun.fill_array(len(msg_id), birthday_guess[6])
		birthday_guess_3_freq =  global_fun.fill_array(len(msg_id), birthday_guess[7])
		birthday_guess_4_freq =  global_fun.fill_array(len(msg_id), birthday_guess[8])
		birthday_guess_5_freq =  global_fun.fill_array(len(msg_id), birthday_guess[9])

	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - birthday")
		print(e)
		
		# append to error list
		global_var['status_feature_error'].append("birthday")

		birthday_guess_1 =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_2 =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_3 =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_4 =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_5 =  global_fun.fill_array(len(msg_id), np.nan)

		birthday_guess_1_freq =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_2_freq =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_3_freq =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_4_freq =  global_fun.fill_array(len(msg_id), np.nan)
		birthday_guess_5_freq =  global_fun.fill_array(len(msg_id), np.nan)

	# format
	birthday_df_tmp = pd.DataFrame({'link_id':link_id, 
		'birthday..birthday_guess_1':birthday_guess_1, 'birthday..birthday_guess_2':birthday_guess_2,
		'birthday..birthday_guess_3':birthday_guess_3,'birthday..birthday_guess_4':birthday_guess_4, 
		'birthday..birthday_guess_5':birthday_guess_5,'birthday..birthday_guess_1_freq':birthday_guess_1_freq,
		'birthday..birthday_guess_2_freq':birthday_guess_2_freq,'birthday..birthday_guess_3_freq':birthday_guess_3_freq,
		'birthday..birthday_guess_4_freq':birthday_guess_4_freq, 
		'birthday..birthday_guess_5_freq':birthday_guess_5_freq })

	# return
	# print("Successfully Completed - lengthimbalance")
	return(birthday_df_tmp)

#---------------------------------------------#