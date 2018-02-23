# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_clean_mod
# Purpose:      Module - Define clean analysis functions
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

# clean_text
#---------------------------------------------#

def clean_text(msg_text):
	
	# print("Launching - clean_text")

	"""
		
	"""

	# initialize
	if pd.isnull(msg_text):
		msg_text_clean = str(msg_text)
	else:
		msg_text_clean = msg_text

	# cleaning successful
	try: 
	
		# omit non-message related text (e.g. forwarded emails, etc.)
		msg_text_clean = msg_text_clean.split("\n>")[0]
		msg_text_clean = msg_text_clean.split("Begin forwarded message:")[0]
		msg_text_clean = msg_text_clean.split("---------- Forwarded message ---------")[0]
		msg_text_clean = msg_text_clean.split("________________________________")[0]
		msg_text_clean = msg_text_clean.split("-----Original Message-----")[0]
		msg_text_clean = re.sub("From:.*Subject:.*", "", msg_text_clean,flags=re.DOTALL)
		msg_text_clean = re.sub("On.*<.*>.*wrote:", "", msg_text_clean,flags=re.DOTALL)
		msg_text_clean = re.sub("On.*wrote:", "", msg_text_clean,flags=re.DOTALL)
		msg_text_clean = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}.*<.*>:","", msg_text_clean,flags=re.DOTALL)

		# replace special characters
		msg_text_clean = re.sub("&#39;|&quot;|&lt;|&gt;"," ",msg_text_clean)

		# replace superfluous spaces, line breaks, etc. 
		msg_text_clean = re.sub("([\n]*[\r]*[\n]*)*$", "", msg_text_clean)
		msg_text_clean = re.sub("^([\n]*[\r]*[\n]*)*", "", msg_text_clean)
		msg_text_clean = re.sub("[ ]{2,}"," ",msg_text_clean)
		msg_text_clean = re.sub("^[ ]|[ ]$","",msg_text_clean)

	# cleaning unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - clean_text")
		print(e)

		msg_text_clean = np.nan

	# return
	# print("Successfully Completed - clean_text")
	return(msg_text_clean)


# clean_date
#---------------------------------------------#

def clean_date(msg_date):
	
	# print("Launching - clean_date")

	"""
		
	"""

	# initialize
	msg_date_clean = msg_date

	try: 
	
		# parse date format & convert to datetime object
		msg_date_clean = parser.parse(msg_date_clean)
		msg_date_clean = pd.to_datetime(msg_date_clean,errors='ignore',utc=True)


	# cleaning unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - clean_date")
		print(e)

		msg_date_clean = datetime.datetime(1990, 1, 1, 1, 1, 1)
		msg_date_clean = pd.to_datetime(msg_date_clean,errors='ignore',utc=True)
	
	# return
	# print("Successfully Completed - clean_date")
	return(msg_date_clean)

# add_date
#---------------------------------------------#

def add_date(date):
	
	# print("Launching - add_date")

	"""
	
	"""

	# initialize
	date = pd.to_datetime(date)

	try: 

		## basic date/time components - generate
		msg_date_day      = int(date.strftime('%d'))
		msg_date_weekday  = int(date.strftime('%w'))
		msg_date_week     = int(date.strftime('%W'))
		msg_date_month    = int(date.strftime('%m'))
		msg_date_hour     = int(date.strftime('%H'))
		msg_date_date     = date.strftime('%m-%d-%Y')

		## new date var > indictors
		msg_date_daypart  = "/"
		if (msg_date_hour>6) & (msg_date_hour<12):
			msg_date_daypart     = "1-morning (6am-noon)"
		elif (msg_date_hour>=12) & (msg_date_hour<21):
			msg_date_daypart   = "2-afternoon (noon-9pm)"
		elif (msg_date_hour>=21) | (msg_date_hour<=06):
			msg_date_daypart  = "3-night (9pm-6am)"

		## basic date/time components - format
		map_dayofweek 	      = {0:'0-Sunday',1:'1-Monday',2:'2-Tuesday',3:'3-Wednesday',4:'4-Thursday',5:'5-Friday',6:'6-Saturday'}
		map_month    	   	  = {0:'0-Jan',1:'1-Feb',2:'2-March',3:'3-April',4:'4-May',5:'5-June',6:'6-July',7:'7-Aug',8:'8-Sept',9:'9-Oct', 10:'10-Nov', 11:'11-Dec'}

		msg_date_month        = pd.Series(msg_date_month).map(map_month)[0]
		msg_date_weekday      = pd.Series(msg_date_weekday).map(map_dayofweek)[0]
		msg_date_week         = "Week " + str(msg_date_week)	
		msg_date_hour      	  = "Hour " + str(msg_date_hour)  
		msg_date_weekday_hour = str(msg_date_weekday) + " - " + str(msg_date_hour)
	
	# cleaning unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - add_date")
		print(e)

		## basic date/time components
		msg_date_daypart      = np.nan
		msg_date_day    	  = np.nan
		msg_date_weekday	  = np.nan
		msg_date_week   	  = np.nan 
		msg_date_month  	  = np.nan
		msg_date_hour   	  = np.nan
		msg_date_date   	  = np.nan
		msg_date_weekday_hour = np.nan

	# return
	# print("Successfully Completed - add_date")
	return(msg_date_date, msg_date_day, msg_date_week, msg_date_hour, msg_date_daypart, msg_date_month, msg_date_weekday, msg_date_weekday_hour)



