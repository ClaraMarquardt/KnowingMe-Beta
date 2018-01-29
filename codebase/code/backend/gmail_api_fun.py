
#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Main Backend / Gmail API Interface Script
# Date:        August 2017
# Language:    Python (.py) [ Python 2.7 ]

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  

# Dependencies - External
#---------------------------------------------#
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init__ import *
from __init_var__ import *

#----------------------------------------------------------------------------#
#			                     Functions                                   #
#----------------------------------------------------------------------------#

## get_email_batch
#---------------------------------------------#
def get_email_batch(service, user_id, earliest_date, latest_date, output_dir, excl_non_personal_email,excl_archived_email, extract_email_lim, mode="data"):
	
	"""Download, format and save all of emails that meet fall within a certain date range.

	Returns:
		/ (Emails are saved as Json files).
	"""

	## initialise log file
	## --------------------------
	old_stdout = sys.stdout
	log_filename = os.path.normpath(os.path.join(output_dir, "email_log.log"))
	log_file = open(log_filename,"w")
	sys.stdout = log_file
	

	## initialise
	## --------------------------
	start_time = datetime.datetime.now()

	global error_count
	global excluded_count
	global global_var

	global_var['status_email_max'] = 100
	global_var['status_email_max_new'] = 100
	global_var['status_email_load'] = 0
	global_var['status_email_overview_max']=365
	global_var['status_email_overview_load']=0

	error_count=0
	excluded_count=0

	## helper functions
	## --------------------------

	## get_email_list
	def get_email_list(service, user_id, filter, max_result_page=200):
	
		"""Obtain list of emails (IDs) that meet a specified set of criteria.
	
		Returns:
			email_list, the list of email IDs.
		"""
	
		email_list = []
		email_list_raw = service.users().messages().list(userId=user_id, q=filter,
			maxResults=max_result_page, includeSpamTrash=False).execute()
		
		if 'messages' in email_list_raw:
			email_list.extend(email_list_raw['messages'])
	
		while 'nextPageToken' in email_list_raw:
			page_token = email_list_raw['nextPageToken']
			email_list_raw = service.users().messages().list(userId=user_id,  q=filter, 
				maxResults=max_result_page, includeSpamTrash=False, pageToken=page_token).execute()
			email_list.extend(email_list_raw['messages'])
	
		return email_list

	## get_msg_text
	def get_msg_text(msg):
	
		"""Parse a MIME message to obtain the email text (recursive).
	
		Returns:
			email_text, the extracted email text.
		"""
	
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
	
		# print(msg_text[1:300])
		return msg_text
		
	## get_msg_meta
	def get_msg_meta(msg):
	
		"""Parse a MIME message to obtain the email meta data.
	
		Returns:
			email_meta, the extracted email meta data.
		"""
	

		global error_count
		global excluded_count

		## format
		msg_str  = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)

		## initialize
		msg_meta = {}
	
		## id (GMAIL)
		msg_meta['msg_id']       = msg['id']
		msg_meta['msg_threadid'] = msg['threadId']
	
		## response to
		msg_meta['msg_id_mime']          = mime_msg['Message-ID']
		if 'In-Reply-To' in mime_msg.keys():
			msg_meta['msg_reply_to_id_mime'] = mime_msg['In-Reply-To']
		else:
			msg_meta['msg_reply_to_id_mime'] = np.nan

		## labels (GMAIL)
		msg_meta['msg_label'] = msg['labelIds']
	
		## snippet (GMAIL)
		msg_meta['msg_snippet'] = msg['snippet']
	
		## date (MAIL)
		msg_meta['msg_date'] = mime_msg['date']
	
		## sender/recipient (MAIL)
		msg_meta['msg_from'] = mime_msg["from"]
		msg_meta['msg_to']   = mime_msg["to"]
		msg_meta['msg_cc']   = mime_msg["cc"]
		msg_meta['msg_bcc']  = mime_msg["bcc"]
	
		## subject (MAIL)
		msg_meta['msg_subject'] = mime_msg["subject"]
	
		## meta labels
		
		### inbox/outbox - based on sender address
		own_address = service.users().getProfile(userId='me').execute()['emailAddress']
		
		if own_address in msg_meta['msg_from']:
			msg_meta['msg_inbox_outbox'] = "outbox"
		else:
			msg_meta['msg_inbox_outbox'] = "inbox"
	
		print("## " + msg_meta['msg_id'])		
		print(msg_meta['msg_from'])
		print(msg_meta['msg_label'])
		print(msg_meta['msg_inbox_outbox'])	
	
		return(msg_meta)
	
	def clean_msg_text(msg_text):
		
		"""Clean email text extracted from a MIME message.
	
		Returns:
			msg_text_clean, the cleaned email text.
		"""

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
		msg_text_clean = re.sub("([\n]*[\r]*[\n]*)*$", "", msg_text_clean)
		msg_text_clean = re.sub("^([\n]*[\r]*[\n]*)*", "", msg_text_clean)

		# basic	- special characters
		msg_text_clean = re.sub("&#39;|&quot;|&lt;|&gt;"," ",msg_text_clean)

		# basic - spaces
		msg_text_clean = msg_text_clean.replace("[ ]{2,}", "")
		msg_text_clean = re.sub("^[ ]|[ ]$","",msg_text_clean)

		return(msg_text_clean)
	
	## process_email
	def process_email(request_id, response, exception):
	
		"""Parse a MIME message - obtain and save the email text and meta data.
	
		Returns:
			\ (Email data is saved).
		"""
	
		global error_count
		global excluded_count
		global msg_id_temp
		global global_var
		
		global_var['status_email_load']=global_var['status_email_load']+1

		print("---------------------------")
		
		try: 
			
			# Obtain the email meta-data
			email_meta = get_msg_meta(response)

			## Obtain the email-text
			email_text = get_msg_text(response)

			# if not any(label in email_meta['msg_label'] for label in exclude_label) and (not any(label in email_meta['msg_label'] for label in exclude_label_non_personal) or excl_non_personal_email=='False') and len(email_text)>0 and "<style>" not in email_text and not any(text in email_text for text in exclude_text_non_personal) and ((excl_archived_email=='True' and any(label in email_meta['msg_label'] for label in include_label)) or (excl_archived_email=='False')):
		
			## Combine the meta data & text
			email_data = email_meta
			email_data['msg_text'] = clean_msg_text(email_text)
			
			## Save the email
			if email_data['msg_inbox_outbox'] == 'inbox':
				email_filename=os.path.normpath(os.path.join(output_dir, "inbox", 'email_' + email_data['msg_id'] + '_' + email_data['msg_inbox_outbox'] + '_' + parser.parse(email_data['msg_date']).strftime('%m_%d_%Y') + '.json'))
			else:
				email_filename=os.path.normpath(os.path.join(output_dir, "outbox", 'email_' + email_data['msg_id'] + '_' + email_data['msg_inbox_outbox'] + '_' + parser.parse(email_data['msg_date']).strftime('%m_%d_%Y') + '.json'))
			
			with open(email_filename, 'w') as out_file:
				print("save")
				json.dump(email_data, out_file, indent=4)


			print("---------------------------")

		except Exception as e: 

			print("Error Encountered")
			print(e)

			error_count = error_count + 1
			
	
	## process_date
	def process_date(request_id, response, exception):
	
		"""Parse a MIME message - obtain dates > append to list.
	
		Returns:
			\ (List of dates).
		"""
		
		global birthday_date_list
	
		## format
		msg_str  = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)

		mime_msg_date = mime_msg['date']

		birthday_date_list.append(mime_msg_date)

	## process_date
	def process_date_year(request_id, response, exception):
	
		"""Parse a MIME message - obtain dates > append to list.
	
		Returns:
			\ (List of dates).
		"""
		
		global year_date_list
		global global_var

		## format
		msg_str  = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)

		mime_msg_date = mime_msg['date']

		year_date_list.append(mime_msg_date)
		


	## main function
	## --------------------------
	if mode=="data":
		
		## Generate filter request (date based) (note - possible labels INBOX / SENT)
		latest_date_mod = datetime.datetime.strptime(latest_date,'%m/%d/%Y')+datetime.timedelta(days=1)
		date_filter = "before: {0} after: {1}".format(latest_date_mod.strftime('%Y/%m/%d'),
					   datetime.datetime.strptime(earliest_date,'%m/%d/%Y').strftime('%Y/%m/%d'))
		print('Requesting emails (ALL (excluding Spam/Trash)) - Start: ' + earliest_date + ' End: ' + latest_date)

		exclude_text = ["opt-out", "viewing the newsletter", "edit your preferences", "update profile", "smartunsuscribe","secureunsuscribe","group-digests","yahoogroups"]
		text_filter = " ".join(["AND NOT: \""+a+"\"" for a in exclude_text])
		q = "(label:sent " + date_filter + ") OR (label:inbox category:personal " + date_filter + " " + text_filter + ")"
		
		## Obtain a list of emails 
		msg_list = get_email_list(service, user_id, q)
		msg_list =[msg['id'] for msg in msg_list]

		## Subset
		lim = np.min([len(msg_list),int(extract_email_lim)])
		msg_list=msg_list[0:lim]
		
		print('Found ' + str(len(msg_list)) + ' emails (All)')


		msg_list_saved = np.concatenate((glob.glob(os.path.join(output_dir,'inbox', 'email*.json')), 
			glob.glob(os.path.join(output_dir,'outbox', 'email*.json'))))
		msg_list_saved = [re.sub("(.*email_)([^_]*)(.*)","\\2", x) for x in msg_list_saved]

		msg_list_mod = [x for x in msg_list if x not in msg_list_saved]

		print('Found ' + str(len(msg_list_mod)) + ' emails (New)')

		global_var['status_email_max']=len(msg_list)
		global_var['status_email_max_new']=len(msg_list_mod)

		if len(msg_list_mod)>0:
			for i in range(0,len(msg_list_mod)):
				print(msg_list_mod[i])
		
			for i in range(0,int(np.ceil(len(msg_list_mod)/25))+1):
				
				start = np.minimum(i*25, len(msg_list_mod))
				end   = np.minimum(start+25, len(msg_list_mod))
		
				if end>start:
					msg_list_temp=msg_list_mod[start:end]
		
					print("# Batch: " + str(i) + " (Number of Emails: " + str(len(msg_list_temp)) + ")")
		
					## Batch process emails - Inbox
					batch = service.new_batch_http_request()
					for msg_id in msg_list_temp:
						print(msg_id)
						batch.add(service.users().messages().get(userId=user_id, id=msg_id, format="raw", metadataHeaders =["In-Reply-To","References","Message-ID","Subject"]), callback=process_email)
					batch.execute()
		


		## other function (birthday, etc.)
		## --------------------------

		birthday_query = [('in:inbox +{"happy birthday OR bday"} -{belated OR late} newer_than:6y')]
		
		global birthday_date_list 
		birthday_date_list = ["birthday"]

		## Obtain a list of emails 
		msg_list_birthday = get_email_list(service, user_id, birthday_query)
		msg_list_birthday =[msg['id'] for msg in msg_list_birthday]

		## 
		if len(msg_list_birthday)>0:
			for i in range(0,len(msg_list_birthday)-1):
				print(msg_list_birthday[i])
		
			for i in range(0,int(np.ceil(len(msg_list_birthday)/25))+1):
				
				start = np.minimum(i*25, len(msg_list_birthday)-1)
				end   = np.minimum(start+25, len(msg_list_birthday)-1)
		
				if end>start:
					msg_list_birthday_temp=msg_list_birthday[start:end]
				else:
					msg_list_birthday_temp=msg_list_birthday[start]
		
				print("# Batch (Birthday): " + str(i) + " (Number of Emails: " + str(len(msg_list_birthday_temp)) + ")")
		
				## Batch process emails - Birthday
				batch = service.new_batch_http_request()
				for msg_id in msg_list_birthday_temp:
					print(msg_id)
					batch.add(service.users().messages().get(userId=user_id, id=msg_id, format="raw", metadataHeaders =["Date"]), callback=process_date)
				batch.execute()

			# save
			birthday_date_filename=os.path.normpath(os.path.join(output_dir, "other", 'date_birthday.json'))
			
			with open(birthday_date_filename, 'w') as out_file:
				json.dump(birthday_date_list, out_file, indent=4)

	## other function (date, etc.)
	## --------------------------

	elif mode=="count":
		current_date = datetime.datetime.now().strftime("%m_%d_%Y")
		year_date_filename=os.path.normpath(os.path.join(output_dir, "other", 'date_year_'+current_date+'.json'))

		if not os.path.exists(year_date_filename):
			global year_date_list 
			year_date_list = [current_date]

			for i in range(1,366): 

				global_var['status_email_overview_load']=global_var['status_email_overview_load']+1

				date_start = (datetime.datetime.strptime(latest_date,'%m/%d/%Y') - datetime.timedelta(days=i)).strftime("%m/%d/%Y")
				date_end   = (datetime.datetime.strptime(latest_date,'%m/%d/%Y') - datetime.timedelta(days=i-1)).strftime("%m/%d/%Y")
				date_filter = "before: {0} after: {1}".format(datetime.datetime.strptime(date_end,'%m/%d/%Y').strftime('%Y/%m/%d'),
						   datetime.datetime.strptime(date_start,'%m/%d/%Y').strftime('%Y/%m/%d'))
				print('Requesting emails (ALL (excluding Spam/Trash)) - Start: ' + earliest_date + ' End: ' + latest_date)

				exclude_text = ["opt-out", "viewing the newsletter", "edit your preferences", "update profile", "smartunsuscribe","secureunsuscribe","group-digests","yahoogroups"]
				text_filter = " ".join(["AND NOT: \""+a+"\"" for a in exclude_text])
				q = "(label:sent " + date_filter + ") OR (label:inbox category:personal " + date_filter + " " + text_filter + ")"
			

				## Obtain a list of emails 
				msg_list_year = get_email_list(service, user_id, q)
				msg_list_year =[msg['id'] for msg in msg_list_year]
			
				for j in range(0,len(msg_list_year)+1):
					year_date_list.append(date_start)

			# save
			
			with open(year_date_filename, 'w') as out_file:
				json.dump(year_date_list, out_file, indent=4)

	## Return
	end_time = datetime.datetime.now()
	run_time = end_time - start_time
	run_time = run_time.seconds
	
	data_array=[error_count,excluded_count,run_time]
	
	## close log file
	## --------------------------	

	sys.stdout = old_stdout
	log_file.close()
	

	return(data_array)

#----------------------------------------------------------------------------#
# 				                  End                                        #
#----------------------------------------------------------------------------#