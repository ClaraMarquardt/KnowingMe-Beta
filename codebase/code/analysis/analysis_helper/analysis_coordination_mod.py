# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_coordination_mod
# Purpose:      Module - Define coordination analysis functions
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
app_root             = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *
from __init_setting__ import *

# Dependencies - Internal
sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# coordination_score
#---------------------------------------------#
def coordination_score(link_list, link_data, msg_text_data, word_list):

	# print("Launching - coordination_score")

	"""

	"""
	
	# initialize
	# --------------
	coord_score_dict = {}

	# word class specific
	# --------------
	for word_class in word_list:

		if (len(link_list))>0:

			# overall probability
			# --------------

			## total number of responses
			total_response                   = len([x for x in link_list if link_data[x].link_reply==1])

			## number of responses containing >=1 word
			total_response_contain_word      = len([x for x in link_list if link_data[x].link_reply==1 and msg_text_data[link_data[x].msg_id].pos_indic[word_class]==1])
		
			## >>> overall probability
			if total_response!=0:
				agg_prob   = float(total_response_contain_word)/total_response
			else:
				agg_prob   = np.nan

			# conditional probability
			# --------------

			## total number of responses | original email contains the word
			total_response_cond        		 = len([x for x in link_list if link_data[x].link_reply==1 and msg_text_data[link_data[x].link_reply_id[0]].pos_indic[word_class]==1])
			
			## number of responses containing >=1 word  | original email contains the word
			total_response_contain_word_cond = len([x for x in link_list if link_data[x].link_reply==1 and msg_text_data[link_data[x].link_reply_id[0]].pos_indic[word_class]==1 and msg_text_data[link_data[x].msg_id].pos_indic[word_class]==1])
	
			## >>> conditional probability
			if total_response_cond!=0:
				cond_prob = float(total_response_contain_word_cond)/total_response_cond
			else:
				cond_prob = np.nan
	
			# score 
			# --------------
			if np.all(pd.notnull([cond_prob,agg_prob ])):
				
				coord_score = cond_prob - agg_prob
				coord_score_dict[word_class] = coord_score

			else:
				coord_score_dict[word_class] = np.nan
		else:

			coord_score_dict[word_class] = np.nan
	
	# aggregate score
	# --------------
	ind_score = np.array([coord_score_dict[x] for x in coord_score_dict.keys()])

	if np.any(pd.notnull(ind_score)):

		coord_score_dict['agg_coordination'] = np.nanmean(ind_score)

	else:
		
		coord_score_dict['agg_coordination'] = np.nan

	return(coord_score_dict)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#