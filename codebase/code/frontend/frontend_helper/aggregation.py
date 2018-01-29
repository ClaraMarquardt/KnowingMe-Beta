## Module    > aggregation
## Functions > aggregate_insight, basic_agg, insight_subset, insight_subset_group, hist_agg, agg_id

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..","..")) 

# Dependencies - External
#---------------------------------------------#
import pandas as pd
import numpy as np
import re

#----------------------------------------------------------------------------#
#			                  Function Definition                            #
#----------------------------------------------------------------------------#

# aggregate_insight
#----------------------------------------------------------------------------#

def aggregate_insight(insight_df,insight_type, coord_word_list):

	# print("Launching - aggregate_insight")

	"""
	Perform insight-specific aggregations on an insight data frame

	Arguments:
	* insight_df      - insight df 
	* insight_type    - category of insights which is to be generated

	Returns:
	* insight_dict    - dictionary with insight df versions aggregated at different levels

	"""

	# initialise
	#---------------------------------------------#
	insight_dict = {}
	

	# column dictionary
	#---------------------------------------------#
	global col_dict
	col_dict = dict()

	col_dict["id_col"]   		       = ['msg_id','link_id','msg_threadid']
	col_dict["date_col"]               = ['msg_date','msg_date_date', 'msg_date_week','msg_date_weekday','msg_date_daypart']
	col_dict["responsiveness_col"]     = ['responsiveness..response_time']
	col_dict["talkative_col"]      	   = ['talkative..character_count', 'talkative..word_count', 'talkative..sentence_count']
	col_dict["length_imbalance_col"]   = ['lengthimbalance..length_imbalance_character','lengthimbalance..length_imbalance_word','lengthimbalance..length_imbalance_sentence']
	col_dict["politeness_col"]         = ['politeness..politeness','politeness..politeness_imbalance']
	col_dict["coordination_col"]       = [x for x in insight_df.columns if 'coordination..' in x]

	#---------------------------------------------#
	# generate aggregations
	#---------------------------------------------#

	# aggregate
	# ------------------------------------
	insight_dict['agg_agg']                   	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='agg'))
	insight_dict['agg_sent']                  	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg'))
	insight_dict['agg_received']              	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg'))

	insight_dict['group_a_agg']               	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_a'))
	insight_dict['group_a_sent']              	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a'))
	insight_dict['group_a_received']          	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a'))

	insight_dict['group_b_agg']                  = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_b'))
	insight_dict['group_b_sent']                 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b'))
	insight_dict['group_b_received']          	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b'))

	insight_dict['group_none_agg']            	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_none'))
	insight_dict['group_none_sent']           	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none'))
	insight_dict['group_none_received']       	 = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_none'))

	# conversation related
	# ------------------------------------
	insight_dict['agg_conversation']              = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='agg', conversation='conversation'))
	insight_dict['agg_sent_response']         	  = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg', conversation='response'))
	insight_dict['agg_sent_reply']            	  = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg', conversation='reply'))
	insight_dict['agg_received_response']         = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg', conversation='response'))
	insight_dict['agg_received_reply']        	  = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg', conversation='reply'))

	insight_dict['group_a_conversation']          = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_a', conversation='conversation'))
	insight_dict['group_a_sent_response']         = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a', conversation='response'))
	insight_dict['group_a_sent_reply']            = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a', conversation='reply'))
	insight_dict['group_a_received_response']     = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a', conversation='response'))
	insight_dict['group_a_received_reply']        = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a', conversation='reply'))

	insight_dict['group_b_conversation']          = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_b', conversation='conversation'))
	insight_dict['group_b_sent_response']         = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b', conversation='response'))
	insight_dict['group_b_sent_reply']            = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b', conversation='reply'))
	insight_dict['group_b_received_response']     = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b', conversation='response'))
	insight_dict['group_b_received_reply']        = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b', conversation='reply'))

	insight_dict['group_none_conversation']       = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='all',    group='group_none', conversation='conversation'))
	insight_dict['group_none_sent_response']      = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none', conversation='response'))
	insight_dict['group_none_sent_reply']         = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none', conversation='reply'))
	insight_dict['group_none_received_response']  = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_none', conversation='response'))
	insight_dict['group_none_received_reply']     = basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_none', conversation='reply'))


	# insight specific
	# ------------------------------------
	
	### * nonlang
	if insight_type == "nonlang":

		## first last
		insight_dict['agg_first']         	      					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg', 		   conversation='first'))
		insight_dict['agg_last']          	      					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg', 	       conversation='last'))

		insight_dict['group_a_first']             					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a_msg',    conversation='first'))
		insight_dict['group_a_last']              					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a_msg',    conversation='last'))

		insight_dict['group_b_first']             					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b_msg',    conversation='first'))
		insight_dict['group_b_last']              					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b_msg',    conversation='last'))

		insight_dict['group_none_first']          					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none_msg', conversation='first'))
		insight_dict['group_none_last']           					= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none_msg', conversation='last'))


	elif insight_type == "nlp":

		## politeness
		insight_dict['politeness_agg_request_sent']        	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg',          content='request'))
		insight_dict['politeness_agg_request_received']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg',          content='request'))

		insight_dict['politeness_group_a_request_sent']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a',      content='request'))
		insight_dict['politeness_group_a_request_received']	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a',      content='request'))

		insight_dict['politeness_group_b_request_sent']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b',      content='request'))
		insight_dict['politeness_group_b_request_received']	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b',      content='request'))

		insight_dict['politeness_group_none_request_sent']      	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none',   content='request'))
		insight_dict['politeness_group_none_request_received']  	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='aggroup_none', content='request'))

		## sentiment
		insight_dict['sentiment_agg_pos_sent']        	    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg',        content='pos_msg'))
		insight_dict['sentiment_agg_pos_received']    	    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg',        content='pos_msg'))
		insight_dict['sentiment_agg_neg_sent']        	    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg',        content='neg_msg'))
		insight_dict['sentiment_agg_neg_received']    	    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='agg', 		  content='neg_msg'))

		insight_dict['sentiment_group_a_pos_sent']        	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a',    content='pos_msg'))
		insight_dict['sentiment_group_a_pos_received']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a',    content='pos_msg'))
		insight_dict['sentiment_group_a_neg_sent']        	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_a',    content='neg_msg'))
		insight_dict['sentiment_group_a_neg_received']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_a', 	  content='neg_msg'))

		insight_dict['sentiment_group_b_pos_sent']        	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b', 	  content='pos_msg'))
		insight_dict['sentiment_group_b_pos_received']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b', 	  content='pos_msg'))
		insight_dict['sentiment_group_b_neg_sent']        	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_b', 	  content='neg_msg'))
		insight_dict['sentiment_group_b_neg_received']    	    	= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_b', 	  content='neg_msg'))

		insight_dict['sentiment_group_none_pos_sent']        		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none', content='pos_msg'))
		insight_dict['sentiment_group_none_pos_received']    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_none', content='pos_msg'))
		insight_dict['sentiment_group_none_neg_sent']        		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='group_none', content='neg_msg'))
		insight_dict['sentiment_group_none_neg_received']    		= basic_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox',  group='group_none', content='neg_msg'))

		insight_dict['sentiment_agg_breakdown_agg']        	        = hist_agg(insight_df, agg_id(insight_df, inbox_outbox='all', group='agg'), "sentiment..unigram_bigram_count_","aggregate")
		insight_dict['sentiment_agg_breakdown_sent']        	    = hist_agg(insight_df, agg_id(insight_df, inbox_outbox='outbox', group='agg'), "sentiment..unigram_bigram_count_", "aggregate")
		insight_dict['sentiment_agg_breakdown_received']        	= hist_agg(insight_df, agg_id(insight_df, inbox_outbox='inbox', group='agg'), "sentiment..unigram_bigram_count_","aggregate")

		# coordination
		for i in coord_word_list:

			insight_dict['coordination_agg_' + i + '_sent']        			= basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='agg',        other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_a_' + i + '_sent']       		= basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_a',    other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_b_' + i + '_sent']       		= basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_b',    other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_none_' + i + '_sent']    		= basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_none', other=['coordination..pos_indic_'+i]))
	
			insight_dict['coordination_agg_' + i + '_reply_sent']        	= basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='agg',        conversation="reply", other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_a_' + i + '_reply_sent']       = basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_a',    conversation="reply", other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_b_' + i + '_reply_sent']       = basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_b',    conversation="reply", other=['coordination..pos_indic_'+i]))
			insight_dict['coordination_group_none_' + i + '_reply_sent']    = basic_agg(insight_df,agg_id(insight_df, inbox_outbox='outbox', group='group_none', conversation="reply", other=['coordination..pos_indic_'+i]))


	# return
	# ------------------------------------
	return(insight_dict)


