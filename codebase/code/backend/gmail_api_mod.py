# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         gmail_api_mod
# Purpose:      Module - Define gmail api functions
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
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Initialize
sys.path.append(os.path.normpath(os.path.join(app_root, 'initialize')))
from __init_lib__ import *
from __init_setting__ import *
from __init_global__ import *

#----------------------------------------------------------------------------#
#			                     Helper Functions                            #
#----------------------------------------------------------------------------#

# get_email_list
#---------------------------------------------#
def get_email_list(service, user, filter, max_result_page=200):
	
	email_list = []
	email_list_raw = service.users().messages().list(userId=user, q=filter,
		maxResults=max_result_page, includeSpamTrash=False).execute()
	
	if 'messages' in email_list_raw:
		email_list.extend(email_list_raw['messages'])
	
	while 'nextPageToken' in email_list_raw:
		page_token = email_list_raw['nextPageToken']
		email_list_raw = service.users().messages().list(userId=user,  q=filter, 
			maxResults=max_result_page, includeSpamTrash=False, pageToken=page_token).execute()
		email_list.extend(email_list_raw['messages'])
	
	return email_list

# get_diff_range
#---------------------------------------------#
def get_diff_range(earliest_date_temp, latest_date_temp):
	
	diff_temp  = int((parser.parse(str(latest_date_temp)) - parser.parse(str(earliest_date_temp))).days) + 1
	
	range_temp = [(datetime.datetime.strptime(str(latest_date_temp),'%m/%d/%Y') - datetime.timedelta(days=x)).strftime("%m/%d/%Y") for x in range(0,diff_temp)]

	return(diff_temp, range_temp)

# get_msg_text
#---------------------------------------------#
def get_msg_text(msg):
	
	# recursive parsing function
	def rec_msg_parse(msg_element):
		messageMainType = msg_element.get_content_maintype()
		if messageMainType == 'multipart':
			for part in msg_element.get_payload():
				if part.get_content_maintype() == 'text' and len(part.get_payload())>0:
					return part.get_payload(decode=True)
				elif part.get_content_maintype() == 'multipart':
					msg_text_temp=rec_msg_parse(part)
					if len(msg_text_temp)>0:
						return(msg_text_temp)
		elif messageMainType == 'text':
			return msg_element.get_payload(decode=True)
	

	# execute
	msg_str  = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
	mime_msg = email.message_from_string(msg_str)
	msg_text = rec_msg_parse(mime_msg)
	
	return msg_text

# get_msg_meta
#---------------------------------------------#
def get_msg_meta(msg):
	
	# define globals
	global error_count
	global excluded_count
	global service

	# format
	msg_str  = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
	mime_msg = email.message_from_string(msg_str)

	# initialize
	msg_meta = {}

	# id (GMAIL)
	msg_meta['msg_id']       = msg['id']
	msg_meta['msg_threadid'] = msg['threadId']

	# response to
	msg_meta['msg_id_mime']              = mime_msg['Message-ID']
	if 'In-Reply-To' in mime_msg.keys():
		msg_meta['msg_reply_to_id_mime'] = mime_msg['In-Reply-To']
	else:
		msg_meta['msg_reply_to_id_mime'] = np.nan

	# labels (GMAIL)
	msg_meta['msg_label']   = msg['labelIds']
	
	# date (MAIL) > Convert from UTC to local timezone
	msg_meta['msg_date']    = int(msg['internalDate'])
	msg_meta['msg_date']    = datetime.datetime.utcfromtimestamp(msg_meta['msg_date']/1000)
	msg_meta['msg_date']    = str(msg_meta['msg_date'] - datetime.timedelta(hours=timezone_offset))

	# sender/recipient (MAIL)
	msg_meta['msg_from']    = mime_msg["from"]
	msg_meta['msg_to']      = mime_msg["to"]
	msg_meta['msg_cc']      = mime_msg["cc"]
	msg_meta['msg_bcc']     = mime_msg["bcc"]

	# subject (MAIL)
	msg_meta['msg_subject'] = clean_msg_text(mime_msg["subject"])

	# meta labels
	
	# inbox/outbox - based on sender address	
	if own_address in msg_meta['msg_from']:
		msg_meta['msg_inbox_outbox'] = "outbox"
	else:
		msg_meta['msg_inbox_outbox'] = "inbox"

	print("# " + msg_meta['msg_id'])		
	print(msg_meta['msg_from'])
	print(msg_meta['msg_label'])
	print(msg_meta['msg_inbox_outbox'])	

	return(msg_meta)

