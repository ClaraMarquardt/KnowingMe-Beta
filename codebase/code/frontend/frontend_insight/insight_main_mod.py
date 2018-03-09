# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_sample_mod
# Purpose:      Module - Define main insight functions
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
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# talkative
#---------------------------------------------#
def talkative(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	talkative_dict     = dict()
	
	# generate graph data    				
	for email_type, email_type_name in zip(["inbox|outbox","inbox","outbox"], ["","_received","_sent"]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):
			for word_type, word_type_name in zip(["character","word","sentence"], ["_character_","_word_","_sentence_"]):

				talkative_dict['stat_mean'+word_type_name+'count'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['talkative..'+word_type+'_count'])

	for email_type, email_type_name in zip(["inbox|outbox"], [""]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):
			for word_type, word_type_name in zip(["character","word","sentence"], ["_character_","_word_","_sentence_"]):

				talkative_dict['stat_mean'+word_type_name+'imbalance'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['lengthimbalance..length_imbalance_'+word_type])

	return(talkative_dict)


# responsiveness
#---------------------------------------------#
def responsiveness(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	responsiveness_dict     = dict()
	
	# generate graph data    				
	for email_type, email_type_name in zip(["inbox|outbox","inbox","outbox"], ["","_received","_sent"]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			responsiveness_dict['stat_mean_response_rate'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['responsiveness..reply']) * float(100)

	for email_type, email_type_name in zip(["inbox|outbox","inbox","outbox"], ["","_received","_sent"]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			responsiveness_dict['stat_mean_response_time'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['responsiveness..response_time'])

	return(responsiveness_dict)


# firstlast
#---------------------------------------------#
def firstlast(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	firstlast_dict     = dict()


	return(firstlast_dict)


# politeness
#---------------------------------------------#
def politeness(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	politeness_dict     = dict()
	
	# generate graph data    				
	for email_type, email_type_name in zip(["inbox|outbox","inbox","outbox"], ["","_received","_sent"]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			politeness_dict['stat_mean_politeness'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['politeness..politeness'])

	for email_type, email_type_name in zip(["inbox|outbox"], ["",]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			politeness_dict['stat_mean_politeness_imbalance'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['politeness..politeness_imbalance'])

	return(politeness_dict)

# sentiment
#---------------------------------------------#
def sentiment(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	sentiment_dict     = dict()
	
	# generate graph data
	for email_type, email_type_name in zip(["inbox|outbox","inbox","outbox"], ["","_received","_sent"]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			sentiment_dict['stat_mean_positivity'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['sentiment..sentiment'])

	for email_type, email_type_name in zip(["inbox|outbox"], [""]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):
			sentiment_dict['stat_mean_positivity_imbalance'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['sentiment..sentiment_imbalance'])

	return(sentiment_dict)

# coordination
#---------------------------------------------#
def coordination(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	coordination_dict     = dict()
	
	# generate graph data
	for email_type, email_type_name in zip(["inbox|outbox"], [""]):
		for contact_type, contact_type_name in zip(["F|M","M","F"], ["","_male","_female"]):

			coordination_dict['stat_mean_coordination'+email_type_name+contact_type_name]  = np.nanmean(email_link_df.ix[email_link_df['inbox_outbox'].str.contains(email_type) & email_link_df['contact_group'].str.contains(contact_type)]['coordination..score_agg'])


	return(coordination_dict)

	
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
