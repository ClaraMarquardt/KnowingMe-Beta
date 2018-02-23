# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         insight_sample_mod
# Purpose:      Module - Define sample insight functions
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

# date_dist
#---------------------------------------------#
def date_dist(email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	date_dist_dict     = dict()
	
	# obtain data
	date_dict           = email_date_df['overview']

	# generate graph data
	date_dist_dict['graph_date']          				= sorted(date_dict.keys())
	date_dist_dict['graph_month']         				= [int(parser.parse(x).strftime("%m")) for x in date_dist_dict['graph_date']]
	date_dist_dict['graph_email_count']   				= [len(date_dict[x]) for x in date_dist_dict['graph_date']]

	date_dist_dict['graph_date_subset']                 = email_range
	date_dist_dict['graph_date_subset']                 = [parser.parse(x).strftime("%m-%d-%Y") for x in date_dist_dict['graph_date_subset'] ]
	date_dist_dict['graph_date_subset']                 = date_dist_dict['graph_date_subset'][::-1]
	date_dist_dict['graph_email_count_subset']          = [len(email_link_df.ix[email_link_df['msg_date_date']==x]) for x in date_dist_dict['graph_date_subset']]
	date_dist_dict['graph_email_count_sent_subset']     = [len(email_link_df.ix[email_link_df['msg_date_date']==x][email_link_df['inbox_outbox']=='outbox']) for x in date_dist_dict['graph_date_subset']]
	date_dist_dict['graph_email_count_received_subset'] = [len(email_link_df.ix[email_link_df['msg_date_date']==x][email_link_df['inbox_outbox']=='inbox']) for x in date_dist_dict['graph_date_subset']]

	# generate stats data
	date_dist_dict['stat_total_email']         			= sum(date_dist_dict['graph_email_count'])
	date_dist_dict['stat_email_per_day']       			= float(date_dist_dict['stat_total_email'])/len(date_dist_dict['graph_date'])
	
	date_dist_dict['stat_most_email_day']      			= date_dist_dict['graph_date'][np.argmax(date_dist_dict['graph_email_count'])]
	date_dist_dict['stat_most_email_email']    			= date_dist_dict['graph_email_count'][np.argmax(date_dist_dict['graph_email_count'])]

	return(date_dist_dict)

# time_dist
#---------------------------------------------#
def time_dist(email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	time_dist_dict = dict()
	
	# generate graph data
	for type_email, type_name in zip(["inbox|outbox","inbox","outbox"], ["","_sent","received"]):
	
		time_dist_dict['graph_weekday_hour_raw'+type_name]		= email_link_df.ix[email_link_df['inbox_outbox'].str.contains(type_email)]['msg_date_weekday_hour']
		time_dist_dict['graph_weekday_hour_raw'+type_name]  	= global_fun_mod.freq_tabulate(time_dist_dict['graph_weekday_hour_raw'+type_name],["email_count","weekday_hour"])

		time_dist_dict['graph_weekday'+type_name]				= [re.sub("(.*-)(.*)", "\\2", x.split(" - ")[0]) for x in time_dist_dict['graph_weekday_hour_raw'+type_name] ['weekday_hour']]
		time_dist_dict['graph_weekday'+type_name]           	= [int(parser.parse(x).strftime("%w")) for x in time_dist_dict['graph_weekday'+type_name]]
		time_dist_dict['graph_hour'+type_name]			    	= [int(re.sub("(Hour[ ]*)(.*)", "\\2", x.split(" - ")[1])) for x in time_dist_dict['graph_weekday_hour_raw'+type_name] ['weekday_hour']]
		time_dist_dict['graph_email_count'+type_name]	    	= time_dist_dict['graph_weekday_hour_raw'+type_name] ['email_count']

	# generate stats data
	for type_email, type_name in zip(["inbox|outbox","inbox","outbox"], ["","_sent","received"]):

		time_dist_dict['stat_total_email' + type_name]                 = len(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)])
		time_dist_dict['stat_email_per_day' + type_name]               = float(len(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)]))/email_diff
		
		time_dist_dict['stat_most_email_weekday' + type_name]          = re.sub("(.*-)(.* .*)", "\\2", np.argmax(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count()))
		time_dist_dict['stat_most_email_daypart' + type_name]          = re.sub("(.*-)(.* .*)", "\\2", np.argmax(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count()))
		time_dist_dict['stat_least_email_weekday' + type_name]         = re.sub("(.*-)(.* .*)", "\\2", np.argmin(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count()))
		time_dist_dict['stat_least_email_daypart' + type_name]         = re.sub("(.*-)(.* .*)", "\\2", np.argmin(email_link_df[email_link_df['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count()))

	return(time_dist_dict)

# network
#---------------------------------------------#
def network(email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	network_dict = dict()
	
	# generate graph data

	## raw data
	user_name_col        					  = np.concatenate([[user_name], np.array(contact_df['contact_name'])])
	user_email_col       					  = np.concatenate([[user_email], np.array(contact_df['contact'])])
	user_gender_col     					  = np.concatenate([[""], np.array(contact_df['contact_gender'])])
	email_count          				      = np.concatenate([[0], np.array(contact_df['freq_agg'])])
	email_count_sent     					  = np.concatenate([[0], np.array(contact_df['freq_outbox'])])
	email_count_received 					  = np.concatenate([[0], np.array(contact_df['freq_inbox'])])

	## network data
	network_dict['graph_network_matrix']      = np.zeros(shape=(len(user_name_col),len(user_name_col)))
	network_dict['graph_network_matrix'][1]   = email_count_sent
	network_dict['graph_network_matrix'][:,1] = email_count_received

	network_dict['graph_contact_name']        = user_name_col
	network_dict['graph_contact_email']       = user_email_col
	network_dict['graph_contact_gender']      = user_gender_col

	# generate stats data
	network_dict['stat_total_contact']        = len(user_name_col)
	network_dict['stat_perc_female']          = (float(len([x for x in network_dict['graph_contact_gender'] if x=='F']))/len([x for x in network_dict['graph_contact_gender'] if x=='M']))*100
	network_dict['stat_most_contact']         = network_dict['graph_contact_name'][np.argmax(email_count)]

	return(network_dict)

# sample_sentiment
#---------------------------------------------#
def sample_sentiment(email_link_df, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):
	
	# initialize
	sentiment_dict = dict()

	# prepare data
	email_link_df_sentiment    = email_link_df.sort_values('politeness..politeness', ascending=0)
	email_link_df_sentiment    = email_link_df_sentiment[np.isfinite(email_link_df['politeness..politeness'])]

	if (len(email_link_df_sentiment)>0):
		
		email_link_df_sentiment = email_link_df_sentiment.reset_index(drop=True, inplace=False)
		random_index            = random.randrange(0,len(email_link_df_sentiment))

		# generate graph data
		sentiment_dict['graph_sample_sentiment_email_text']  = email_link_df_sentiment.ix[random_index]['text']
		sentiment_dict['graph_sample_sentiment_email_stat']  = email_link_df_sentiment.ix[random_index]['politeness..politeness']

	else:

		email_link_df    = email_link_df.reset_index(drop=True, inplace=False)
		random_index     = random.randrange(0,len(email_link_df))

		sentiment_dict['graph_sample_sentiment_email_text']  = email_link_df.ix[random_index]['text']
		sentiment_dict['graph_sample_sentiment_email_stat']  = np.nan

	return(sentiment_dict)


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