# clean_msg_text
#---------------------------------------------#
def clean_msg_text(msg_text):
	
	# omit forwarded emails, etc.	
	msg_text_clean = msg_text.split("\n>")[0]
	msg_text_clean = msg_text_clean.split("Begin forwarded message:")[0]
	msg_text_clean = msg_text_clean.split("---------- Forwarded message ---------")[0]
	msg_text_clean = msg_text_clean.split("________________________________")[0]
	msg_text_clean = msg_text_clean.split("-----Original Message-----")[0]
	
	msg_text_clean = re.sub("From:.*Subject:.*", "", msg_text_clean,flags=re.DOTALL)
	msg_text_clean = re.sub("On.*<.*>.*wrote:", "", msg_text_clean,flags=re.DOTALL)
	msg_text_clean = re.sub("On.*wrote:", "", msg_text_clean,flags=re.DOTALL)
	msg_text_clean = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}.*<.*>:","", msg_text_clean,flags=re.DOTALL)
	msg_text_clean = re.sub("(\r\n[\r]*[\n]*){1,}", "\n", msg_text_clean)
	msg_text_clean = re.sub("(\n\r[\n]*[\r]*){1,}", "\n", msg_text_clean)
	msg_text_clean = re.sub("(<--)(.*)(-->)", "", msg_text_clean)
	msg_text_clean = re.sub("(<!DOCTYPE html>)(.*)(</html>)", "", msg_text_clean)

	# basic	- special characters
	msg_text_clean = re.sub("&#39;|&quot;|&lt;|&gt;"," ",msg_text_clean)
	
	# basic - spaces
	msg_text_clean = msg_text_clean.replace("[ ]{2,}", "")
	msg_text_clean = re.sub("^[ ]|[ ]$","",msg_text_clean)

	return(msg_text_clean)
	
# process_email
#---------------------------------------------#
def process_email(request_id, response, exception):

	# define globals
	global error_count
	global error_list
	global excluded_count
	global global_var
	global store_dir

	global_var['status_email_load'] = global_var['status_email_load']+1

	print("---------------------------")
	
	try: 
	
		# Obtain the email meta-data
		email_meta             = get_msg_meta(response)

		# Obtain the email-text
		email_text 	           = get_msg_text(response)
		email_text_clean       = clean_msg_text(email_text)

		if (len(re.sub("\r|\n", "", email_text_clean))>0):
				
			# Combine the meta data & text
			email_data 			   = email_meta
			email_data['msg_text'] = email_text_clean
		
			# Save the email
			if email_data['msg_inbox_outbox'] == 'inbox':
				email_filename=os.path.normpath(os.path.join(store_dir, "inbox", 'email_' + email_data['msg_id'] + '_' + email_data['msg_inbox_outbox'] + '_' + parser.parse(email_data['msg_date']).strftime('%m_%d_%Y') + '.p'))
			else:
				email_filename=os.path.normpath(os.path.join(store_dir, "outbox", 'email_' + email_data['msg_id'] + '_' + email_data['msg_inbox_outbox'] + '_' + parser.parse(email_data['msg_date']).strftime('%m_%d_%Y') + '.p'))
		
			pickle.dump(email_data, open(email_filename, "wb" ))
			print("save")

			print("---------------------------")

		else:

				print("Empty Email")
				print(email_text_clean)
	
				try: 
			
					error_list.append(email_meta['msg_id'])

				except Exception as e: 

					print("Empty Email - Not added to error list")
				
	except Exception as e: 

		print("Error Encountered")
		print(e)
		error_count = error_count + 1

		try: 
			
			error_list.append(email_meta['msg_id'])

		except Exception as e: 

			print("Error Encountered - Not added to error list")
			print(e)


# process_date
#---------------------------------------------#
def process_date(request_id, response, exception):

	# define flobals	
	global date_list

	## format
	msg_str  = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
	mime_msg = email.message_from_string(msg_str)

	mime_msg_date = mime_msg['date']
	mime_msg_date = parser.parse(mime_msg_date)
	mime_msg_date = mime_msg_date.strftime("%m-%d")

	date_list.append(mime_msg_date)


#----------------------------------------------------------------------------#
#			                     Functions                                   #
#----------------------------------------------------------------------------#

