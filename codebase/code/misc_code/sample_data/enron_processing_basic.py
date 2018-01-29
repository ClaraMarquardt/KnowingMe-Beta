#----------------------------------------------------------------------------#

# Purpose:     KnowingMeTester Application - Generate sample data set based on Enron Data
# Date:        August 2017
# Language:    Python (.py) [Python 2.7]

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# NOTE

# Source of original data: 
# https://www.kaggle.com/wcukierski/enron-email-dataset#

# cd [directory of choice]
# mkdir enron
# cd enron
# wget https://www.kaggle.com/wcukierski/enron-email-dataset/downloads/enron-email-dataset.zip
# unzip enron-email-dataset.zip

#----------------------------------------------------------------------------#
#                                SetUp                                       #
#----------------------------------------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
print(app_root)

# Dependencies - External
#---------------------------------------------#
sys.path.append(os.path.normpath(os.path.join(app_root)))
from __init__ import *

# Control Parameters [USER SETTINGS]
#---------------------------------------------#

## Raw data path - folder where the raw data is stored
raw_data_path = "~/Desktop/enron"
raw_data_file = "emails.csv"

## Output path  - where the data is stored
output_dir = os.path.normpath(os.path.join(app_root, "output", "sample"))

## Person of interest
person = "lay-k"
person_email = ["kenneth@enron.com", "kenneth.lay@enron.com", "lay.kenneth@enron.com"]

## Emails (Inbox / Outbox)
email_count_max = 10000

#----------------------------------------------------------------------------#
#                              Processing                                    #
#----------------------------------------------------------------------------#


# Load & Subset 
#---------------------------------------------#

# load
enron_data_path = os.path.normpath(os.path.join(raw_data_path, raw_data_file))
enron_data = pd.read_csv(enron_data_path)

# subset 
# enron_data_subset = enron_data[enron_data['file'].str.contains(person)]
# enron_data_subset_inbox = enron_data_subset[enron_data_subset['file'].str.contains("/inbox/")]
# enron_data_subset_outbox = enron_data_subset[~enron_data_subset['file'].str.contains("sent")]

# sample - basic
# enron_data_subset_inbox = enron_data_subset_inbox.iloc[0:min(1000, len(enron_data_subset_inbox))]
# enron_data_subset_outbox = enron_data_subset_outbox.iloc[0:min(1000, len(enron_data_subset_inbox))]

# combine
# enron_data_subset = enron_data_subset_outbox.append(enron_data_subset_inbox)

enron_data_subset       = enron_data
enron_data_subset_index = range(0, len(enron_data))
enron_data_subset       = enron_data_subset.iloc[enron_data_subset_index[::-1]]

# Parse - Basic 
#---------------------------------------------#

## initialise
email_count=0
subject_id=0
i=0
subject_dict={}


