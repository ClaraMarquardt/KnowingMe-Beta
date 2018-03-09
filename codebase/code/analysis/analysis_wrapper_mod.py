# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_wrapper_mod
# Purpose:      Module - Define analysis wrapper functions
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
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialization')))
from __init_lib__ import *
from __init_setting__ import *
from __init_global__ import *

# Dependencies - Internal
from analysis_helper import *  

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *


#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

def analysis_wrapper(msg_text, insight):

	try: 
		
		# prepare
		msg_text = [str(msg_text)]
		msg_id   = [1]
	
		# process
		msg_text_parser     = analysis_msg_class_mod.text
		msg_text_parsed     = [msg_text_parser(x,y) for (x,y) in zip(msg_text, msg_id)]
		msg_text_parsed     = dict([(x,y) for (x,y) in zip(msg_id, msg_text_parsed)])
	
		# extract
		if (insight=="politeness"):
	
			insight_temp = msg_text_parsed[1].polite
	
			if (np.isnan(insight_temp)):
				return("No Requests")
			else:
				return(insight_temp)
			
		
		elif (insight=="sentiment"):
	
			insight_temp = msg_text_parsed[1].sentiment_score_score_vader
	
			if (np.isnan(insight_temp)):
				return("No Sentiment Features")
			else:
				return(insight_temp)
	
	except Exception as e: 

		insight_temp = "Retry!"
		return(insight_temp)

		
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
