# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_nlp_mod
# Purpose:      Module - Define nlp insight functions
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
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_helper')))
from analysis_coordination_mod import coordination_score

sys.path.append(os.path.normpath(os.path.join(app_root, 'code','analysis','analysis_helper')))
from analysis_conver_mod import response_balance

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# sentiment
#---------------------------------------------#
def sentiment(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date):
	
	# print("Launching - sentiment")

	"""
				
	"""
	
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

		sentiment_df_tmp = sentiment_df_tmp

	# return
	# print("Successfully Completed - sentiment")
	return(sentiment_df_tmp)

# politeness
#---------------------------------------------#
def politeness(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_datea):
	
	# print("Launching - politeness")

	"""
				
	"""

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
		
		request            	= global_fun_mod.fill_array(len(msg_id), np.nan)
		politeness         	= global_fun_mod.fill_array(len(msg_id), np.nan)
		request_agg        	= global_fun_mod.fill_array(len(msg_id), np.nan)
		politeness_balance 	= global_fun_mod.fill_array(len(msg_id), np.nan)

	# format
	politeness_df_tmp = pd.DataFrame({'link_id':link_id, 'politeness..politeness':politeness,'politeness..politeness_imbalance':politeness_balance,'politeness..request_sentence':request, 'politeness..request':request_agg})

	# return
	# print("Successfully Completed - politeness")
	return(politeness_df_tmp)

# coordination
#---------------------------------------------#
def coordination(email_link_df, link_id, msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data, email_date_df, current_date):
	
	# print("Launching - coordination")

	"""
				
	"""

	# initialize
	coordination_df_tmp = pd.DataFrame({'link_id':link_id})

	# insight generation successful
	try:
	
		# individual word categories
		word_list = np.array([msg_text_data[x].pos_count.keys() for x in msg_id])[0]

		# contact level aggregates
		link_contact                             	   = list(set([contact_data[link_data[x].link_contact].contact_id for x in link_id]))
		link_contact_link_id                     	   = [contact_data[x].link_id_outbox for x in link_contact]

		link_contact_coordination_score          	   = [coordination_score(x, link_data, msg_text_data, word_list) for x in link_contact_link_id]
		link_contact_coordination_score_dict     	   = dict([(x,y) for (x,y) in zip(link_contact, link_contact_coordination_score)])
 		
		# message/link itself - message level identifiers
		for word_list_name in word_list:
			
			word_list_col_count             	       = 'coordination..pos_count_' + word_list_name
			word_list_col_prop             	           = 'coordination..pos_prop_' + word_list_name
			word_list_col_indic             	       = 'coordination..pos_indic_' + word_list_name
			word_list_col_score               	       = 'coordination..score_' + word_list_name
			word_list_col_set               	       = 'coordination.__pos_set_' + word_list_name
			
			coordination_df_tmp[word_list_col_count]   = np.array([msg_text_data[x].pos_count[word_list_name] for x in msg_id])
			coordination_df_tmp[word_list_col_indic]   = np.array([msg_text_data[x].pos_indic[word_list_name] for x in msg_id])
			coordination_df_tmp[word_list_col_set]     = np.array([str(msg_text_data[x].pos_set_agg[word_list_name]) for x in msg_id])
			coordination_df_tmp[word_list_col_prop]    = np.array([global_fun_mod.perc(msg_text_data[x].pos_count[word_list_name], msg_text_data[x].word_count) for x in msg_id])

			coordination_df_tmp[word_list_col_score]   = np.array([link_contact_coordination_score_dict[link_data[x].link_contact][word_list_name] for x in link_id])

		## aggregate coordination
		coordination_df_tmp['coordination..score_agg'] = np.array([link_contact_coordination_score_dict[link_data[x].link_contact]['agg_coordination'] for x in link_id])

	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - coordination")
		print(e)
		
		coordination_df_tmp              		     = coordination_df_tmp

	# return
	# print("Successfully Completed - coordination")
	return(coordination_df_tmp)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
