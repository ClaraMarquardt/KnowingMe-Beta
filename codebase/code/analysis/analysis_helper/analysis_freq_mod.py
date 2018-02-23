# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_freq_mod
# Purpose:      Module - Define frequency analysis functions
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

# date_agg
# ---------------------------------------------#

def date_agg(date_list):
	
	# print("Launching - date_agg")

	"""

	"""

	# initialize
	# ----------------

	# aggregate
	dcounts    = pd.DataFrame(date_list)
	dcounts    = dcounts[0].groupby(dcounts[0], sort=False).count()
	dc 		   = dcounts.tolist()
	data_guess = dcounts.index.tolist()

	# return
	# print("Successfully Completed - date_freq")
	return([data_guess, dc])


# date_freq
# ---------------------------------------------#

def date_freq(date_list):
	
	# print("Launching - date_freq")

	"""

	"""

	# initialize
	# ----------------


	try: 
		
		# aggregate
	 	[data_guess, dc]         = date_agg(date_list)

		# sort
		data_guess = [x for y, x in sorted(zip(dc,data_guess), reverse=True)]
		dc = [y for y, x in sorted(zip(dc,data_guess), reverse=True)]

		# top 5
		date_1 = data_guess[0:1]
		date_2 = data_guess[1:2]
		date_3 = data_guess[2:3]
		date_4 = data_guess[3:4]
		date_5 = data_guess[4:5]
	
		date_1_freq = dc[0:1]
		date_2_freq = dc[1:2]
		date_3_freq = dc[2:3]
		date_4_freq = dc[3:4]
		date_5_freq = dc[4:5]

	except Exception as e: 

		date_1 = np.nan
		date_2 = np.nan
		date_3 = np.nan
		date_4 = np.nan
		date_5 = np.nan		

		date_1_freq = np.nan
		date_2_freq = np.nan
		date_3_freq = np.nan
		date_4_freq = np.nan
		date_5_freq = np.nan		

	# return
	# print("Successfully Completed - date_freq")
	return([date_1, date_2, date_3, date_4, date_5, 
		date_1_freq, date_2_freq, date_3_freq, date_4_freq, date_5_freq])



#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