# clean_contact
#---------------------------------------------#

def clean_contact(msg_contact):

	# print("Launching - clean_contact")

	"""
		
	"""

	# initialize
	msg_contact_clean = msg_contact
	msg_omit_word     = "\(cron daemon\)|\(via google docs\)"

	try: 

		if pd.notnull(msg_contact_clean):

			msg_contact_clean = re.sub("\n|\t|\r","",msg_contact_clean)
			msg_contact_clean = re.sub(msg_omit_word, "", msg_contact_clean)
			msg_contact_clean_tmp = []
			
			for line in csv.reader([msg_contact_clean], skipinitialspace=True):
				msg_contact_clean_tmp.append(line)
			
			msg_contact_clean = msg_contact_clean_tmp[0]
			msg_contact_clean = [re.sub(","," ",x) for x in msg_contact_clean] 
			msg_contact_clean = [re.sub("[ ]{2,}"," ",x) for x in msg_contact_clean] 
			msg_contact_clean = [re.sub("^\.","",x) for x in msg_contact_clean] 
			msg_contact_clean = [re.sub("^\.","",x) for x in msg_contact_clean] 
			msg_contact_clean = [str.lower(x) for x in msg_contact_clean if x] 
			msg_contact_clean = [re.sub(msg_omit_word,"",x) for x in msg_contact_clean] 
			msg_contact_clean = [x for x in msg_contact_clean if x]

			# separate names and contacts
			msg_contact_clean_name       = [re.sub("(.*)<(.*)","\\1",x) for x in msg_contact_clean]
			msg_contact_clean_name       = [re.sub("^$","/",x) for x in msg_contact_clean_name]
			msg_contact_clean_address    = [re.sub("(.*)<(.*)", "\\2", x) for x in msg_contact_clean]
			msg_contact_clean_address 	 = [re.sub("(.*)>(.*)", "\\1", x) for x in msg_contact_clean_address]	
			
			# clean names
			msg_contact_clean_name       = [re.sub("[ ]*$","",x) for x in msg_contact_clean_name]
			msg_contact_clean_name       = [re.sub("^[ ]*","",x) for x in msg_contact_clean_name]

			# clean addresses
			msg_contact_clean_address    = [re.sub("[ ]*$","",x) for x in msg_contact_clean_address]
			msg_contact_clean_address    = [re.sub("^[ ]*","",x) for x in msg_contact_clean_address]

		else:
			
			msg_contact_clean_name    = []
			msg_contact_clean_address = []

	# cleaning unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - clean_contact")
		print(e)

		msg_contact_clean_name    = []
		msg_contact_clean_address = []

	msg_contact_clean_name		  = [x for x in msg_contact_clean_name if x not in ['none']]
	msg_contact_clean_address     = [x for x in msg_contact_clean_address if x not in ['none']]

	# return
	# print("Successfully Completed - clean_contact")
	return({"name":np.array(msg_contact_clean_name), "address": np.array(msg_contact_clean_address)})



#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#