# overview_email
#---------------------------------------------#
def overview_email(service, user, current_date, timelag_overview, overview_day, birthday_day, output_dir, timezone_utc_offset):

	# Define globals
	global global_var

	# Define filenames
	overview_filename=os.path.normpath(os.path.join(output_dir, "other", 'overview_'+ datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))
	birthday_filename=os.path.normpath(os.path.join(output_dir, "other", 'birthday_'+ datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))

	# Initialize global var
	global_var['status_overview_max'] = len(range(timelag_overview,overview_day+timelag_overview))

	# Overview file do not exist > Generate
	if not os.path.exists(overview_filename):
	
		# initialize
		email_dict = dict()
		
		# loop over days
		for i in range(timelag_overview,overview_day+timelag_overview): 


			# define end dates
			date_start = (datetime.datetime.strptime(current_date,'%m/%d/%Y') - datetime.timedelta(days=i)).strftime("%m/%d/%Y")
			date_end   = (datetime.datetime.strptime(current_date,'%m/%d/%Y') - datetime.timedelta(days=i-1)).strftime("%m/%d/%Y")

			# convert to UTC
			date_start_utc  = parser.parse(date_start) + datetime.timedelta(hours=timezone_utc_offset)
			date_end_utc    = parser.parse(date_end)   + datetime.timedelta(hours=timezone_utc_offset)

			date_start_utc_timestamp  = str(calendar.timegm((parser.parse(date_start) + datetime.timedelta(hours=timezone_utc_offset)).timetuple())).split(".")[0]
			date_end_utc_timestamp    = str(calendar.timegm((parser.parse(date_end)   + datetime.timedelta(hours=timezone_utc_offset)).timetuple())).split(".")[0]

			# define date filter
			date_filter = "before: {0} after: {1}".format(date_end_utc_timestamp, date_start_utc_timestamp)
			exclude_text = ["opt-out", "viewing the newsletter", "edit your preferences", "update profile", "smartunsuscribe","secureunsuscribe","group-digests","yahoogroups"]
			text_filter = " ".join(["AND NOT: \""+a+"\"" for a in exclude_text])
			q  = "(category:personal OR label:sent) AND ("+ date_filter +") " + text_filter + " -from:'no-reply@accounts.google.com'"
			
			# obtain email_ids
			msg_list = get_email_list(service, user, q)
			msg_list =[msg['id'] for msg in msg_list]

			# store in dictionary
			date_start_format = str(datetime.datetime.strptime(date_start,'%m/%d/%Y').strftime("%m/%d/%Y"))
			email_dict[date_start_format] = msg_list
			global_var['status_overview_load'] = global_var['status_overview_load']+1

		# save
		with open(overview_filename, 'wb') as out_file:
			pickle.dump(email_dict, out_file)

	else:
		
		time.sleep(3)

		global_var['status_overview_load'] = global_var['status_overview_max']
		
		time.sleep(3)

	# Birthday file do not exist > Generate
	if not os.path.exists(birthday_filename):
	
		# initialize
		global date_list 
		date_list = []

		# define birthday filter
		birthday_query = [('in:inbox +{"happy birthday OR bday"} -{belated OR late}')]
		
		# obtain email_ids
		msg_list = get_email_list(service, user, birthday_query)
		msg_list =[msg['id'] for msg in msg_list]
		
		if len(msg_list)>0:

			for i in range(0,int(np.ceil(len(msg_list)/25))+1):
			
				start = np.minimum(i*25, len(msg_list)-1)
				end   = np.minimum(start+25, len(msg_list)-1)
	
				if end>start:
					msg_list_temp=msg_list[start:end]
				else:
					msg_list_temp=msg_list[start]
		
				# Batch process emails 
				batch = service.new_batch_http_request()
				for msg_id in msg_list_temp:
					batch.add(service.users().messages().get(userId=user, id=msg_id, format="raw", metadataHeaders =["Date"]), callback=process_date)
				batch.execute()
	
		date_dict = dict()
		date_dict['birthday'] = date_list

		with open(birthday_filename, 'wb') as out_file:
			pickle.dump(date_dict, out_file)