# basic_agg
#----------------------------------------------------------------------------#

def basic_agg(df, link_id_list):

	# print("Launching - basic_agg")

	"""
	Perform basic aggregations on an insight data frame

	Arguments:
	* df                - insight df 
	* link_id_list      - list of link_ids corresponding to the links which are to be considered

	Returns:
	* dict_tmp          - dictionary with insight df versions aggregated at different levels

	"""
	global col_dict

	# initialize
	df_link     = df.loc[df['link_id'].apply(lambda x: x in link_id_list)]
	dict_tmp    = {}

	# sort
	df_link     = df_link.sort_values(by=['msg_threadid','msg_date'], ascending=[True,True])

	# aggregate (note - by default keep 1st (earliest) occurence)
	unique_link                  		             = insight_subset(df_link.drop_duplicates('link_id'))
	unique_msg                   		             = insight_subset(df_link.drop_duplicates('msg_id'))
	unique_thread_start                  			 = insight_subset(df_link.drop_duplicates('msg_threadid'))                                 
	unique_thread_ongoing                			 = insight_subset(df_link.drop_duplicates(['msg_threadid', 'msg_date_date']))                                 
	
	dict_tmp['unique_link_date']                     = insight_subset_group(unique_link.groupby('msg_date_date').agg('count'))
	dict_tmp['unique_link_week']                     = insight_subset_group(unique_link.groupby('msg_date_week').agg('count'))
	dict_tmp['unique_link_weekday']                  = insight_subset_group(unique_link.groupby('msg_date_weekday').agg('count'))
	dict_tmp['unique_link_dayperiod']                = insight_subset_group(unique_link.groupby('msg_date_daypart').agg('count'))
		
	dict_tmp['unique_msg_date']              		 = insight_subset_group(unique_msg.groupby('msg_date_date').agg('count'))
	dict_tmp['unique_msg_week']              		 = insight_subset_group(unique_msg.groupby('msg_date_week').agg('count'))
	dict_tmp['unique_msg_weekday']                   = insight_subset_group(unique_msg.groupby('msg_date_weekday').agg('count'))
	dict_tmp['unique_msg_dayperiod']         		 = insight_subset_group(unique_msg.groupby('msg_date_daypart').agg('count'))
		
	dict_tmp['unique_thread_start_date']           	 = insight_subset_group(unique_thread_start.groupby('msg_date_date').agg('count'))
	dict_tmp['unique_thread_start_week']           	 = insight_subset_group(unique_thread_start.groupby('msg_date_week').agg('count'))
	dict_tmp['unique_thread_start_weekday']          = insight_subset_group(unique_thread_start.groupby('msg_date_weekday').agg('count'))
	dict_tmp['unique_thread_start_dayperiod']      	 = insight_subset_group(unique_thread_start.groupby('msg_date_daypart').agg('count'))

	dict_tmp['unique_thread_ongoing_date']           = insight_subset_group(unique_thread_ongoing.groupby('msg_date_date').agg('count'))
	dict_tmp['unique_thread_ongoing_week']           = insight_subset_group(unique_thread_ongoing.groupby('msg_date_week').agg('count'))
	dict_tmp['unique_thread_ongoing_weekday']        = insight_subset_group(unique_thread_ongoing.groupby('msg_date_weekday').agg('count'))
	dict_tmp['unique_thread_ongoing_dayperiod']      = insight_subset_group(unique_thread_ongoing.groupby('msg_date_daypart').agg('count'))
	
	# additional output - talkative insight
	dict_tmp['unique_msg_date_length']               = unique_msg.groupby('msg_date_date').agg('median')[col_dict['talkative_col']]
	dict_tmp['unique_msg_date_length']['date_index'] = dict_tmp['unique_msg_date_length'].index
	dict_tmp['unique_msg_date_length'].reset_index(drop=True, inplace=True)

	dict_tmp['unique_msg_week_length']               = unique_msg.groupby('msg_date_week').agg('median')[col_dict['talkative_col']]
	dict_tmp['unique_msg_week_length']['date_index'] = dict_tmp['unique_msg_week_length'].index
	dict_tmp['unique_msg_week_length'].reset_index(drop=True, inplace=True)

	dict_tmp['unique_msg_weekday_length']               = unique_msg.groupby('msg_date_weekday').agg('median')[col_dict['talkative_col']]
	dict_tmp['unique_msg_weekday_length']['date_index'] = dict_tmp['unique_msg_weekday_length'].index
	dict_tmp['unique_msg_weekday_length'].reset_index(drop=True, inplace=True)
	
	dict_tmp['unique_msg_dayperiod_length']               = unique_msg.groupby('msg_date_daypart').agg('median')[col_dict['talkative_col']]
	dict_tmp['unique_msg_dayperiod_length']['date_index'] = dict_tmp['unique_msg_dayperiod_length'].index
	dict_tmp['unique_msg_dayperiod_length'].reset_index(drop=True, inplace=True)

	# additional output - politeness insight
	dict_tmp['unique_msg_date_politeness']               = unique_msg.groupby('msg_date_date').agg('mean')[['politeness..politeness']]
	dict_tmp['unique_msg_date_politeness']['date_index'] = dict_tmp['unique_msg_date_politeness'].index
	dict_tmp['unique_msg_date_politeness'].reset_index(drop=True, inplace=True)

	dict_tmp['unique_msg_week_politeness']               = unique_msg.groupby('msg_date_week').agg('mean')[['politeness..politeness']]
	dict_tmp['unique_msg_week_politeness']['date_index'] = dict_tmp['unique_msg_week_politeness'].index
	dict_tmp['unique_msg_week_politeness'].reset_index(drop=True, inplace=True)

	dict_tmp['unique_msg_weekday_politeness']               = unique_msg.groupby('msg_date_weekday').agg('mean')[['politeness..politeness']]
	dict_tmp['unique_msg_weekday_politeness']['date_index'] = dict_tmp['unique_msg_weekday_politeness'].index
	dict_tmp['unique_msg_weekday_politeness'].reset_index(drop=True, inplace=True)
	
	dict_tmp['unique_msg_dayperiod_politeness']               = unique_msg.groupby('msg_date_daypart').agg('mean')[['politeness..politeness']]
	dict_tmp['unique_msg_dayperiod_politeness']['date_index'] = dict_tmp['unique_msg_dayperiod_politeness'].index
	dict_tmp['unique_msg_dayperiod_politeness'].reset_index(drop=True, inplace=True)


	# aggregate & format
	dict_tmp['unique_link']                          = pd.DataFrame({"id_index":unique_link.link_id, 'date_index':unique_link.msg_date, 'responsiveness..response_time':unique_link['responsiveness..response_time']})

	unique_msg_col = sum([col_dict['talkative_col'],col_dict['length_imbalance_col'],col_dict['politeness_col'], col_dict['coordination_col']], [])
	unique_msg_col = sum([unique_msg_col,['link_id','msg_date']], [])
	unique_msg_tmp = unique_msg[np.array(unique_msg_col)]
	unique_msg_tmp = unique_msg_tmp.rename(columns={'link_id':'id_index', 'msg_date':'date_index'}, inplace=False)
	dict_tmp['unique_msg']  = unique_msg_tmp                  

	dict_tmp['unique_thread_start']                  = pd.DataFrame({"id_index":unique_thread_start.link_id, 'date_index':unique_thread_start.msg_date})
	dict_tmp['unique_thread_ongoing']                = pd.DataFrame({"id_index":unique_thread_ongoing.link_id, 'date_index':unique_thread_ongoing.msg_date})

	# return
	return(dict_tmp)


