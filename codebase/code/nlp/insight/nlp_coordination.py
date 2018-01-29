## Module    > nlp_coordination
## Functions > coordination


# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init_var__ import *

sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
from coordination import coordination_score

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
def coordination(link_id,msg_id, msg_threadid, msg_data, link_data, conver_data, msg_text_data, contact_data):
	
	# print("Launching - coordination")

	"""
				
	"""
	global global_var

	# initialize
	coordination_df_tmp = pd.DataFrame({'link_id':link_id})

	# insight generation successful
	try:
	
		# individual word categories
		word_list = np.array([msg_text_data[x].pos_count.keys() for x in msg_id])[0]

		# contact level aggregates
		link_contact                             	  = list(set([contact_data[link_data[x].link_contact].contact_id for x in link_id]))
		link_contact_link_id                     	  = [contact_data[x].link_id_outbox for x in link_contact]

		link_contact_coordination_score          	  = [coordination_score(x, link_data, msg_text_data, word_list) for x in link_contact_link_id]
		link_contact_coordination_score_dict     	  = dict([(x,y) for (x,y) in zip(link_contact, link_contact_coordination_score)])
 		
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
			coordination_df_tmp[word_list_col_prop]    = np.array([global_fun.perc(msg_text_data[x].pos_count[word_list_name], msg_text_data[x].word_count) for x in msg_id])

			coordination_df_tmp[word_list_col_score]   = np.array([link_contact_coordination_score_dict[link_data[x].link_contact][word_list_name] for x in link_id])

		## aggregate coordination
		coordination_df_tmp['coordination..score_agg'] = np.array([link_contact_coordination_score_dict[link_data[x].link_contact]['agg_coordination'] for x in link_id])

	# insight generation unsuccessful
	except Exception as e: 
		
		# error message
		print("Error Encountered - coordination")
		print(e)

		# append to error list
		global_var['status_feature_error'].append("coordination")
		
		coordination_df_tmp              		     = coordination_df_tmp

	# return
	# print("Successfully Completed - coordination")
	return(coordination_df_tmp)


#---------------------------------------------#