# timeframe_email
#---------------------------------------------#
def timeframe_email(current_date, timelag_day, timelag_overview, min_day, overview_day, email_max, output_dir):

	# default earliest / latest date
	email_latest   = (datetime.datetime.strptime(current_date,'%m/%d/%Y') - datetime.timedelta(days=timelag_day)).strftime("%m/%d/%Y")
	email_earliest = (datetime.datetime.strptime(current_date,'%m/%d/%Y') - datetime.timedelta(days=(timelag_day+min_day))).strftime("%m/%d/%Y")

	## load overview file 
	email_dict_file    = os.path.normpath(os.path.join(output_dir, "other", 'overview_'+ datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))
	with open(email_dict_file) as file:
		email_dict     = pickle.load(file)

	# obtain the date diff / range
	email_diff, email_range   = get_diff_range(email_earliest, email_latest)

	# subset emails 
	msg_list    = [email_dict[x] for x in email_range]
	msg_list    = sum(msg_list, [])

	while (len(msg_list) < email_max and (email_diff + timelag_day) < (overview_day + timelag_overview)):

		# update date
		email_earliest = (datetime.datetime.strptime(str(email_earliest),'%m/%d/%Y') - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

		# update date diff / range
		email_diff, email_range   = get_diff_range(email_earliest, email_latest)
		
		# update message selection
		msg_list    = [email_dict[x] for x in email_range]
		msg_list    = sum(msg_list, [])

	return(email_earliest, email_latest, email_diff, email_range)

# get_email
#---------------------------------------------#
def get_email(service, user, email_range, output_dir,current_date, user_address, timezone_utc_offset):

	# define globals
	global global_var
	global error_count
	global excluded_count
	global error_list

	global own_address
	global store_dir
	global timezone_offset

	error_count     = 0
	error_list      = []
	excluded_count  = 0
	own_address     = user_address
	store_dir       = output_dir
	timezone_offset = timezone_utc_offset

	# initialize (log file)
	old_stdout   = sys.stdout
	log_filename = os.path.normpath(os.path.join(output_dir, "dev", "email_log.log"))
	log_file     = open(log_filename,"w")
	sys.stdout   = log_file

	# load overview file
	email_dict_file = os.path.normpath(os.path.join(output_dir, "other", 'overview_'+ datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))
	with open(email_dict_file) as file:
		email_dict     = pickle.load(file)

	# load error file (if it exists)
	email_error_file = os.path.normpath(os.path.join(output_dir, "other", 'error_'+ datetime.datetime.strptime(current_date,'%m/%d/%Y').strftime("%m_%d_%Y") + '.p'))
	if (os.path.exists(email_error_file)): 
		
		with open(email_error_file, "rb") as file:
			email_error_dict   = pickle.load(file)

		error_list = list(email_error_dict)


	# subset to relevant emails
	msg_list = [email_dict[x] for x in email_range]
	msg_list = sum(msg_list, [])
	print('Found ' + str(len(msg_list)) + ' emails')

	# subset to non-error emails
	msg_list   = [x for x in msg_list if x not in error_list]
	print('Found ' + str(len(msg_list)) + ' emails (Non Error)')

	# subset to emails not previously downloaded
	msg_list_saved = np.concatenate((glob.glob(os.path.join(output_dir,'inbox', 'email*.p')), 
		glob.glob(os.path.join(output_dir,'outbox', 'email*.p'))))
	msg_list_saved = [re.sub("(.*email_)([^_]*)(.*)","\\2", x) for x in msg_list_saved]
	msg_list_mod   = [x for x in msg_list if x not in msg_list_saved]

	print('Found ' + str(len(msg_list_mod)) + ' emails (New)')
	global_var['status_email_max']  = len(msg_list)
	global_var['status_email_load'] = len([x for x in msg_list if x in msg_list_saved])

	if len(msg_list_mod)>0:
		
		for i in range(0,len(msg_list_mod)):
			print(msg_list_mod[i])
	
		for i in range(0,int(np.ceil(len(msg_list_mod)/25))+1):
			
			start = np.minimum(i*25, len(msg_list_mod))
			end   = np.minimum(start+25, len(msg_list_mod))
	
			if end>start:
				
				msg_list_temp=msg_list_mod[start:end]
	
				print("# Batch: " + str(i) + " (Number of Emails: " + str(len(msg_list_temp)) + ")")
	
				# Batch process emails
				batch = service.new_batch_http_request()
				for msg_id in msg_list_temp:
					print(msg_id)
					batch.add(service.users().messages().get(userId=user, id=msg_id, format="raw", metadataHeaders =["In-Reply-To","References","Message-ID","Subject"]), callback=process_email)
				batch.execute()

		time.sleep(3)	
			
	else:

		time.sleep(7)

	# Save error file
	error_list = np.array(error_list)

	with open(email_error_file, "wb") as file:
		pickle.dump(error_list, file)

	# Reset log file
	sys.stdout = old_stdout
	log_file.close()

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
