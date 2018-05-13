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
def date_dist(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):
	
	# initialize
	date_dist_dict     = dict()
	
	# obtain data
	date_dict           = email_date_df['overview']
	
	# generate graph data
	date_dist_dict['graph_date']          					= [x.strftime("%m/%d/%Y") for x in sorted([parser.parse(x) for x in date_dict.keys() ])][::-1]
	date_dist_dict['graph_month']         					= [int(parser.parse(x).strftime("%m")) for x in date_dist_dict['graph_date']]
	date_dist_dict['graph_email_count']   					= [len(date_dict[x]) for x in date_dist_dict['graph_date']]

	date_dist_dict['graph_date_subset']                 	= email_range
	date_dist_dict['graph_date_subset']                 	= [parser.parse(x).strftime("%m-%d-%Y") for x in date_dist_dict['graph_date_subset']]
	date_dist_dict['graph_date_subset']                 	= date_dist_dict['graph_date_subset'][::-1]
	date_dist_dict['graph_email_count_subset']          	= [len(set(np.array(email_link_df_unique.ix[email_link_df_unique['msg_date_date']==x]['msg_id']))) for x in date_dist_dict['graph_date_subset']]
	date_dist_dict['graph_email_count_sent_subset']     	= [len(set(np.array(email_link_df_unique.ix[email_link_df_unique['msg_date_date']==x][email_link_df_unique['inbox_outbox']=='outbox']['msg_id']))) for x in date_dist_dict['graph_date_subset']]
	date_dist_dict['graph_email_count_received_subset'] 	= [len(set(np.array(email_link_df_unique.ix[email_link_df_unique['msg_date_date']==x][email_link_df_unique['inbox_outbox']=='inbox']['msg_id']))) for x in date_dist_dict['graph_date_subset']]
	
	for type_email, type_name in zip(["inbox|outbox","outbox","inbox"], ["","_sent","_received"]):

		graph_email_sample_subset_raw   					    = [np.array(email_link_df_unique.ix[email_link_df_unique['inbox_outbox'].str.contains(type_email)][email_link_df_unique['msg_date_date']==x]['msg_id']) for x in date_dist_dict['graph_date_subset']]
		[np.random.shuffle(x) for x in graph_email_sample_subset_raw ]
		
		graph_email_sample_subset             = []
		for i in graph_email_sample_subset_raw:
			if len(i)>0:
				graph_email_sample_subset.append(i[0])
			else:
				graph_email_sample_subset.append('')
		
		date_dist_dict['graph_email_sample'+type_name+'_subset']             = []
		for i in graph_email_sample_subset:
			if len(i)>0:
				email_temp = (np.array(email_link_df_unique.ix[email_link_df_unique['msg_id']==i]['text'])[0][0:np.min([len(np.array(email_link_df_unique.ix[email_link_df_unique['msg_id']==i]['text'])[0]), 200])] + ("..."))
				email_temp = ''.join(x for x in email_temp if x in string.printable)
				date_dist_dict['graph_email_sample'+type_name+'_subset'].append(email_temp)
			else:
				date_dist_dict['graph_email_sample'+type_name+'_subset'].append(i)
		
	
		date_dist_dict['graph_email_sample_contact'+ type_name+'_subset']    = []
		
		for i in graph_email_sample_subset:
			if (len(i)>0):
				if np.array(email_link_df_unique.ix[email_link_df_unique['msg_id']==i]['inbox_outbox'])[0] == "inbox":
					date_dist_dict['graph_email_sample_contact'+type_name+'_subset'].append(("From: " + np.array(email_link_df_unique.ix[email_link_df_unique['msg_id']==i]['link_contact'])[0]))
				else:
					date_dist_dict['graph_email_sample_contact'+type_name+'_subset'].append(("To: " + np.array(email_link_df_unique.ix[email_link_df_unique['msg_id']==i]['link_contact'])[0]))
			else:
				date_dist_dict['graph_email_sample_contact'+type_name+'_subset'].append('')
		
	

	# generate stats data
	date_dist_dict['stat_total_email']         				= sum(date_dist_dict['graph_email_count'])
	date_dist_dict['stat_email_per_day']       				= float(date_dist_dict['stat_total_email'])/len(date_dist_dict['graph_date'])
	date_dist_dict['stat_perc_eng']       				    = float(np.nanmean(email_link_df_unique['language..english'])) * 100

	date_dist_dict['stat_subset_total_email']           	= sum(date_dist_dict['graph_email_count_subset'])
	date_dist_dict['stat_subset_sent_total_email']      	= sum(date_dist_dict['graph_email_count_sent_subset'])
	date_dist_dict['stat_subset_received_total_email']  	= sum(date_dist_dict['graph_email_count_received_subset'])

	return(date_dist_dict)

