#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Main Frontend Interface Script
# Date:        August 2017
# Language:    Python (.py) [ Python 2.7 ]

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Dependencies - Internal
#---------------------------------------------#

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root,'code','frontend')))
from frontend_helper import * 

sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init__ import *
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Other Paths
pos_dict_path        = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'coordination', 'pos_dict.json'))

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

def insight_agg(insight_df, date_diff, insight_type, group_none_indic):

	print("Launching - insight_agg")

	"""
	Aggregate an insight DataFrame > Return insights

	Arguments:
	* insight_df         - insight DataFrame
	* date_diff          - length of time period over which emails have been extracted
	* insight_type       - category of insights which is to be generated

	Returns:
	* insight_agg_dict   - dictionary containing the generated insights
	* insight_plot       - list of insight plots
	* insight_plot_id    - ids associated with the list of insight plots
	
	"""

	# initialize
	# ------------------------------------
	insight_agg_dict = {}
	insight_plot     = []
	insight_plot_id  = []


	# date ranges
	# ------------------------------------
	date_range_dict = global_fun.date_range(insight_df)

	# other paramters
	# ------------------------------------
	with open(pos_dict_path) as f:
		pos_dict = json.load(f)

	pos_word_list         = pos_dict.keys()

	# collapse - aggregate
	# ------------------------------------
	insight_dict = aggregation.aggregate_insight(insight_df,insight_type,pos_word_list)

	#----------------------------------------------------------------------------#
	# non-language
	#----------------------------------------------------------------------------#
	if insight_type == "nonlang":

		# * volume
		#----------------------------------------------------------------------------#
		insight_volume_dict       = {}
		insight_volume_dict_agg   = {}
		insight_volume_dict_group = {}
		insight_volume_dict_time  = {}

		# aggregate
		# **********
		insight_volume_dict_agg['01-  Number of emails - sent/received']             =  len(insight_dict['agg_agg']['unique_msg'])
		insight_volume_dict_agg['02-  Number of emails - sent']                      =  len(insight_dict['agg_sent']['unique_msg'])
		insight_volume_dict_agg['03-  Number of emails - received']                  =  len(insight_dict['agg_received']['unique_msg'])
		insight_volume_dict_agg['04-  Average number of emails/day - sent/received'] =  insight_volume_dict_agg['01-  Number of emails - sent/received']  / float(date_diff)
		insight_volume_dict_agg['05-  Average number of emails/day - sent']          =  insight_volume_dict_agg['02-  Number of emails - sent']  /  float(date_diff)
		insight_volume_dict_agg['06-  Average number of emails/day - received']      =  insight_volume_dict_agg['03-  Number of emails - received']  /  float(date_diff)
		
		# by group
		# **********
		sent_received_a               = len(insight_dict['group_a_agg']['unique_msg'])
		sent_a                        = len(insight_dict['group_a_sent']['unique_msg'])
		received_a         			  = len(insight_dict['group_a_received']['unique_msg'])
		avg_sent_received_a           = sent_received_a / float(date_diff)
		avg_sent_a                    = sent_a / float(date_diff)
		avg_received_a                = received_a / float(date_diff)

		sent_received_b               = len(insight_dict['group_b_agg']['unique_msg'])
		sent_b                        = len(insight_dict['group_b_sent']['unique_msg'])
		received_b        			  = len(insight_dict['group_b_received']['unique_msg'])
		avg_sent_received_b           = sent_received_b / float(date_diff)
		avg_sent_b                    = sent_b / float(date_diff)
		avg_received_b                = received_b / float(date_diff)

		sent_received_none            = len(insight_dict['group_none_agg']['unique_msg'])
		sent_none                     = len(insight_dict['group_none_sent']['unique_msg'])
		received_none        		  = len(insight_dict['group_none_received']['unique_msg'])
		avg_sent_received_none        = sent_received_none / float(date_diff)
		avg_sent_none                 = sent_none / float(date_diff)
		avg_received_none             = received_none / float(date_diff)

		if (group_none_indic==1):

			insight_volume_dict_group['01-  Number of emails - sent/received']               = str(sent_received_a) + " / " + str(sent_received_b) + " / " + str(sent_received_none)
			insight_volume_dict_group['02-  Number of emails - sent']                        = str(sent_a) + " / " + str(sent_b) + " / " + str(sent_none)
			insight_volume_dict_group['03-  Number of emails - received']                    = str(received_a) + " / " + str(received_b) + " / " + str(received_none)
			insight_volume_dict_group['04-  Average number of emails/day - sent/received']   = str(avg_sent_received_a) + " / " + str(avg_sent_received_b) + " / " + str(avg_sent_received_none)
			insight_volume_dict_group['05-  Average number of emails/day - sent']            = str(avg_sent_a) + " / " + str(avg_sent_b) + " / " + str(avg_sent_none)
			insight_volume_dict_group['06-  Average number of emails/day - received']        = str(avg_received_a) + " / " + str(avg_received_b) + " / " + str(avg_received_none)
		
		else:

			insight_volume_dict_group['01-  Number of emails - sent/received']               = str(sent_received_a) + " / " + str(sent_received_b) 
			insight_volume_dict_group['02-  Number of emails - sent']                        = str(sent_a) + " / " + str(sent_b) 
			insight_volume_dict_group['03-  Number of emails - received']                    = str(received_a) + " / " + str(received_b) 
			insight_volume_dict_group['04-  Average number of emails/day - sent/received']   = str(avg_sent_received_a) + " / " + str(avg_sent_received_b) 
			insight_volume_dict_group['05-  Average number of emails/day - sent']            = str(avg_sent_a) + " / " + str(avg_sent_b) 
			insight_volume_dict_group['06-  Average number of emails/day - received']        = str(avg_received_a) + " / " + str(avg_received_b) 

		# by time
		# **********

		insight_volume_df_time_date                = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_agg']['unique_msg_date']['date_index'], "sent_received":insight_dict['agg_agg']['unique_msg_date']['id_index']}), "date", date_range_dict)
		insight_volume_df_time_week                = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_agg']['unique_msg_week']['date_index'], "sent_received":insight_dict['agg_agg']['unique_msg_week']['id_index']}), "week", date_range_dict)
		insight_volume_df_time_weekday             = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_agg']['unique_msg_weekday']['date_index'], "sent_received":insight_dict['agg_agg']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)
		insight_volume_df_time_dayperiod           = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_agg']['unique_msg_dayperiod']['date_index'], "sent_received":insight_dict['agg_agg']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)

		insight_volume_df_sent_time_date           = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date']['date_index'], "sent":insight_dict['agg_sent']['unique_msg_date']['id_index']}), "date", date_range_dict)
		insight_volume_df_sent_time_week           = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week']['date_index'], "sent":insight_dict['agg_sent']['unique_msg_week']['id_index']}), "week", date_range_dict)
		insight_volume_df_sent_time_weekday        = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday']['date_index'], "sent":insight_dict['agg_sent']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)
		insight_volume_df_sent_time_dayperiod      = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod']['date_index'], "sent":insight_dict['agg_sent']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)

		insight_volume_df_received_time_date       = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_date']['date_index'], "received":insight_dict['agg_received']['unique_msg_date']['id_index']}), "date", date_range_dict)
		insight_volume_df_received_time_week       = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_week']['date_index'], "received":insight_dict['agg_received']['unique_msg_week']['id_index']}), "week", date_range_dict)
		insight_volume_df_received_time_weekday    = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_weekday']['date_index'], "received":insight_dict['agg_received']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)
		insight_volume_df_received_time_dayperiod  = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_dayperiod']['date_index'], "received":insight_dict['agg_received']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)

		## generate graph traces

		# * sent / received
		sent_received_day = dict(
			x=insight_volume_df_time_date['msg_date'],
			y=insight_volume_df_time_date['sent_received'],
			name="Emails - Sent/Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		sent_received_week = dict(
			x=insight_volume_df_time_week['msg_date'],
			y=insight_volume_df_time_week['sent_received'],
			name="Emails - Sent/Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line = dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		sent_received_weekday = dict(
			x=insight_volume_df_time_weekday['msg_date'],
			y=insight_volume_df_time_weekday['sent_received'],
			name="Emails - Sent/Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		sent_received_dayperiod = dict(
			x=insight_volume_df_time_dayperiod['msg_date'],
			y=insight_volume_df_time_dayperiod['sent_received'],
			name="Emails - Sent/Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		# * sent
		sent_day = dict(
			x=insight_volume_df_sent_time_date['msg_date'],
			y=insight_volume_df_sent_time_date['sent'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		sent_week = dict(
			x=insight_volume_df_sent_time_week['msg_date'],
			y=insight_volume_df_sent_time_week['sent'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		sent_weekday = dict(
			x=insight_volume_df_sent_time_weekday['msg_date'],
			y=insight_volume_df_sent_time_weekday['sent'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		sent_dayperiod = dict(
			x=insight_volume_df_sent_time_dayperiod['msg_date'],
			y=insight_volume_df_sent_time_dayperiod['sent'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		# * received
		received_day = dict(
			x=insight_volume_df_received_time_date['msg_date'],
			y=insight_volume_df_received_time_date['received'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)
		)

		received_week = dict(
			x=insight_volume_df_received_time_week['msg_date'],
			y=insight_volume_df_received_time_week['received'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)
		)

		received_weekday = dict(
			x=insight_volume_df_received_time_weekday['msg_date'],
			y=insight_volume_df_received_time_weekday['received'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)
		)

		received_dayperiod = dict(
			x=insight_volume_df_received_time_dayperiod['msg_date'],
			y=insight_volume_df_received_time_dayperiod['received'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)


		## generate graph (s)
		volume_graph_day = dict(	
				data=[sent_received_day, sent_day, received_day]
		)
		insight_plot.append(volume_graph_day)

		volume_graph_week = dict(	
				data=[sent_received_week, sent_week, received_week]
		)
		insight_plot.append(volume_graph_week)

		volume_graph_weekday = dict(	
				data=[sent_received_weekday, sent_weekday, received_weekday]
		)
		insight_plot.append(volume_graph_weekday)

		volume_graph_dayperiod = dict(	
				data=[sent_received_dayperiod, sent_dayperiod, received_dayperiod]
		)
		insight_plot.append(volume_graph_dayperiod)

		# aggregate & store
		# **********
		insight_volume_dict['agg']   = global_fun.dict_round(insight_volume_dict_agg)
		insight_volume_dict['group'] = global_fun.dict_round(insight_volume_dict_group)
		insight_volume_dict['time']  = global_fun.dict_round(insight_volume_dict_time)
		insight_agg_dict['volume']   = insight_volume_dict
		
		# * firstlast
		#----------------------------------------------------------------------------#

		insight_firstlast_dict       = {}
		insight_firstlast_dict_agg   = {}
		insight_firstlast_dict_group = {}
		insight_firstlast_dict_time  = {}

		# aggregate
		# **********
		insight_firstlast_dict_agg['01-  Percent of conversations > Sent 1st email (%)']  =   global_fun.perc(len(insight_dict['agg_first']['unique_thread_start']), len(insight_dict['agg_conversation']['unique_thread_start']))
		insight_firstlast_dict_agg['02-  Percent of conversations > Sent last email (%)'] =   global_fun.perc(len(insight_dict['agg_last']['unique_thread_start']), len(insight_dict['agg_conversation']['unique_thread_start']))

		# by group
		# **********
		firstlast_first_a      =  global_fun.perc(len(insight_dict['group_a_first']['unique_thread_start']), len(insight_dict['group_a_conversation']['unique_thread_start']))
		firstlast_last_a       =  global_fun.perc(len(insight_dict['group_a_last']['unique_thread_start']), len(insight_dict['group_a_conversation']['unique_thread_start']))   
		
		firstlast_first_b      =  global_fun.perc(len(insight_dict['group_b_first']['unique_thread_start']), len(insight_dict['group_b_conversation']['unique_thread_start']))
		firstlast_last_b       =  global_fun.perc(len(insight_dict['group_b_last']['unique_thread_start']), len(insight_dict['group_b_conversation']['unique_thread_start']))

		firstlast_first_none   =  global_fun.perc(len(insight_dict['group_none_first']['unique_thread_start']), len(insight_dict['group_none_conversation']['unique_thread_start']))
		firstlast_last_none    =  global_fun.perc(len(insight_dict['group_none_last']['unique_thread_start']), len(insight_dict['group_none_conversation']['unique_thread_start']))
		
		if (group_none_indic==1):
			insight_firstlast_dict_group['01-  Percent of conversations > Sent 1st email (%)']  =  str(firstlast_first_a) + " / " + str(firstlast_first_b) + " / " + str(firstlast_first_none)
			insight_firstlast_dict_group['02-  Percent of conversations > Sent last email (%)'] =  str(firstlast_last_a) + " / " + str(firstlast_last_b) + " / " + str(firstlast_last_none)
		
		else: 
			insight_firstlast_dict_group['01-  Percent of conversations > Sent 1st email (%)']  =  str(firstlast_first_a) + " / " + str(firstlast_first_b) 
			insight_firstlast_dict_group['02-  Percent of conversations > Sent last email (%)'] =  str(firstlast_last_a) + " / " + str(firstlast_last_b) 

		# by time
		# **********

		## thread
		insight_firstlast_df_agg_thread_time_date     = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_conversation']['unique_thread_ongoing_date']['date_index'], "conversation":insight_dict['agg_conversation']['unique_thread_ongoing_date']['id_index']}), "date", date_range_dict)
		insight_firstlast_df_agg_thread_time_week     = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_conversation']['unique_thread_ongoing_week']['date_index'], "conversation":insight_dict['agg_conversation']['unique_thread_ongoing_week']['id_index']}), "week", date_range_dict)

		## message
		insight_firstlast_df_agg_msg_time_date        = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date']['date_index'], "message":insight_dict['agg_sent']['unique_msg_date']['id_index']}), "date",date_range_dict)
		insight_firstlast_df_agg_msg_time_week        = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week']['date_index'], "message":insight_dict['agg_sent']['unique_msg_week']['id_index']}), "week",date_range_dict)

		insight_firstlast_df_first_msg_time_date      = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_first']['unique_msg_date']['date_index'], "message_first":insight_dict['agg_first']['unique_msg_date']['id_index']}), "date",date_range_dict)
		insight_firstlast_df_first_msg_time_week      = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_first']['unique_msg_week']['date_index'], "message_first":insight_dict['agg_first']['unique_msg_week']['id_index']}), "week",date_range_dict)

		insight_firstlast_df_last_msg_time_date       = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_last']['unique_msg_date']['date_index'], "message_last":insight_dict['agg_last']['unique_msg_date']['id_index']}), "date",date_range_dict)
		insight_firstlast_df_last_msg_time_week       = global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_last']['unique_msg_week']['date_index'], "message_last":insight_dict['agg_last']['unique_msg_week']['id_index']}), "week",date_range_dict)


		# * msg level
		agg_msg_week = dict(
			x=insight_firstlast_df_agg_msg_time_week['msg_date'],
			y=insight_firstlast_df_agg_msg_time_week['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		first_msg_week = dict(
			x=insight_firstlast_df_first_msg_time_week['msg_date'],
			y=insight_firstlast_df_first_msg_time_week['message_first'],
			name="Emails - Sent + 1st Email (Conversations Started)",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		last_msg_week = dict(
			x=insight_firstlast_df_last_msg_time_week['msg_date'],
			y=insight_firstlast_df_last_msg_time_week['message_last'],
			name="Emails - Sent + Last Email (Conversations Ended)",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)
		)

		agg_msg_date = dict(
			x=insight_firstlast_df_agg_msg_time_date['msg_date'],
			y=insight_firstlast_df_agg_msg_time_date['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		first_msg_date = dict(
			x=insight_firstlast_df_first_msg_time_date['msg_date'],
			y=insight_firstlast_df_first_msg_time_date['message_first'],
			name="Emails - Sent + 1st Email (Conversations Started)",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		last_msg_date = dict(
			x=insight_firstlast_df_last_msg_time_date['msg_date'],
			y=insight_firstlast_df_last_msg_time_date['message_last'],
			name="Emails - Sent + Last Email (Conversations Ended)",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)
		)

		# * thread level
		agg_thread_week = dict(
			x=insight_firstlast_df_agg_thread_time_week['msg_date'],
			y=insight_firstlast_df_agg_thread_time_week['conversation'],
			name="Active Conversations",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dashdot', width= 1), 
			marker=dict(size=4)
		)

		agg_thread_date = dict(
			x=insight_firstlast_df_agg_thread_time_date['msg_date'],
			y=insight_firstlast_df_agg_thread_time_date['conversation'],
			name="Active Conversations",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dashdot', width= 1), 
			marker=dict(size=4)
		)


		## generate graph (s)
		firstlast_msg_graph_day = dict(	
				data=[agg_thread_date, agg_msg_date, first_msg_date, last_msg_date]
		)
		insight_plot.append(firstlast_msg_graph_day)

		firstlast_msg_graph_week = dict(	
				data=[agg_thread_week, agg_msg_week, first_msg_week, last_msg_week]
		)
		insight_plot.append(firstlast_msg_graph_week)


	
		## STORE
		insight_firstlast_dict['agg']   = global_fun.dict_round(insight_firstlast_dict_agg)
		insight_firstlast_dict['group'] = global_fun.dict_round(insight_firstlast_dict_group)
		insight_firstlast_dict['time']  = global_fun.dict_round(insight_firstlast_dict_time)
		insight_agg_dict['firstlast']   = insight_firstlast_dict

		
		# * responsiveness
		#----------------------------------------------------------------------------#

		insight_responsiveness_dict       = {}
		insight_responsiveness_dict_agg   = {}
		insight_responsiveness_dict_group = {}
		insight_responsiveness_dict_time  = {}


		# aggregate
		# **********
		insight_responsiveness_dict_agg['01-  Percent of messages sent > Received a response (%)']     = global_fun.perc(len(insight_dict['agg_sent_response']['unique_msg']),len(insight_dict['agg_sent']['unique_msg']))
		insight_responsiveness_dict_agg['02-  > Median response time (minutes)']               		   = np.nanmedian([float(x) for x in insight_dict['agg_sent_response']['unique_link']['responsiveness..response_time']])
		insight_responsiveness_dict_agg['03-  Percent of messages received > Sent a response (%)']     = global_fun.perc(len(insight_dict['agg_received_response']['unique_msg']),len(insight_dict['agg_received']['unique_msg']))
		insight_responsiveness_dict_agg['04-  > Median response time (minutes)']                       = np.nanmedian([float(x) for x in insight_dict['agg_received_response']['unique_link']['responsiveness..response_time']])

		# by group
		# **********
		responsiveness_sent_group_a               	 = global_fun.perc(len(insight_dict['group_a_sent_response']['unique_msg']),len(insight_dict['group_a_sent']['unique_msg']))
		responsiveness_sent_time_group_a          	 = np.nanmedian([float(x) for x in insight_dict['group_a_sent_response']['unique_link']['responsiveness..response_time']])
		
		responsiveness_received_group_a           	 = global_fun.perc(len(insight_dict['group_a_received_response']['unique_msg']),len(insight_dict['group_a_received']['unique_msg']))
		responsiveness_received_time_group_a      	 = np.nanmedian([float(x) for x in insight_dict['group_a_received_response']['unique_link']['responsiveness..response_time']])

		responsiveness_sent_group_b               	 = global_fun.perc(len(insight_dict['group_b_sent_response']['unique_msg']),len(insight_dict['group_b_sent']['unique_msg']))
		responsiveness_sent_time_group_b          	 = np.nanmedian([float(x) for x in insight_dict['group_b_sent_response']['unique_link']['responsiveness..response_time']])
		
		responsiveness_received_group_b           	 = global_fun.perc(len(insight_dict['group_b_received_response']['unique_msg']),len(insight_dict['group_b_received']['unique_msg']))
		responsiveness_received_time_group_b      	 = np.nanmedian([float(x) for x in insight_dict['group_b_received_response']['unique_link']['responsiveness..response_time']])

		responsiveness_sent_group_none               = global_fun.perc(len(insight_dict['group_none_sent_response']['unique_msg']),len(insight_dict['group_none_sent']['unique_msg']))
		responsiveness_sent_time_group_none          = np.nanmedian([float(x) for x in insight_dict['group_none_sent_response']['unique_link']['responsiveness..response_time']])
		
		responsiveness_received_group_none           = global_fun.perc(len(insight_dict['group_none_received_response']['unique_msg']),len(insight_dict['group_none_received']['unique_msg']))
		responsiveness_received_time_group_none      = np.nanmedian([float(x) for x in insight_dict['group_none_received_response']['unique_link']['responsiveness..response_time']])

		if (group_none_indic==1):

			insight_responsiveness_dict_group['01-  Percent of messages sent > Received a response (%)']     	=  str(responsiveness_sent_group_a) + " / " + str(responsiveness_sent_group_b) + " / " + str(responsiveness_sent_group_none)
			insight_responsiveness_dict_group['02-  > Median response time (minutes)']      					=  str(responsiveness_sent_time_group_a) + " / " + str(responsiveness_sent_time_group_b) + " / " + str(responsiveness_sent_time_group_none)
			insight_responsiveness_dict_group['03-  Percent of messages received > Sent a response (%)']     	=  str(responsiveness_received_group_a) + " / " + str(responsiveness_received_group_b) + " / " + str(responsiveness_received_group_none)
			insight_responsiveness_dict_group['04-  > Median response time (minutes)']      					=  str(responsiveness_received_time_group_a) + " / " + str(responsiveness_received_time_group_b) + " / " + str(responsiveness_received_time_group_none)

		else: 

			insight_responsiveness_dict_group['01-  Percent of messages sent > Received a response (%)']     	=  str(responsiveness_sent_group_a) + " / " + str(responsiveness_sent_group_b) 
			insight_responsiveness_dict_group['02-  > Median response time (minutes)']      					=  str(responsiveness_sent_time_group_a) + " / " + str(responsiveness_sent_time_group_b)
			insight_responsiveness_dict_group['03-  Percent of messages received > Sent a response (%)']     	=  str(responsiveness_received_group_a) + " / " + str(responsiveness_received_group_b) 
			insight_responsiveness_dict_group['04-  > Median response time (minutes)']      					=  str(responsiveness_received_time_group_a) + " / " + str(responsiveness_received_time_group_b) 

		# by time
		# **********

		## sent
		insight_responsiveness_df_sent_date              	   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date']['date_index'], "message":insight_dict['agg_sent']['unique_msg_date']['id_index']}), "date", date_range_dict)
		insight_responsiveness_df_sent_response_date    	   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent_response']['unique_msg_date']['date_index'], "message":insight_dict['agg_sent_response']['unique_msg_date']['id_index']}), "date", date_range_dict)

		insight_responsiveness_df_sent_week              	   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week']['date_index'], "message":insight_dict['agg_sent']['unique_msg_week']['id_index']}), "week", date_range_dict)
		insight_responsiveness_df_sent_response_week     	   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent_response']['unique_msg_week']['date_index'], "message":insight_dict['agg_sent_response']['unique_msg_week']['id_index']}), "week", date_range_dict)

		insight_responsiveness_df_sent_weekday                 =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday']['date_index'], "message":insight_dict['agg_sent']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)
		insight_responsiveness_df_sent_response_weekday        =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent_response']['unique_msg_weekday']['date_index'], "message":insight_dict['agg_sent_response']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)

		insight_responsiveness_df_sent_dayperiod               =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod']['date_index'], "message":insight_dict['agg_sent']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)
		insight_responsiveness_df_sent_response_dayperiod      =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent_response']['unique_msg_dayperiod']['date_index'], "message":insight_dict['agg_sent_response']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)

		## received
		insight_responsiveness_df_received_date                =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_date']['date_index'], "message":insight_dict['agg_received']['unique_msg_date']['id_index']}), "date", date_range_dict)
		insight_responsiveness_df_received_response_date       =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received_response']['unique_msg_date']['date_index'], "message":insight_dict['agg_received_response']['unique_msg_date']['id_index']}), "date", date_range_dict)

		insight_responsiveness_df_received_week                =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_week']['date_index'], "message":insight_dict['agg_received']['unique_msg_week']['id_index']}), "week", date_range_dict)
		insight_responsiveness_df_received_response_week       =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received_response']['unique_msg_week']['date_index'], "message":insight_dict['agg_received_response']['unique_msg_week']['id_index']}), "week", date_range_dict)

		insight_responsiveness_df_received_weekday             =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_weekday']['date_index'], "message":insight_dict['agg_received']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)
		insight_responsiveness_df_received_response_weekday    =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received_response']['unique_msg_weekday']['date_index'], "message":insight_dict['agg_received_response']['unique_msg_weekday']['id_index']}), "weekday", date_range_dict)

		insight_responsiveness_df_received_dayperiod           =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_dayperiod']['date_index'], "message":insight_dict['agg_received']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)
		insight_responsiveness_df_received_response_dayperiod  =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received_response']['unique_msg_dayperiod']['date_index'], "message":insight_dict['agg_received_response']['unique_msg_dayperiod']['id_index']}), "dayperiod", date_range_dict)


		# sent
		agg_sent_date = dict(
			x=insight_responsiveness_df_sent_date['msg_date'],
			y=insight_responsiveness_df_sent_date['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_sent_response_date = dict(
			x=insight_responsiveness_df_sent_response_date['msg_date'],
			y=insight_responsiveness_df_sent_response_date['message'],
			name="Emails > Sent + Received a Response",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)


		agg_sent_week = dict(
			x=insight_responsiveness_df_sent_week['msg_date'],
			y=insight_responsiveness_df_sent_week['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_sent_response_week = dict(
			x=insight_responsiveness_df_sent_response_week['msg_date'],
			y=insight_responsiveness_df_sent_response_week['message'],
			name="Emails > Sent + Received a Response",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)


		agg_sent_weekday = dict(
			x=insight_responsiveness_df_sent_weekday['msg_date'],
			y=insight_responsiveness_df_sent_weekday['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_sent_response_weekday = dict(
			x=insight_responsiveness_df_sent_response_weekday['msg_date'],
			y=insight_responsiveness_df_sent_response_weekday['message'],
			name="Emails > Sent + Received a Response",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		agg_sent_dayperiod = dict(
			x=insight_responsiveness_df_sent_dayperiod['msg_date'],
			y=insight_responsiveness_df_sent_dayperiod['message'],
			name="Emails - Sent",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_sent_response_dayperiod = dict(
			x=insight_responsiveness_df_sent_response_dayperiod['msg_date'],
			y=insight_responsiveness_df_sent_response_dayperiod['message'],
			name="Emails > Sent + Received a Response",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		## received
		agg_received_date = dict(
			x=insight_responsiveness_df_received_date['msg_date'],
			y=insight_responsiveness_df_received_date['message'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_received_response_date = dict(
			x=insight_responsiveness_df_received_response_date['msg_date'],
			y=insight_responsiveness_df_received_response_date['message'],
			name="Emails > Received + Sent a Reponse",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)


		agg_received_week = dict(
			x=insight_responsiveness_df_received_week['msg_date'],
			y=insight_responsiveness_df_received_week['message'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_received_response_week = dict(
			x=insight_responsiveness_df_received_response_week['msg_date'],
			y=insight_responsiveness_df_received_response_week['message'],
			name="Emails > Received + Sent a Reponse",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)


		agg_received_weekday = dict(
			x=insight_responsiveness_df_received_weekday['msg_date'],
			y=insight_responsiveness_df_received_weekday['message'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_received_response_weekday = dict(
			x=insight_responsiveness_df_received_response_weekday['msg_date'],
			y=insight_responsiveness_df_received_response_weekday['message'],
			name="Emails > Received + Sent a Reponse",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)

		agg_received_dayperiod = dict(
			x=insight_responsiveness_df_received_dayperiod['msg_date'],
			y=insight_responsiveness_df_received_dayperiod['message'],
			name="Emails - Received",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)
		)

		agg_received_response_dayperiod = dict(
			x=insight_responsiveness_df_received_response_dayperiod['msg_date'],
			y=insight_responsiveness_df_received_response_dayperiod['message'],
			name="Emails > Received + Sent a Reponse",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
		)


		## generate graph (s)

		## sent 
		responsiveness_sent_graph_day = dict(	
				data=[agg_sent_date,agg_sent_response_date,agg_received_date,agg_received_response_date]
		)
		insight_plot.append(responsiveness_sent_graph_day)

		responsiveness_sent_graph_week = dict(	
				data=[agg_sent_week,agg_sent_response_week,agg_received_week,agg_received_response_week]
		)
		insight_plot.append(responsiveness_sent_graph_week)


		responsiveness_sent_graph_weekday = dict(	
				data=[agg_sent_weekday,agg_sent_response_weekday,agg_received_weekday,agg_received_response_weekday]
		)
		insight_plot.append(responsiveness_sent_graph_weekday)


		responsiveness_sent_graph_dayperiod = dict(	
				data=[agg_sent_dayperiod,agg_sent_response_dayperiod,agg_received_dayperiod,agg_received_response_dayperiod]
		)
		insight_plot.append(responsiveness_sent_graph_dayperiod)


		## STORE
		insight_responsiveness_dict['agg']   = global_fun.dict_round(insight_responsiveness_dict_agg)
		insight_responsiveness_dict['group'] = global_fun.dict_round(insight_responsiveness_dict_group)
		insight_responsiveness_dict['time']  = global_fun.dict_round(insight_responsiveness_dict_time)
		insight_agg_dict['responsiveness']   = insight_responsiveness_dict




	#----------------------------------------------------------------------------#
	# simple-language
	#----------------------------------------------------------------------------#
	elif insight_type == "simplelang": 

		# * talkative
		#----------------------------------------------------------------------------#

		insight_talkative_dict       = {}
		insight_talkative_dict_agg   = {}
		insight_talkative_dict_group = {}
		insight_talkative_dict_time  = {}

		# aggregate
		# **********

		insight_talkative_dict_agg['01-  Median number of characters - sent emails']        =  np.nanmedian([float(x) for x in insight_dict['agg_sent']['unique_msg']['talkative..character_count']])
		insight_talkative_dict_agg['02-  Median number of words - sent emails']             =  np.nanmedian([float(x) for x in insight_dict['agg_sent']['unique_msg']['talkative..word_count']])
		insight_talkative_dict_agg['03-  Median number of sentences - sent emails']         =  np.nanmedian([float(x) for x in insight_dict['agg_sent']['unique_msg']['talkative..sentence_count']])

		insight_talkative_dict_agg['04-  Median number of characters - received emails']    =  np.nanmedian([float(x) for x in insight_dict['agg_received']['unique_msg']['talkative..character_count']])
		insight_talkative_dict_agg['05-  Median number of words - received emails']         =  np.nanmedian([float(x) for x in insight_dict['agg_received']['unique_msg']['talkative..word_count']])
		insight_talkative_dict_agg['06-  Median number of sentences - received emails']     =  np.nanmedian([float(x) for x in insight_dict['agg_received']['unique_msg']['talkative..sentence_count']])


		# by group
		# **********

		## sent
		character_count_sent_a        = np.nanmedian([float(x) for x in insight_dict['group_a_sent']['unique_msg']['talkative..character_count']])
		word_count_sent_a             = np.nanmedian([float(x) for x in insight_dict['group_a_sent']['unique_msg']['talkative..word_count']])
		sentence_count_sent_a         = np.nanmedian([float(x) for x in insight_dict['group_a_sent']['unique_msg']['talkative..sentence_count']])

		character_count_sent_b        = np.nanmedian([float(x) for x in insight_dict['group_b_sent']['unique_msg']['talkative..character_count']])
		word_count_sent_b             = np.nanmedian([float(x) for x in insight_dict['group_b_sent']['unique_msg']['talkative..word_count']])
		sentence_count_sent_b  	      = np.nanmedian([float(x) for x in insight_dict['group_b_sent']['unique_msg']['talkative..sentence_count']])

		character_count_sent_none     = np.nanmedian([float(x) for x in insight_dict['group_none_sent']['unique_msg']['talkative..character_count']])
		word_count_sent_none          = np.nanmedian([float(x) for x in insight_dict['group_none_sent']['unique_msg']['talkative..word_count']])
		sentence_count_sent_none  	  = np.nanmedian([float(x) for x in insight_dict['group_none_sent']['unique_msg']['talkative..sentence_count']])


		## received
		character_count_received_a    = np.nanmedian([float(x) for x in insight_dict['group_a_received']['unique_msg']['talkative..character_count']])
		word_count_received_a         = np.nanmedian([float(x) for x in insight_dict['group_a_received']['unique_msg']['talkative..word_count']])
		sentence_count_received_a     = np.nanmedian([float(x) for x in insight_dict['group_a_received']['unique_msg']['talkative..sentence_count']])

		character_count_received_b    = np.nanmedian([float(x) for x in insight_dict['group_b_received']['unique_msg']['talkative..character_count']])
		word_count_received_b         = np.nanmedian([float(x) for x in insight_dict['group_b_received']['unique_msg']['talkative..word_count']])
		sentence_count_received_b  	  = np.nanmedian([float(x) for x in insight_dict['group_b_received']['unique_msg']['talkative..sentence_count']])

		character_count_received_none = np.nanmedian([float(x) for x in insight_dict['group_none_received']['unique_msg']['talkative..character_count']])
		word_count_received_none      = np.nanmedian([float(x) for x in insight_dict['group_none_received']['unique_msg']['talkative..word_count']])
		sentence_count_received_none  = np.nanmedian([float(x) for x in insight_dict['group_none_received']['unique_msg']['talkative..sentence_count']])

		if (group_none_indic==1):

			insight_talkative_dict_group['01-  Median number of characters - sent emails']        =  str(character_count_sent_a) + " / " + str(character_count_sent_b) + " / " + str(character_count_sent_none)
			insight_talkative_dict_group['02-  Median number of words - sent emails']             =  str(word_count_sent_a) + " / " + str(word_count_sent_b) + " / " + str(word_count_sent_none)
			insight_talkative_dict_group['03-  Median number of sentences - sent emails']         =  str(sentence_count_sent_a) + " / " + str(sentence_count_sent_b)+ " / " + str(sentence_count_sent_none)

			insight_talkative_dict_group['04-  Median number of characters - received emails']    =  str(character_count_received_a) + " / " + str(character_count_received_b) + " / " + str(character_count_received_none)
			insight_talkative_dict_group['05-  Median number of words - received emails']         =  str(word_count_received_a) + " / " + str(word_count_received_b) + " / " + str(word_count_received_none)
			insight_talkative_dict_group['06-  Median number of sentences - received emails']     =  str(sentence_count_received_a) + " / " + str(sentence_count_received_b)+ " / " + str(sentence_count_received_none)

		else: 

			insight_talkative_dict_group['01-  Median number of characters - sent emails']        =  str(character_count_sent_a) + " / " + str(character_count_sent_b) 
			insight_talkative_dict_group['02-  Median number of words - sent emails']             =  str(word_count_sent_a) + " / " + str(word_count_sent_b) 
			insight_talkative_dict_group['03-  Median number of sentences - sent emails']         =  str(sentence_count_sent_a) + " / " + str(sentence_count_sent_b)

			insight_talkative_dict_group['04-  Median number of characters - received emails']    =  str(character_count_received_a) + " / " + str(character_count_received_b) 
			insight_talkative_dict_group['05-  Median number of words - received emails']         =  str(word_count_received_a) + " / " + str(word_count_received_b) 
			insight_talkative_dict_group['06-  Median number of sentences - received emails']     =  str(sentence_count_received_a) + " / " + str(sentence_count_received_b)
	

		# by time
		# **********

		# aggregate
		insight_talkative_df_sent_character_date        =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_date_length']['talkative..character_count']}), "date", date_range_dict)
		insight_talkative_df_sent_character_week        =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_week_length']['talkative..character_count']}), "week", date_range_dict)
		insight_talkative_df_sent_character_weekday     =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_weekday_length']['talkative..character_count']}), "weekday", date_range_dict)
		insight_talkative_df_sent_character_dayperiod   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_dayperiod_length']['talkative..character_count']}), "dayperiod", date_range_dict)

		insight_talkative_df_sent_word_date        		=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_date_length']['talkative..word_count']}), "date", date_range_dict)
		insight_talkative_df_sent_word_week        		=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_week_length']['talkative..word_count']}), "week", date_range_dict)
		insight_talkative_df_sent_word_weekday     		=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_weekday_length']['talkative..word_count']}), "weekday", date_range_dict)
		insight_talkative_df_sent_word_dayperiod   		=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_dayperiod_length']['talkative..word_count']}), "dayperiod", date_range_dict)

		insight_talkative_df_sent_sentence_date        	=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_date_length']['talkative..sentence_count']}), "date", date_range_dict)
		insight_talkative_df_sent_sentence_week        	=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_week_length']['talkative..sentence_count']}), "week", date_range_dict)
		insight_talkative_df_sent_sentence_weekday     	=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_weekday_length']['talkative..sentence_count']}), "weekday", date_range_dict)
		insight_talkative_df_sent_sentence_dayperiod   	=  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod_length']['date_index'], "length":insight_dict['agg_sent']['unique_msg_dayperiod_length']['talkative..sentence_count']}), "dayperiod", date_range_dict)


		# graphs

		## character
		character_sent_date = dict(
			x=insight_talkative_df_sent_character_date['msg_date'],
			y=insight_talkative_df_sent_character_date['length'],
			name="Median Number of Characters - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)

		character_sent_week = dict(
			x=insight_talkative_df_sent_character_week['msg_date'],
			y=insight_talkative_df_sent_character_week['length'],
			name="Median Number of Characters - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)

		character_sent_weekday = dict(
			x=insight_talkative_df_sent_character_weekday['msg_date'],
			y=insight_talkative_df_sent_character_weekday['length'],
			name="Median Number of Characters - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)


		character_sent_dayperiod = dict(
			x=insight_talkative_df_sent_character_dayperiod['msg_date'],
			y=insight_talkative_df_sent_character_dayperiod['length'],
			name="Median Number of Characters - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)

		## word
		word_sent_date = dict(
			x=insight_talkative_df_sent_word_date['msg_date'],
			y=insight_talkative_df_sent_word_date['length'],
			name="Median Number of Words - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)

		word_sent_week = dict(
			x=insight_talkative_df_sent_word_week['msg_date'],
			y=insight_talkative_df_sent_word_week['length'],
			name="Median Number of Words - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)

		word_sent_weekday = dict(
			x=insight_talkative_df_sent_word_weekday['msg_date'],
			y=insight_talkative_df_sent_word_weekday['length'],
			name="Median Number of Words - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)


		word_sent_dayperiod = dict(
			x=insight_talkative_df_sent_word_dayperiod['msg_date'],
			y=insight_talkative_df_sent_word_dayperiod['length'],
			name="Median Number of Words - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)

		## sentence
		sentence_sent_date = dict(
			x=insight_talkative_df_sent_sentence_date['msg_date'],
			y=insight_talkative_df_sent_sentence_date['length'],
			name="Median Number of Sentences - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)

		)

		sentence_sent_week = dict(
			x=insight_talkative_df_sent_sentence_week['msg_date'],
			y=insight_talkative_df_sent_sentence_week['length'],
			name="Median Number of Sentences - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)

		)

		sentence_sent_weekday = dict(
			x=insight_talkative_df_sent_sentence_weekday['msg_date'],
			y=insight_talkative_df_sent_sentence_weekday['length'],
			name="Median Number of Sentences - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)

		)


		sentence_sent_dayperiod = dict(
			x=insight_talkative_df_sent_sentence_dayperiod['msg_date'],
			y=insight_talkative_df_sent_sentence_dayperiod['length'],
			name="Median Number of Sentences - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dot', width= 1), 
			marker=dict(size=4)

		)

		## sent 
		talkative_sent_graph_day = dict(	
				data=[character_sent_date,word_sent_date,sentence_sent_date]
		)
		insight_plot.append(talkative_sent_graph_day)

		talkative_sent_graph_week = dict(	
				data=[character_sent_week,word_sent_week,sentence_sent_week]
		)
		insight_plot.append(talkative_sent_graph_week)
	
		talkative_sent_graph_weekday = dict(	
				data=[character_sent_weekday,word_sent_weekday,sentence_sent_weekday]
		)
		insight_plot.append(talkative_sent_graph_weekday)

		talkative_sent_graph_dayperiod = dict(	
				data=[character_sent_dayperiod,word_sent_dayperiod,sentence_sent_dayperiod]
		)
		insight_plot.append(talkative_sent_graph_dayperiod)


	
		## STORE
		insight_talkative_dict['agg']   = global_fun.dict_round(insight_talkative_dict_agg)
		insight_talkative_dict['group'] = global_fun.dict_round(insight_talkative_dict_group)
		insight_talkative_dict['time']  = global_fun.dict_round(insight_talkative_dict_time)
		insight_agg_dict['talkative']   = insight_talkative_dict


		# * lengthimbalance
		#----------------------------------------------------------------------------#
		
		insight_lengthimbalance_dict       = {}
		insight_lengthimbalance_dict_agg   = {}
		insight_lengthimbalance_dict_group = {}
		insight_lengthimbalance_dict_time  = {}

		# aggregate
		# **********

		insight_lengthimbalance_dict_agg['01-  Average length imbalance - characters (sent length / received length)']    =  np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['agg_received_response']['unique_msg']['lengthimbalance..length_imbalance_character']]))
		insight_lengthimbalance_dict_agg['02-  Average length imbalance - words (sent length / received length)']         =  np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['agg_received_response']['unique_msg']['lengthimbalance..length_imbalance_word']]))
		insight_lengthimbalance_dict_agg['03-  Average length imbalance - sentences (sent length / received length)']     =  np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['agg_received_response']['unique_msg']['lengthimbalance..length_imbalance_sentence']]))

		# by group
		# **********

		balance_character_count_a  	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_a_received_response']['unique_msg']['lengthimbalance..length_imbalance_character']]))
		balance_word_count_a      	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_a_received_response']['unique_msg']['lengthimbalance..length_imbalance_word']]))
		balance_sentence_count_a  	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_a_received_response']['unique_msg']['lengthimbalance..length_imbalance_sentence']]))

		balance_character_count_b 	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_b_received_response']['unique_msg']['lengthimbalance..length_imbalance_character']]))
		balance_word_count_b      	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_b_received_response']['unique_msg']['lengthimbalance..length_imbalance_word']]))
		balance_sentence_count_b  	 = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_b_received_response']['unique_msg']['lengthimbalance..length_imbalance_sentence']]))

		balance_character_count_none = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_none_received_response']['unique_msg']['lengthimbalance..length_imbalance_character']]))
		balance_word_count_none      = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_none_received_response']['unique_msg']['lengthimbalance..length_imbalance_word']]))
		balance_sentence_count_none  = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_none_received_response']['unique_msg']['lengthimbalance..length_imbalance_sentence']]))

		if (group_none_indic==1):

			insight_lengthimbalance_dict_group['01-  Average length imbalance - characters (sent length / received length)']    =  str(balance_character_count_a) + " / " + str(balance_character_count_b) + " / " + str(balance_character_count_none)
			insight_lengthimbalance_dict_group['02-  Average length imbalance - words (sent length / received length)']         =  str(balance_word_count_a) + " / " + str(balance_word_count_b) + " / " + str(balance_word_count_none)
			insight_lengthimbalance_dict_group['03-  Average length imbalance - sentences (sent length / received length)']     =  str(balance_sentence_count_a) + " / " + str(balance_sentence_count_b) + " / " + str(balance_sentence_count_none)

		else:

			insight_lengthimbalance_dict_group['01-  Average length imbalance - characters (sent length / received length)']    =  str(balance_character_count_a) + " / " + str(balance_character_count_b) 
			insight_lengthimbalance_dict_group['02-  Average length imbalance - words (sent length / received length)']         =  str(balance_word_count_a) + " / " + str(balance_word_count_b)
			insight_lengthimbalance_dict_group['03-  Average length imbalance - sentences (sent length / received length)']     =  str(balance_sentence_count_a) + " / " + str(balance_sentence_count_b) 
		
		## STORE
		insight_lengthimbalance_dict['agg']   = global_fun.dict_round(insight_lengthimbalance_dict_agg)
		insight_lengthimbalance_dict['group'] = global_fun.dict_round(insight_lengthimbalance_dict_group)
		insight_lengthimbalance_dict['time']  = global_fun.dict_round(insight_lengthimbalance_dict_time)
		insight_agg_dict['lengthimbalance']   = insight_lengthimbalance_dict


	#----------------------------------------------------------------------------#
	# nlp
	#----------------------------------------------------------------------------#
	
	elif insight_type == "nlp": 

		# * politeness
		#----------------------------------------------------------------------------#

		insight_politeness_dict       = {}
		insight_politeness_dict_agg   = {}
		insight_politeness_dict_group = {}
		insight_politeness_dict_time  = {}

		# aggregate
		# **********

		insight_politeness_dict_agg['01-  Percent of messages containing at least 1 request - sent emails']        =  global_fun.perc(len(insight_dict['politeness_agg_request_sent']['unique_msg']),len(insight_dict['agg_sent']['unique_msg']))
		insight_politeness_dict_agg['02-  Average politness - sent emails']                                        =  np.nanmean([float(x) for x in insight_dict['agg_sent']['unique_msg']['politeness..politeness']])
		
		insight_politeness_dict_agg['03-  Percent of messages containing at least 1 request - received emails']    =  global_fun.perc(len(insight_dict['politeness_agg_request_received']['unique_msg']),len(insight_dict['agg_received']['unique_msg']))
		insight_politeness_dict_agg['04-  Average politeness - received emails']                                   =  np.nanmean([float(x) for x in insight_dict['agg_received']['unique_msg']['politeness..politeness']])
		
		insight_politeness_dict_agg['05-  Average politeness imbalance - (sent politeness / received politeness)'] =  np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['agg_received_response']['unique_msg']['politeness..politeness_imbalance']]))


		# by group
		# **********

		## sent
		politeness_sent_a             = np.nanmean([float(x) for x in insight_dict['group_a_sent']['unique_msg']['politeness..politeness']])
		request_sent_a                = global_fun.perc(len(insight_dict['politeness_group_a_request_sent']['unique_msg']),len(insight_dict['group_a_sent']['unique_msg']))

		politeness_sent_b             = np.nanmean([float(x) for x in insight_dict['group_b_sent']['unique_msg']['politeness..politeness']])
		request_sent_b                = global_fun.perc(len(insight_dict['politeness_group_b_request_sent']['unique_msg']),len(insight_dict['group_b_sent']['unique_msg']))

		politeness_sent_none          = np.nanmean([float(x) for x in insight_dict['group_none_sent']['unique_msg']['politeness..politeness']])
		request_sent_none             = global_fun.perc(len(insight_dict['politeness_group_none_request_sent']['unique_msg']),len(insight_dict['group_none_sent']['unique_msg']))

		## received
		politeness_received_a         = np.nanmean([float(x) for x in insight_dict['group_a_received']['unique_msg']['politeness..politeness']])
		request_received_a            = global_fun.perc(len(insight_dict['politeness_group_a_request_received']['unique_msg']),len(insight_dict['group_a_received']['unique_msg']))

		politeness_received_b         = np.nanmean([float(x) for x in insight_dict['group_b_received']['unique_msg']['politeness..politeness']])
		request_received_b            = global_fun.perc(len(insight_dict['politeness_group_b_request_received']['unique_msg']),len(insight_dict['group_b_received']['unique_msg']))

		politeness_received_none      = np.nanmean([float(x) for x in insight_dict['group_none_received']['unique_msg']['politeness..politeness']])
		request_received_none         = global_fun.perc(len(insight_dict['politeness_group_none_request_received']['unique_msg']),len(insight_dict['group_none_received']['unique_msg']))


		## imbalance

		politeness_imbalance_a        = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_a_received_response']['unique_msg']['politeness..politeness_imbalance']]))
		politeness_imbalance_b        = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_b_received_response']['unique_msg']['politeness..politeness_imbalance']]))
		politeness_imbalance_none     = np.nanmean(filter(lambda x: x not in [float('inf'),0],[float(x) for x in insight_dict['group_none_received_response']['unique_msg']['politeness..politeness_imbalance']]))
	
		if (group_none_indic==1):

			insight_politeness_dict_group['01-  Percent of messages containing at least 1 request - sent emails']      	 =  str(request_sent_a) + " / " + str(request_sent_b) + " / " + str(request_sent_none)
			insight_politeness_dict_group['02-  Average politness - sent emails']             						  	 =  str(politeness_sent_a) + " / " + str(politeness_sent_b) + " / " + str(politeness_sent_none)
		
			insight_politeness_dict_group['03-  Percent of messages containing at least 1 request - received emails']  	 =  str(request_received_a) + " / " + str(request_received_b) + " / " + str(request_received_none)
			insight_politeness_dict_group['04-  Average politeness - received emails']         						  	 =  str(politeness_received_a) + " / " + str(politeness_received_b) + " / " + str(politeness_received_none)
		
			insight_politeness_dict_group['05-  Average politeness imbalance - (sent politeness / received politeness)'] =  str(politeness_imbalance_a) + " / " + str(politeness_imbalance_b) + " / " + str(politeness_imbalance_none)

		else: 

			insight_politeness_dict_group['01-  Percent of messages containing at least 1 request - sent emails']      	 =  str(request_sent_a) + " / " + str(request_sent_b) 
			insight_politeness_dict_group['02-  Average politness - sent emails']             						  	 =  str(politeness_sent_a) + " / " + str(politeness_sent_b)
		
			insight_politeness_dict_group['03-  Percent of messages containing at least 1 request - received emails']  	 =  str(request_received_a) + " / " + str(request_received_b) 
			insight_politeness_dict_group['04-  Average politeness - received emails']         						  	 =  str(politeness_received_a) + " / " + str(politeness_received_b) 
		
			insight_politeness_dict_group['05-  Average politeness imbalance - (sent politeness / received politeness)'] =  str(politeness_imbalance_a) + " / " + str(politeness_imbalance_b)


		# by time
		# **********
		
		# aggregate
		insight_politeness_df_sent_politeness_date            =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_date_politeness']['date_index'], "politeness":insight_dict['agg_sent']['unique_msg_date_politeness']['politeness..politeness']}), "date", date_range_dict,np.nan)
		insight_politeness_df_sent_politeness_week        	  =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_week_politeness']['date_index'], "politeness":insight_dict['agg_sent']['unique_msg_week_politeness']['politeness..politeness']}), "week", date_range_dict,np.nan)
		insight_politeness_df_sent_politeness_weekday     	  =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_weekday_politeness']['date_index'], "politeness":insight_dict['agg_sent']['unique_msg_weekday_politeness']['politeness..politeness']}), "weekday", date_range_dict,np.nan)
		insight_politeness_df_sent_politeness_dayperiod  	  =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_sent']['unique_msg_dayperiod_politeness']['date_index'], "politeness":insight_dict['agg_sent']['unique_msg_dayperiod_politeness']['politeness..politeness']}), "dayperiod", date_range_dict,np.nan)

		insight_politeness_df_received_politeness_date        =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_date_politeness']['date_index'], "politeness":insight_dict['agg_received']['unique_msg_date_politeness']['politeness..politeness']}), "date", date_range_dict,np.nan)
		insight_politeness_df_received_politeness_week        =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_week_politeness']['date_index'], "politeness":insight_dict['agg_received']['unique_msg_week_politeness']['politeness..politeness']}), "week", date_range_dict,np.nan)
		insight_politeness_df_received_politeness_weekday     =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_weekday_politeness']['date_index'], "politeness":insight_dict['agg_received']['unique_msg_weekday_politeness']['politeness..politeness']}), "weekday", date_range_dict,np.nan)
		insight_politeness_df_received_politeness_dayperiod   =  global_fun.date_reindex(pd.DataFrame({"msg_date":insight_dict['agg_received']['unique_msg_dayperiod_politeness']['date_index'], "politeness":insight_dict['agg_received']['unique_msg_dayperiod_politeness']['politeness..politeness']}), "dayperiod", date_range_dict,np.nan)

		## sent
		politeness_sent_date = dict(
			x=insight_politeness_df_sent_politeness_date['msg_date'],
			y=insight_politeness_df_sent_politeness_date['politeness'],
			name="Average Politeness - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)

		politeness_sent_week = dict(
			x=insight_politeness_df_sent_politeness_week['msg_date'],
			y=insight_politeness_df_sent_politeness_week['politeness'],
			name="Average Politeness - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)

		politeness_sent_weekday = dict(
			x=insight_politeness_df_sent_politeness_weekday['msg_date'],
			y=insight_politeness_df_sent_politeness_weekday['politeness'],
			name="Average Politeness - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)

		)


		politeness_sent_dayperiod = dict(
			x=insight_politeness_df_sent_politeness_dayperiod['msg_date'],
			y=insight_politeness_df_sent_politeness_dayperiod['politeness'],
			name="Average Politeness - Sent Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='solid', width= 1), 
			marker=dict(size=4)


		)

		## received
		politeness_received_date = dict(
			x=insight_politeness_df_received_politeness_date['msg_date'],
			y=insight_politeness_df_received_politeness_date['politeness'],
			name="Average Politeness - Received Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)

		politeness_received_week = dict(
			x=insight_politeness_df_received_politeness_week['msg_date'],
			y=insight_politeness_df_received_politeness_week['politeness'],
			name="Average Politeness - Received Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)

		politeness_received_weekday = dict(
			x=insight_politeness_df_received_politeness_weekday['msg_date'],
			y=insight_politeness_df_received_politeness_weekday['politeness'],
			name="Average Politeness - Received Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)

		)


		politeness_received_dayperiod = dict(
			x=insight_politeness_df_received_politeness_dayperiod['msg_date'],
			y=insight_politeness_df_received_politeness_dayperiod['politeness'],
			name="Average Politeness - Received Emails",
			hoverinfo='none',
			mode = 'lines+markers', 
			line= dict(dash='dash', width= 1), 
			marker=dict(size=4)
			

		)

		## sent
		politeness_graph_day = dict(	
				data=[politeness_sent_date,politeness_received_date]
		)
		insight_plot.append(politeness_graph_day)

		politeness_graph_week = dict(	
				data=[politeness_sent_week,politeness_received_week]
		)
		insight_plot.append(politeness_graph_week)

		politeness_graph_weekday = dict(	
				data=[politeness_sent_weekday,politeness_received_weekday]
		)
		insight_plot.append(politeness_graph_weekday)

		politeness_graph_dayperiod = dict(	
				data=[politeness_sent_dayperiod,politeness_received_dayperiod]
		)
		insight_plot.append(politeness_graph_dayperiod)


	
		## STORE
		insight_politeness_dict['agg']   = global_fun.dict_round(insight_politeness_dict_agg)
		insight_politeness_dict['group'] = global_fun.dict_round(insight_politeness_dict_group)
		insight_politeness_dict['time']  = global_fun.dict_round(insight_politeness_dict_time)
		insight_agg_dict['politeness']   = insight_politeness_dict

		# * sentiment
		#----------------------------------------------------------------------------#

		insight_sentiment_dict       = {}
		insight_sentiment_dict_agg   = {}
		insight_sentiment_dict_group = {}
		insight_sentiment_dict_time  = {}

		# aggregate
		# **********

		insight_sentiment_dict_agg['01-  Percent of messages containing at least 1 positive sentiment (unigram) - sent emails']   	 =  global_fun.perc(len(insight_dict['sentiment_agg_pos_sent']['unique_msg']),len(insight_dict['agg_sent']['unique_msg']))
		insight_sentiment_dict_agg['02-  Percent of messages containing at least 1 negative sentiment (unigram) - sent emails']   	 =  global_fun.perc(len(insight_dict['sentiment_agg_neg_sent']['unique_msg']),len(insight_dict['agg_sent']['unique_msg']))
		
		insight_sentiment_dict_agg['03-  Percent of messages containing at least 1 positive sentiment (unigram) - received emails']   =  global_fun.perc(len(insight_dict['sentiment_agg_pos_received']['unique_msg']),len(insight_dict['agg_received']['unique_msg']))
		insight_sentiment_dict_agg['04-  Percent of messages containing at least 1 negative sentiment (unigram) - received emails']   =  global_fun.perc(len(insight_dict['sentiment_agg_neg_received']['unique_msg']),len(insight_dict['agg_received']['unique_msg']))


		# by group
		# **********

		## sent
		pos_sent_a                    = global_fun.perc(len(insight_dict['sentiment_group_a_pos_sent']['unique_msg']),len(insight_dict['group_a_sent']['unique_msg']))
		neg_sent_a                	  = global_fun.perc(len(insight_dict['sentiment_group_a_neg_sent']['unique_msg']),len(insight_dict['group_a_sent']['unique_msg']))
		pos_received_a                = global_fun.perc(len(insight_dict['sentiment_group_a_pos_received']['unique_msg']),len(insight_dict['group_a_received']['unique_msg']))
		neg_received_a                = global_fun.perc(len(insight_dict['sentiment_group_a_neg_received']['unique_msg']),len(insight_dict['group_a_received']['unique_msg']))

		pos_sent_b                    = global_fun.perc(len(insight_dict['sentiment_group_b_pos_sent']['unique_msg']),len(insight_dict['group_b_sent']['unique_msg']))
		neg_sent_b                	  = global_fun.perc(len(insight_dict['sentiment_group_b_neg_sent']['unique_msg']),len(insight_dict['group_b_sent']['unique_msg']))
		pos_received_b                = global_fun.perc(len(insight_dict['sentiment_group_b_pos_received']['unique_msg']),len(insight_dict['group_b_received']['unique_msg']))
		neg_received_b                = global_fun.perc(len(insight_dict['sentiment_group_b_neg_received']['unique_msg']),len(insight_dict['group_b_received']['unique_msg']))

		pos_sent_none                 = global_fun.perc(len(insight_dict['sentiment_group_none_pos_sent']['unique_msg']),len(insight_dict['group_none_sent']['unique_msg']))
		neg_sent_none                 = global_fun.perc(len(insight_dict['sentiment_group_none_neg_sent']['unique_msg']),len(insight_dict['group_none_sent']['unique_msg']))
		pos_received_none             = global_fun.perc(len(insight_dict['sentiment_group_none_pos_received']['unique_msg']),len(insight_dict['group_none_received']['unique_msg']))
		neg_received_none             = global_fun.perc(len(insight_dict['sentiment_group_none_neg_received']['unique_msg']),len(insight_dict['group_none_received']['unique_msg']))
	
		if (group_none_indic==1):

			insight_sentiment_dict_group['01-  Percent of messages containing at least 1 positive sentiment (unigram) - sent emails']      	 =  str(pos_sent_a) + " / " + str(pos_sent_b) + " / " + str(pos_sent_none)
			insight_sentiment_dict_group['02-  Percent of messages containing at least 1 negative sentiment (unigram) - sent emails']        =  str(neg_sent_a) + " / " + str(neg_sent_b) + " / " + str(neg_sent_none)
			
			insight_sentiment_dict_group['03-  Percent of messages containing at least 1 positive sentiment (unigram) - received emails']  	 =  str(pos_received_a) + " / " + str(pos_received_b) + " / " + str(pos_received_none)
			insight_sentiment_dict_group['04-  Percent of messages containing at least 1 negative sentiment (unigram) - received emails']    =  str(neg_received_a) + " / " + str(neg_received_b) + " / " + str(neg_received_none)

		else: 

			insight_sentiment_dict_group['01-  Percent of messages containing at least 1 positive sentiment (unigram) - sent emails']      	 =  str(pos_sent_a) + " / " + str(pos_sent_b) 
			insight_sentiment_dict_group['02-  Percent of messages containing at least 1 negative sentiment (unigram) - sent emails']        =  str(neg_sent_a) + " / " + str(neg_sent_b)
			
			insight_sentiment_dict_group['03-  Percent of messages containing at least 1 positive sentiment (unigram) - received emails']  	 =  str(pos_received_a) + " / " + str(pos_received_b) 
			insight_sentiment_dict_group['04-  Percent of messages containing at least 1 negative sentiment (unigram) - received emails']    =  str(neg_received_a) + " / " + str(neg_received_b) 
		
		# by category
		# **********

		sentiment_agg_category_agg = go.Bar(
			x=insight_dict['sentiment_agg_breakdown_agg']['key_col'][1:10],
			y=insight_dict['sentiment_agg_breakdown_agg']['key_col_count'][1:10],
			orientation = 'v',
			name="Most Common Sentiments - Overall (Normalised Counts)",
			hoverinfo='none', 
			marker=dict(color='red')
		)	

		sentiment_agg_category_sent = go.Bar(
			x=insight_dict['sentiment_agg_breakdown_sent']['key_col'][1:10],
			y=insight_dict['sentiment_agg_breakdown_sent']['key_col_count'][1:10],
			orientation = 'v',
			name="Most Common Sentiments - Sent Emails (Normalised Counts)",
			hoverinfo='none', 
			marker=dict(color='blue')
		)	
	
		sentiment_agg_category_received = go.Bar(
			x=insight_dict['sentiment_agg_breakdown_received']['key_col'][1:10],
			y=insight_dict['sentiment_agg_breakdown_received']['key_col_count'][1:10],
			orientation = 'v',
			name="Most Common Sentiments - Received Emails (Normalised Counts)",
			hoverinfo='none', 
			marker=dict(color='green')
		)	
	
		sentiment_graph_agg = dict(	
				data=[sentiment_agg_category_agg]
		)
		insight_plot.append(sentiment_graph_agg)

		sentiment_graph_sent = dict(	
				data=[sentiment_agg_category_sent]
		)
		insight_plot.append(sentiment_graph_sent)

		sentiment_graph_received = dict(	
				data=[sentiment_agg_category_received]
		)
		insight_plot.append(sentiment_graph_received)


		## STORE
		insight_sentiment_dict['agg']   = global_fun.dict_round(insight_sentiment_dict_agg)
		insight_sentiment_dict['group'] = global_fun.dict_round(insight_sentiment_dict_group)
		insight_sentiment_dict['time']  = global_fun.dict_round(insight_sentiment_dict_time)
		insight_agg_dict['sentiment']   = insight_sentiment_dict

		# * coordination
		#----------------------------------------------------------------------------#

		insight_coordination_dict       = {}
		insight_coordination_dict_agg   = {}
		insight_coordination_dict_group = {}
		insight_coordination_dict_time  = {}

		# aggregate
		# **********
		score_list = []

		for i in range(0,len(pos_word_list)):

			# position
			pos_tmp = str(i+1)
			if len(pos_tmp) < 2:
				pos_tmp = '0' + pos_tmp

			# word
			word_tmp = pos_word_list[i]

			# stats
			insight_coordination_dict_agg[pos_tmp+'a-  Average **'+word_tmp+'** coordination score']   	     							      = np.nanmean([float(x) for x in insight_dict['agg_sent_reply']['unique_msg']['coordination..score_'+word_tmp]])     
			insight_coordination_dict_agg[pos_tmp+'b-  > Percent of emails containing at least 1 '+word_tmp+' - sent emails']   	    	  = global_fun.perc(len(insight_dict['coordination_agg_'+word_tmp+'_sent']['unique_msg']),len(insight_dict['agg_sent']['unique_msg']))
			insight_coordination_dict_agg[pos_tmp+'c-  > Average '+word_tmp+' word fraction - sent emails']   	             	              = np.nanmean([float(x) for x in insight_dict['agg_sent']['unique_msg']['coordination..pos_prop_'+word_tmp]])                               
			insight_coordination_dict_agg[pos_tmp+'d-  > Percent of emails containing at least 1 '+word_tmp+' - sent emails (as a response)'] = global_fun.perc(len(insight_dict['coordination_agg_'+word_tmp+'_reply_sent']['unique_msg']),len(insight_dict['agg_sent_reply']['unique_msg']))
			insight_coordination_dict_agg[pos_tmp+'e-  > Average '+word_tmp+' word fraction - sent emails (as a response)']   	              = np.nanmean([float(x) for x in insight_dict['agg_sent_reply']['unique_msg']['coordination..pos_prop_'+word_tmp]])                               

			score_list.append(insight_coordination_dict_agg[pos_tmp+'a-  Average **'+word_tmp+'** coordination score'])

		insight_coordination_dict_agg['99a-  Average **aggregate** coordination score']   	     							                  = np.nanmean([float(x) for x in insight_dict['agg_sent_reply']['unique_msg']['coordination..score_agg']])     
		score_list.append(insight_coordination_dict_agg['99a-  Average **aggregate** coordination score'])

		# by group
		# **********

		# for i in range(0,len(pos_word_list)):

		# 	# position
		# 	pos_tmp = str(i+1)
		# 	if len(pos_tmp) < 2:
		# 		pos_tmp = '0' + pos_tmp

		# 	# word
		# 	word_tmp = pos_word_list[i]

		# 	# stats
		# 	group_a_score      = np.nanmean([float(x) for x in insight_dict['group_a_sent_reply']['unique_msg']['coordination..score_'+word_tmp]])   
		# 	group_b_score      = np.nanmean([float(x) for x in insight_dict['group_b_sent_reply']['unique_msg']['coordination..score_'+word_tmp]])   
		# 	group_none_score   = np.nanmean([float(x) for x in insight_dict['group_none_sent_reply']['unique_msg']['coordination..score_'+word_tmp]]) 

		# 	group_a_prop       = np.nanmean([float(x) for x in insight_dict['group_a_sent_reply']['unique_msg']['coordination..pos_prop_'+word_tmp]])      
		# 	group_b_prop       = np.nanmean([float(x) for x in insight_dict['group_b_sent_reply']['unique_msg']['coordination..pos_prop_'+word_tmp]])  
		# 	group_none_prop    = np.nanmean([float(x) for x in insight_dict['group_none_sent_reply']['unique_msg']['coordination..pos_prop_'+word_tmp]])  

		# 	# aggregate
		# 	if (group_none_indic==1):

		# 		insight_coordination_dict_group[pos_tmp+'a-  Average **'+word_tmp+'** coordination score']   	     							      = str(group_a_score) + " / " + str(group_b_score) + " / " + str(group_none_score)    
		# 		insight_coordination_dict_group[pos_tmp+'b-  > Average '+word_tmp+' word fraction - sent emails (as a response)']   	              = str(group_a_prop) + " / " + str(group_b_prop) + " / " + str(group_none_prop)                             
	
		# 	else: 

		# 		insight_coordination_dict_group[pos_tmp+'a-  Average **'+word_tmp+'** coordination score']   	     							      = str(group_a_score) + " / " + str(group_b_score) 
		# 		insight_coordination_dict_group[pos_tmp+'b-  > Average '+word_tmp+' word fraction - sent emails (as a response)']   	              = str(group_a_prop) + " / " + str(group_b_prop)                           
	
		group_a_agg_score      = np.nanmean([float(x) for x in insight_dict['group_a_sent_reply']['unique_msg']['coordination..score_agg']])   
		group_b_agg_score      = np.nanmean([float(x) for x in insight_dict['group_b_sent_reply']['unique_msg']['coordination..score_agg']])   
		group_none_agg_score   = np.nanmean([float(x) for x in insight_dict['group_none_sent_reply']['unique_msg']['coordination..score_agg']]) 

		## agg score
		if (group_none_indic==1):
			insight_coordination_dict_group[pos_tmp+'a-  Average **aggregate** coordination score']   	     							           = str(group_a_agg_score) + " / " + str(group_b_agg_score) + " / " + str(group_none_agg_score)   
		else:
			insight_coordination_dict_group[pos_tmp+'a-  Average **aggregate** coordination score']   	     							           = str(group_a_agg_score) + " / " + str(group_b_agg_score) 

		# graph
		# **********

		score_name = sum([pos_word_list, ["agg"]], [])

		coordination_agg = go.Bar(
			x=score_name,
			y=score_list,
			orientation = 'v',
			name="Linguistic Coordination Scores",
			hoverinfo='none'
		)	

		coordination_graph_agg = dict(	
				data=[coordination_agg]
		)
		insight_plot.append(coordination_graph_agg)

		## STORE
		insight_coordination_dict['agg']   = global_fun.dict_round(insight_coordination_dict_agg)
		insight_coordination_dict['group'] = global_fun.dict_round(insight_coordination_dict_group)
		insight_coordination_dict['time']  = global_fun.dict_round(insight_coordination_dict_time)
		insight_agg_dict['coordination']   = insight_coordination_dict

	# ------------------------------------
	# ------------------------------------

	# Enumerate & Combine graphs
	# ------------------------------------
	insight_plot    = json.dumps(insight_plot, cls=plotly.utils.PlotlyJSONEncoder)
	insight_plot_id = ['graph-{}'.format(i) for i, _ in enumerate(insight_plot)]

	# return
	return(insight_agg_dict, insight_plot, insight_plot_id)



#----------------------------------------------------------------------------#
#			                      End                                        #
#----------------------------------------------------------------------------#