# hist_agg
#----------------------------------------------------------------------------#

def hist_agg(df, link_id_list, col_pattern,col_pattern_exclude):

	# print("Launching - basic_agg")

	"""

	"""
	
	global col_dict

	# initialize
	df          = df.loc[df['link_id'].apply(lambda x: x in link_id_list)]

	# identify the key columns
	key_col = [x for x in df.columns if col_pattern in x and col_pattern_exclude not in x]

	# initialize
	key_col_count = []

	# loop
	for col in key_col:

		df_tmp             = df.loc[df[col]>0, 'msg_id'].unique()
		key_col_unique_msg = len(df_tmp)
		if (key_col_unique_msg==0):
			key_col_unique_msg=np.nan
		key_col_count.append(key_col_unique_msg)

	dict_tmp = pd.DataFrame({'key_col':key_col, 'key_col_count':key_col_count})
	dict_tmp['key_col']       = [re.sub("(.*)_([^_]*$)","\\2", x) for x in dict_tmp['key_col']]
	dict_tmp['key_col_count'] = [float(x)/max(dict_tmp['key_col_count']) for x in dict_tmp['key_col_count']]

	dict_tmp.sort_values(by=['key_col_count'], ascending=[False],inplace=True)

	# return
	return(dict_tmp)


# insight_subset
#----------------------------------------------------------------------------#