# time_dist
#---------------------------------------------#
def time_dist(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	time_dist_dict       = dict()
	
	# generate graph data
	for type_email, type_name in zip(["inbox|outbox","outbox","inbox"], ["","_sent","_received"]):
	
		graph_weekday_hour_raw									      = email_link_df_unique.ix[email_link_df_unique['inbox_outbox'].str.contains(type_email)]['msg_date_weekday_hour']
		graph_weekday_hour_raw  								      = global_fun_mod.freq_tabulate(graph_weekday_hour_raw,["email_count","weekday_hour"])

		time_dist_dict['graph_weekday'+type_name]				      = list(np.array([re.sub("(.*-)(.*)", "\\2", x.split(" - ")[0]) for x in graph_weekday_hour_raw['weekday_hour']]))
		time_dist_dict['graph_weekday'+type_name]           	      = list(np.array([int(parser.parse(x).strftime("%w")) for x in time_dist_dict['graph_weekday'+type_name]]))
		time_dist_dict['graph_hour'+type_name]			    		  = list(np.array([int(re.sub("(Hour[ ]*)(.*)", "\\2", x.split(" - ")[1])) for x in graph_weekday_hour_raw['weekday_hour']]))
		time_dist_dict['graph_email_count'+type_name]	    		  = list(np.array(graph_weekday_hour_raw['email_count']))

		# format weekday = 0 == mon
		time_dist_dict['graph_weekday'+type_name]                     = np.array([x-1 for x in time_dist_dict['graph_weekday'+type_name]])
		time_dist_dict['graph_weekday'+type_name][time_dist_dict['graph_weekday'+type_name]==-1] = 6
		time_dist_dict['graph_weekday'+type_name]                     = list(time_dist_dict['graph_weekday'+type_name])

	# generate stats data
	for type_email, type_name in zip(["inbox|outbox","outbox","inbox"], ["","_sent","_received"]):
		
		time_dist_dict['stat_most_email_weekday' + type_name]          = np.where(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count()==email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count().max())
		time_dist_dict['stat_most_email_weekday' + type_name]          = ', '.join([re.sub("(.*-)(.*)", "\\2", x) for x in np.array(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count().index[time_dist_dict['stat_most_email_weekday' + type_name]])])

		time_dist_dict['stat_least_email_weekday' + type_name]         = np.where(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count()==email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count().min())
		time_dist_dict['stat_least_email_weekday' + type_name]         = ', '.join([re.sub("(.*-)(.*)", "\\2", x) for x in np.array(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_weekday")['msg_date_weekday'].count().index[time_dist_dict['stat_least_email_weekday' + type_name]])])

		time_dist_dict['stat_most_email_daypart' + type_name]          = np.where(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count()==email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count().max())
		time_dist_dict['stat_most_email_daypart' + type_name]          = ', '.join([re.sub("(.*-)(.*)( .*)", "\\2", x) for x in np.array(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count().index[time_dist_dict['stat_most_email_daypart' + type_name]])])

		time_dist_dict['stat_least_email_daypart' + type_name]         = np.where(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count()==email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count().min())
		time_dist_dict['stat_least_email_daypart' + type_name]         = ', '.join([re.sub("(.*-)(.*)( .*)", "\\2", x) for x in np.array(email_link_df_unique[email_link_df_unique['inbox_outbox'].str.contains(type_email)].groupby("msg_date_daypart")['msg_date_daypart'].count().index[time_dist_dict['stat_least_email_daypart' + type_name]])])

	return(time_dist_dict)


# network
#---------------------------------------------#
def network(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):

	# initialize
	network_dict = dict()
	
	# generate graph data

	## subset
	contact_df_temp 								   = contact_df.sort_values(by=['freq_agg'], ascending=[False])
	contact_df_temp                                    = contact_df_temp[0:np.min([len(contact_df_temp), 30])]
	
	## raw data
	user_name_col        					           = np.concatenate([[user_name], np.array(contact_df_temp['contact_name'])])
	user_email_col       					           = np.concatenate([[user_email], np.array(contact_df_temp['contact'])])
	user_gender_col     					           = np.concatenate([[""], np.array(contact_df_temp['contact_gender'])])
	email_count          				               = np.concatenate([[0], np.array(contact_df_temp['freq_agg'])])
	email_count_sent     					           = np.concatenate([[0], np.array(contact_df_temp['freq_outbox'])])
	email_count_received 					  		   = np.concatenate([[0], np.array(contact_df_temp['freq_inbox'])])

	email_filter_male                                  = np.array([x!='M' for x in user_gender_col])
	email_count_male    				               = np.array(email_count)
	email_count_male[email_filter_male]                = 0
	email_count_sent_male    				           = np.array(email_count_sent)
	email_count_sent_male[email_filter_male]           = 0
	email_count_received_male    				       = np.array(email_count_received)
	email_count_received_male[email_filter_male]       = 0

	email_filter_female                                = np.array([x!='F' for x in user_gender_col])
	email_count_female    				               = np.array(email_count)
	email_count_female[email_filter_female]            = 0
	email_count_sent_female    				           = np.array(email_count_sent)
	email_count_sent_female[email_filter_female]       = 0
	email_count_received_female    				       = np.array(email_count_received)
	email_count_received_female[email_filter_female]   = 0

	## network data
	network_dict['graph_contact_name']                 = list(user_name_col)
	network_dict['graph_contact_email']                = list(user_email_col)
	network_dict['graph_contact_gender']               = list(user_gender_col)

	network_dict['graph_network_matrix_sent']      	   = list(email_count_sent)
	network_dict['graph_network_matrix_received']      = list(email_count_received)

	network_dict['graph_network_matrix']               = np.zeros(shape=(len(user_name_col),len(user_name_col)))
	network_dict['graph_network_matrix'][0]            = email_count_sent
	network_dict['graph_network_matrix'][:,0]          = email_count_received
	network_dict['graph_network_matrix']      	       = list(network_dict['graph_network_matrix'].flatten())

	network_dict['graph_network_matrix_male']          = np.zeros(shape=(len(user_name_col),len(user_name_col)))
	network_dict['graph_network_matrix_male'][0]       = email_count_sent_male
	network_dict['graph_network_matrix_male'][:,0]     = email_count_received_male
	network_dict['graph_network_matrix_male']          = list(network_dict['graph_network_matrix_male'].flatten())

	network_dict['graph_network_matrix_female']        = np.zeros(shape=(len(user_name_col),len(user_name_col)))
	network_dict['graph_network_matrix_female'][0]     = email_count_sent_female
	network_dict['graph_network_matrix_female'][:,0]   = email_count_received_female
	network_dict['graph_network_matrix_female']        = list(network_dict['graph_network_matrix_female'].flatten())

	# generate stats data
	network_dict['stat_total_contact_perc']            = (float(sum(contact_df_temp['freq_agg']))/sum(contact_df['freq_agg']))*100

	network_dict['stat_total_contact']                 = len(user_name_col)
	network_dict['stat_perc_female']                   = (float(len([x for x in network_dict['graph_contact_gender'] if x=='F']))/len([x for x in network_dict['graph_contact_gender'] if bool(re.search("M|F", x))==True]))*100
	network_dict['stat_perc_na']                       = (float(len([x for x in network_dict['graph_contact_gender'] if x=='I']))/len([x for x in network_dict['graph_contact_gender'] if bool(re.search("M|F|I", x))==True]))*100

	network_dict['stat_most_contact']                  = network_dict['graph_contact_name'][np.argmax(email_count)]
	network_dict['stat_most_contact_sent']             = network_dict['graph_contact_name'][np.argmax(email_count_sent)]
	network_dict['stat_most_contact_received']         = network_dict['graph_contact_name'][np.argmax(email_count_received)]

	network_dict['stat_most_contact_male']             = network_dict['graph_contact_name'][np.argmax(email_count_male)]
	network_dict['stat_most_contact_sent_male']        = network_dict['graph_contact_name'][np.argmax(email_count_sent_male)]
	network_dict['stat_most_contact_received_male']    = network_dict['graph_contact_name'][np.argmax(email_count_received_male)]

	network_dict['stat_most_contact_female']           = network_dict['graph_contact_name'][np.argmax(email_count_female)]
	network_dict['stat_most_contact_sent_female']      = network_dict['graph_contact_name'][np.argmax(email_count_sent_female)]
	network_dict['stat_most_contact_received_female']  = network_dict['graph_contact_name'][np.argmax(email_count_received_female)]

	return(network_dict)

# sample_sentiment
#---------------------------------------------#
def sample_sentiment(email_link_df, email_link_df_unique, current_date, email_date_df, email_diff, contact_df, user_name, user_email, email_range):
	
	# initialize
	sample_sentiment_dict = dict()

	# subset to sent
	email_link_df_unique_temp                 = email_link_df_unique.loc[email_link_df_unique['inbox_outbox']=='outbox']

	# generate graph data
	sample_sentiment_dict['graph_sentiment']  = list([x for x in np.array(email_link_df_unique_temp['sentiment..sentiment']) if ~np.isnan(x)])

	# generate samples
	sample_sentiment_dict['graph_sentiment_sample']          = []
	sample_sentiment_dict['graph_sentiment_sample_dist']     = []

	min_range = pd.cut((0,1),10, retbins=True)[1][0:10]
	max_range = pd.cut((0,1),10, retbins=True)[1][1:11]

	for min_sentiment,max_sentiment in zip(min_range, max_range):

		sample_temp = np.array(email_link_df_unique_temp[(email_link_df_unique_temp['sentiment..sentiment']>=min_sentiment) & (email_link_df_unique_temp['sentiment..sentiment'] < max_sentiment)]['msg_id'])

		if len(sample_temp)>0:
			np.random.shuffle(sample_temp)
			sample_temp = sample_temp[0]

			sample_msg  = np.array(email_link_df_unique_temp[(email_link_df_unique_temp['msg_id']==sample_temp)]['text'])[0]
			sample_msg  = ''.join(x for x in sample_msg if x in string.printable) 
			
			sample_dist = np.array(email_link_df_unique_temp[(email_link_df_unique_temp['msg_id']==sample_temp)]['sentiment_score_dist_vader'])[0]
			

			sample_sentiment_dict['graph_sentiment_sample'].append(sample_msg)
			sample_sentiment_dict['graph_sentiment_sample_dist'].append(sample_dist)
		
		else:
			
			sample_sentiment_dict['graph_sentiment_sample'] .append('')
			sample_sentiment_dict['graph_sentiment_sample_dist'].append('')


	return(sample_sentiment_dict)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
