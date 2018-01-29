#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Insight Interface Script
# Date:        August 2017
# Language:    Python (.py) [ Python 2.7 ]

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Modules
from insight import * 
from nlp_helper import *  

sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init__ import *
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import pandas as pd
import numpy as np
import datetime

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# insight_generation
#---------------------------------------------#

def insight_generation(email_file_array, email_file_array_other, user_address):
	
	global global_var

	start_time = datetime.datetime.now()
	global_var['status_feature']=0
	
	print("Launching - insight_generation")

	"""
	
	"""

	# Import & basic processing > email_df
	# -------------------------------------------#
	# -------------------------------------------#	

	# load
	# ---------------------------#	

	print("Emails - files: " + str(len(email_file_array)))

	print("Launch - load")
	email_df             		  = load.load_email(email_file_array)

	print("Launch - load (other data)")
	email_df_date                 = load.load_date(email_file_array_other, verbose=False)
	
	## status
	print("Emails - loaded: " + str(len(email_df)))

	global_var['status_feature']=1
	print("Successfully completed - loading")


	# response structure
	# ---------------------#	
	email_df = conver.response_structure(email_df)

	global_var['status_feature']=2
	print("Successfully completed - response_structure")

	# Message & Conversation Processing > objects
	# -------------------------------------------#	
	# -------------------------------------------#	

	# parse conversations
	conver_parser       = msg_class.conver
	msg_threadid        = np.unique(np.array(email_df['msg_threadid']))
	conver_parsed       = [conver_parser(email_df.loc[email_df['msg_threadid']==x]) for x in msg_threadid]
	conver_parsed       = dict([(x,y) for (x,y) in zip(msg_threadid, conver_parsed)])

	global_var['status_feature']=3
	print("Successfully completed - conversation object creation")

	# parse messages (1)
	msg_parser          = msg_class.msg
	msg_id              = np.unique(np.array(email_df['msg_id']))
	msg_parsed          = [msg_parser(email_df.loc[email_df['msg_id']==x], conver_parsed) for x in msg_id]
	msg_parsed          = dict([(x,y) for (x,y) in zip(msg_id, msg_parsed)])

	global_var['status_feature']=4
	print("Successfully completed - message object creation")

	# parse links 
	link_parser         = msg_class.link
	link_parsed         = sum([dimension.email_to_link(msg_parsed[x], msg_parsed, user_address) for x in msg_parsed.keys()], [])
	link_parsed         = [link_parser(x) for x in link_parsed]
	link_id             = np.array([x.link_id for x in link_parsed])
	link_parsed         = dict([(x,y) for (x,y) in zip(link_id, link_parsed)])

	global_var['status_feature']=5
	print("Successfully completed - link object creation")

	contact_parser      = msg_class.contact
	contact_list        = list(set([link_parsed[x].link_contact for x in link_id]))
	contact_parsed      = [contact_parser(x, link_parsed, msg_parsed) for x in contact_list]
	contact_parsed      = dict([(x,y) for (x,y) in zip(contact_list, contact_parsed)])

	global_var['status_feature']=6
	print("Successfully completed - contact object creation")


	# Text Processing
	# -------------------------------------------#	
	# -------------------------------------------#	
	
	print("Launching - text analysis ")

	# store message text > msg_text
	msg_id              = msg_parsed.keys()
	msg_text            = [np.array(email_df.loc[email_df['msg_id']==x, 'msg_text'])[0] for x in msg_id]

	# parse message text > msg class
	msg_text_parser     = msg_class.text
	msg_text_parsed     = [msg_text_parser(x,y) for (x,y) in zip(msg_text, msg_id)]
	msg_text_parsed     = dict([(x,y) for (x,y) in zip(msg_id, msg_text_parsed)])
	
	global_var['status_feature']=7
	print("Successfully completed - text analysis")

	# Contact aggregation & labelling
	# -------------------------------------------#	
	# -------------------------------------------#	

	# contact lists & gender labelling
	print("Launching - contact aggregation & labelling ")
	agg_contact_df                   = contact.contact_list(msg_parsed)
	agg_contact_df['contact_gender'] = gender.gender_labeler(agg_contact_df['contact_name'],agg_contact_df['contact'])

	global_var['status_feature']=8

	# Insight generation
	# -------------------------------------------#	
	# -------------------------------------------#	

	## initialize
	# -------------------------------------------#	
	
	# basic 
	email_link_df = pd.merge(global_fun.dict_key_df(conver_parsed, "msg_threadid","msg_id"), global_fun.dict_key_df(msg_parsed, "msg_id","link_id"), 
		on='msg_id', how='right')
	email_link_df = email_link_df.reset_index(drop=True, inplace=False)

	# initialize insight df
	insight_df    = email_link_df

	## NON LANGUAGE INSIGHTS
	# -------------------------------------------#	
	print("Launching Insights - nonlang ")
	## volume [not merged in]
	volume_df = nonlang.volume(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'], msg_parsed,link_parsed, conver_parsed)

	global_var['status_feature']=9
	print("Successfully completed - volume [nonlang]")

	# firstlast
	firstlast_df = nonlang.firstlast(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed)
	insight_df   = pd.merge(insight_df, firstlast_df, on='link_id', how='outer')


	global_var['status_feature']=10
	print("Successfully completed - firstlast [nonlang]")

	# responsiveness
	responsiveness_df = nonlang.responsiveness(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed)
	insight_df        = pd.merge(responsiveness_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=11
	print("Successfully completed - responsiveness [nonlang]")

	## SIMPLE LANGUAGE INSIGHTS
	# -------------------------------------------#	
	print("Launching Insights - simplelang ")

	birthday_df        = simplelang.birthday(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed,msg_text_parsed,email_df_date["birthday"])
	insight_df         = pd.merge(birthday_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=12
	print("Successfully completed - birthday [simplelang]")

	# talkative
	talkative_df = simplelang.talkative(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed,msg_text_parsed)
	insight_df   = pd.merge(talkative_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=13
	print("Successfully completed - talkative [simplelang]")

	# lengthimbalance
	lengthimbalance_df = simplelang.lengthimbalance(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed,msg_text_parsed)
	insight_df         = pd.merge(lengthimbalance_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=14
	print("Successfully completed - lengthimbalance [simplelang]")


	## NLP INSIGHTS
	# -------------------------------------------#	
	print("Launching Insights - nlp ")

	## politeness
	politeness_df  = nlp_politeness.politeness(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'],msg_parsed,link_parsed,conver_parsed,msg_text_parsed)
	insight_df     = pd.merge(politeness_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=15
	print("Successfully completed - politeness [nlp]")

	## sentiment
	sentiment_df   = nlp_sentiment.sentiment(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'], msg_parsed,link_parsed,conver_parsed,msg_text_parsed)
	insight_df     = pd.merge(sentiment_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=16
	print("Successfully completed - sentiment [nlp]")

	## coordination
	coordination_df = nlp_coordination.coordination(email_link_df['link_id'], email_link_df['msg_id'], email_link_df['msg_threadid'], msg_parsed,link_parsed,conver_parsed,msg_text_parsed, contact_parsed)
	insight_df      = pd.merge(coordination_df, insight_df, on='link_id', how='outer')

	global_var['status_feature']=17
	print("Successfully completed - coordination [nlp]")

	# Append non-insight data 
	# -------------------------------------------#
	# -------------------------------------------#	
	
	# extract data
	conver_data     = global_fun.dict_key_df(conver_parsed, id_name_1="msg_threadid", incl_data=True)
	msg_data        = global_fun.dict_key_df(msg_parsed, id_name_1="msg_id", incl_data=True)
	msg_text_data   = global_fun.dict_key_df(msg_text_parsed, id_name_1="msg_id", incl_data=True)
	link_data       = global_fun.dict_key_df(link_parsed, id_name_1="link_id", incl_data=True)

	# merge
	insight_df      = pd.merge(insight_df, conver_data, on='msg_threadid', how='left')
	insight_df      = pd.merge(insight_df, msg_data, on='msg_id', how='left')
	insight_df      = pd.merge(insight_df, msg_text_data, on='msg_id', how='left')
	insight_df      = pd.merge(insight_df, link_data, on='link_id', how='left')
	
	# Format 
	# -------------------------------------------#
	# -------------------------------------------#	

	### omit rows with missing ids
	print("OMIT (MISSING ID): " + str(len(insight_df.loc[pd.isnull(insight_df['msg_id'])])))
	insight_df = insight_df.loc[pd.notnull(insight_df['msg_id'])]

	## omit unnecessary columns
	omit_col=[]
	insight_df.drop(omit_col, axis=1, inplace=True)

	## rename columns
	insight_df.rename(columns={'label':'label.gmail', 'message_sentence':'misc*msg_sentence','inbox_outbox':'flag.inbox_outbox'}, inplace=True)

	## set column order

	### column grouping & dictionary
	insight_df_dict = {}

	insight_df_dict['id_col']                  = ['msg_id','link_id','msg_threadid']
	insight_df_dict['contact_col']             = ['msg_to_name','msg_from_name','msg_cc_name','msg_bcc_name','msg_to_address','msg_from_address','msg_cc_address','msg_bcc_address','msg_contact']
	insight_df_dict['date_col']                = ['msg_date','msg_date_day','msg_date_weekday','msg_date_week','msg_date_month','msg_date_hour','msg_date_date','msg_date_daypart']
	insight_df_dict['link_col']                = [x for x in insight_df.columns if 'link_' in x and x not in insight_df_dict['id_col'] ]
	insight_df_dict['insight_col']             = [x for x in insight_df.columns if '..' in x]
	insight_df_dict['insight_interm_col']      = [x for x in insight_df.columns if '.__' in x]
	insight_df_dict['flag_col']                = [x for x in insight_df.columns if 'flag.' in x]
	insight_df_dict['label_col']               = [x for x in insight_df.columns if 'label.' in x]
	insight_df_dict['text_extra_col']          = [x for x in insight_df.columns if '*' in x]

	insight_df_dict['text_col']                = ['text']
	insight_df_dict['text_rel_col']            = ['subject']

	key_col                                    = np.concatenate([insight_df_dict['id_col'],insight_df_dict['link_col'], insight_df_dict['date_col'], insight_df_dict['insight_col'],insight_df_dict['label_col'], insight_df_dict['insight_interm_col'],insight_df_dict['text_extra_col'],insight_df_dict['flag_col'], insight_df_dict['text_col'], insight_df_dict['contact_col'], insight_df_dict['text_rel_col']])
	insight_df_dict['other_col']               = [x for x in insight_df.columns if x not in key_col]

	### order
	insight_df = insight_df[np.concatenate([insight_df_dict['id_col'], insight_df_dict['date_col'],insight_df_dict['contact_col'],
		insight_df_dict['text_col'],insight_df_dict['text_extra_col'], insight_df_dict['text_rel_col'], insight_df_dict['flag_col'],insight_df_dict['label_col'],insight_df_dict['link_col'],insight_df_dict['insight_col'],insight_df_dict['insight_interm_col']])]

	## append excluded emails
	insight_df['excluded']        = 0
	
	### format the excluded table (to enusre alignment)
	insight_df.reset_index(drop=True, inplace=True)

	## Run time
	end_time = datetime.datetime.now()
	run_time = end_time - start_time
	run_time = run_time.seconds

	# Return
	# -------------------------------------------#
	print("Successfully Completed - insight_generation")
	return (insight_df, insight_df_dict, agg_contact_df, volume_df, run_time)

#----------------------------------------------------------------------------#
#			                         End                                     #
#----------------------------------------------------------------------------#