def insight_subset(df):

	# print("Launching - insight_subset")

	"""
	Subset an insight data frame to a selected number of key columns

	Arguments:
	* df           - original df

	Returns:
	* df_subset    - subset df

	"""
	global col_dict

	# initialize
	df_subset  = df

	
	# subset	
	keep_col  = np.array(sum([col_dict['id_col'],col_dict['date_col'],col_dict['responsiveness_col'], col_dict['talkative_col'],col_dict['length_imbalance_col'],col_dict['politeness_col'],col_dict['coordination_col']],[]))
	
	df_subset = df[keep_col]
	df_subset.reset_index(drop=True, inplace=True)

	return(df_subset)


# insight_subset_group
#----------------------------------------------------------------------------#

def insight_subset_group(df):

	# print("Launching - insight_subset_group")

	"""
	Subset an insight data frame to a selected number of key columns (applies to a grouped data frame)

	Arguments:
	* df           - original df

	Returns:
	* df_subset    - subset df

	"""
	global col_dict

	# subset
	df_subset  = pd.DataFrame({"date_index":df.index, 'id_index':df.iloc[:,1]})
	df_subset.reset_index(drop=True, inplace=True)

	return(df_subset)

# agg_id
#----------------------------------------------------------------------------#

def agg_id(df, inbox_outbox, group, conversation=None, content=None,other=None,  unit='link'):

	# print("Launching - agg_id")

	"""

	"""
	global col_dict

	# initialize
	df_tmp = df

	# inbox_outbox
	if inbox_outbox=='all':

		df_tmp = df_tmp

	elif inbox_outbox=='inbox':

		df_tmp = df_tmp.loc[df_tmp['flag.inbox_outbox']=='inbox']

	elif inbox_outbox=='outbox':

		df_tmp = df_tmp.loc[df_tmp['flag.inbox_outbox']=='outbox']

	# group
	if group=='agg':

		df_tmp = df_tmp

	elif group=='group_a':

		df_tmp = df_tmp.loc[df_tmp['flag.group']=='group_a']

	elif group=='group_b':

		df_tmp = df_tmp.loc[df_tmp['flag.group']=='group_b']

	elif group=='group_none':

		df_tmp = df_tmp.loc[df_tmp['flag.group']=='group_na']

	elif group=='group_a_msg':

		df_tmp = df_tmp.loc[df_tmp['flag.group_msg'].str.contains('group_a')]

	elif group=='group_b_msg':

		df_tmp = df_tmp.loc[df_tmp['flag.group_msg'].str.contains('group_b')]

	elif group=='group_none_msg':	

		df_tmp = df_tmp.loc[df_tmp['flag.group_msg'].str.contains('group_na')]

	# conversation
	if pd.notnull(conversation):

		if 'conversation' in conversation:

			df_tmp = df_tmp.loc[df_tmp['firstlast.__conversation']==1]

		if 'first' in conversation:

			df_tmp = df_tmp.loc[(df_tmp['firstlast..first']==1) & (df_tmp['firstlast.__conversation']==1)]

		if 'last' in conversation:

			df_tmp = df_tmp.loc[(df_tmp['firstlast..last']==1) & (df_tmp['firstlast.__conversation']==1)]

		if 'reply' in conversation:

			df_tmp = df_tmp.loc[df_tmp['responsiveness..reply']==1]

		if 'response' in conversation:

			df_tmp = df_tmp.loc[df_tmp['responsiveness..response']==1]

	# content
	if pd.notnull(content):

		if 'request' in content:

			df_tmp = df_tmp.loc[df_tmp['politeness..request']==1]

		if 'pos_msg' in content:

			df_tmp = df_tmp.loc[df_tmp['sentiment..pos_msg']==1]

		if 'neg_msg' in content:

			df_tmp = df_tmp.loc[df_tmp['sentiment..neg_msg']==1]

	if pd.notnull(other):

		df_tmp = df_tmp.loc[df_tmp[other[0]]==1]

	# subset
	if unit=='link':

		df_tmp_id = df_tmp['link_id'].unique()

	elif group=='msg':

		df_tmp_id = df_tmp['msg_id'].unique()


	return(df_tmp_id)

#----------------------------------------------------------------------------#