## loop - extract email meta data & text
while email_count <= email_count_max and i < len(enron_data_subset):

	try: 
		# parse email
		email_raw = enron_data_subset.iloc[i,1]
		email_parsed = Parser().parsestr(email_raw)

		# count
		i = i+1

		print(email_parsed['to'])
		print(email_parsed['from'])

		# subset - to / from
		if (pd.notnull(email_parsed['to']) & pd.notnull(email_parsed['from'])):

			if any(email in email_parsed['to'] for email in person_email) or any(email in email_parsed['from'] for email in person_email):

				print("Relevant")

				# extract meta data
				# -----------
		
				## initialize
				msg_meta = {}
			
				## id 
				msg_meta['msg_id']       = email_parsed['Message-ID']
				msg_meta['msg_id']       = re.sub("<|>","", msg_meta['msg_id'])
				msg_meta['msg_id']       = re.sub("(.*)(\\.JavaMail.*)","\\1", msg_meta['msg_id'])

				msg_meta['msg_threadid'] = "/"                  # IMPUTE BASED ON SUBJECT
		
				## snippet
				msg_meta['msg_snippet'] = "/"                    # IMPUTE BASED ON TEXT
		
				## date
				msg_meta['msg_date']    = email_parsed['Date']
		
				## sender/recipient
				msg_meta['msg_from']    = email_parsed["from"]
				msg_meta['msg_to']      = email_parsed["to"]
				msg_meta['msg_cc']      = email_parsed["X-cc"]
				msg_meta['msg_bcc']     = email_parsed["X-bcc"]

				if len(msg_meta['msg_cc'])==0:
					msg_meta['msg_cc']=None
				if len(msg_meta['msg_bcc'])==0:
					msg_meta['msg_bcc']=None

				## subject
				msg_meta['msg_subject'] = email_parsed["subject"]
				msg_meta['msg_subject'] = re.sub("RE: ","",msg_meta['msg_subject'])

				## meta labels
				
				### inbox/outbox - based on sender address
				if any(email in email_parsed['from'] for email in person_email):
					msg_meta['msg_inbox_outbox'] = "outbox"
					msg_meta['msg_label']        = ["SENT"]

				else:
					msg_meta['msg_inbox_outbox'] = "inbox"
					msg_meta['msg_label']        = ["INBOX"]
		
				## msg thread id

				if msg_meta['msg_subject'] in subject_dict.keys():
					msg_meta['msg_threadid']  = subject_dict[msg_meta['msg_subject']]
				else:
					msg_meta['msg_threadid']  = subject_id
					subject_dict[msg_meta['msg_subject']] = subject_id
					subject_id = subject_id + 1

				print(msg_meta['msg_from'])
				print(msg_meta['msg_label'])
				print(msg_meta['msg_inbox_outbox'])	

		
				# extract text
				# -----------
			
				## get_msg_text - helper function
				def get_msg_text(msg):
		
					messageMainType = msg.get_content_maintype()
					if messageMainType == 'multipart':
						for part in msg.get_payload():
							if part.get_content_maintype() == 'text':
								return part.get_payload()
						return ''
					elif messageMainType == 'text':
						return msg.get_payload()

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
					msg_text_clean = re.sub("([\n]*[\r]*[\n]*)*$", "", msg_text_clean)
					msg_text_clean = re.sub("^([\n]*[\r]*[\n]*)*", "", msg_text_clean)

					# basic	- special characters
					msg_text_clean = re.sub("&#39;|&quot;|&lt;|&gt;"," ",msg_text_clean)

					# basic - spaces
					msg_text_clean = msg_text_clean.replace("[ ]{2,}", "")
					msg_text_clean = re.sub("^[ ]|[ ]$","",msg_text_clean)

					# basic
					msg_text = msg_text
			
					msg_text = re.sub("[ ]{2,}"," ",msg_text)
					msg_text = re.sub("^[ ]|[ ]$","",msg_text)
					msg_text = re.sub("&#39;|&quot;|&lt;|&gt;"," ",msg_text)

					return(msg_text_clean)

				## execute 
				email_text = get_msg_text(email_parsed)
				print(email_text)
				print(len(email_text))
				print(i)
				
				# basic cleaning 

				if (len(email_text)>0) & (len(email_text)<1100):

					print("process")

					# clean
					email_text = clean_msg_text(email_text)

					# store
					msg_meta['msg_text'] = email_text
					msg_meta['msg_snippet'] = email_text[:200]

					# save
					# -----------
					if msg_meta['msg_inbox_outbox'] == 'inbox':
						email_filename=os.path.normpath(os.path.join(output_dir, "inbox", 'email_' + msg_meta['msg_id'] + '_' + msg_meta['msg_inbox_outbox'] + '.json'))
					else:
						email_filename=os.path.normpath(os.path.join(output_dir, "outbox", 'email_' + msg_meta['msg_id'] + '_' + msg_meta['msg_inbox_outbox'] + '.json'))
			
					with open(email_filename, 'w') as out_file:
						json.dump(msg_meta, out_file, indent=4)

					# count
					email_count = email_count + 1
		
					print("Relevant email count: " + str(email_count))
				
				else:
					print("No Text / Too long")

			else: 
				
				print("Irrelevant")

	except Exception as e: 

		# error message
		print("Error Encountered")
		print(e)


## NOTE - subsequent subsetting
## -------------------------
### Focus on messages with 'responsiveness..response'==1
### Focus on messages with ''msg_date_year'>=2000




#----------------------------------------------------------------------------#
#                                 End                                        #
#----------------------------------------------------------------------------#

