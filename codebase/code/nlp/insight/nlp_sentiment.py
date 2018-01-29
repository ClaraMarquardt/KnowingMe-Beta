## Module    >  nlp_sentiment
## Functions >  sentiment

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import pandas as pd
import numpy as np

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# politeness
#---------------------------------------------#
def sentiment(link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data):
	
	# print("Launching - sentiment")

	"""
				
	"""
	global global_var
	
	# initialize
	sentiment_df_tmp = pd.DataFrame({'link_id':link_id})

	# insight generation successful
	try:
	   	
		# individual word categories
		word_list = np.array([msg_text_data[x].sentiment_count.keys() for x in msg_id])[0]
		
		for word_list_name in word_list:
		
			word_list_col_count             	  = 'sentiment..unigram_bigram_count_' + word_list_name
			word_list_col_set               	  = 'sentiment.__unigram_bigram_set_' + word_list_name
			sentiment_df_tmp[word_list_col_count] = np.array([msg_text_data[x].sentiment_count[word_list_name] for x in msg_id])
			sentiment_df_tmp[word_list_col_set]   = np.array([str(msg_text_data[x].sentiment_set_agg[word_list_name]) for x in msg_id])
			
		# pos / neg
		sentiment_df_tmp['sentiment..pos_msg']    = np.array([msg_text_data[x].sentiment_indic['positive_aggregate'] for x in msg_id])
		sentiment_df_tmp['sentiment..neg_msg']    = np.array([msg_text_data[x].sentiment_indic['negative_aggregate'] for x in msg_id])

	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - sentiment")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("sentiment")

		sentiment_df_tmp = sentiment_df_tmp

	# return
	# print("Successfully Completed - sentiment")
	return(sentiment_df_tmp)

#---------------------------------------------#