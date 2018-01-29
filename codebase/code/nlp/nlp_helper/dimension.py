## Module    > dimension 
## Functions > email_to_link

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
# from * import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import numpy as np
import pandas as pd
import re 

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# email_to_link
#---------------------------------------------#
def email_to_link(msg_obj, msg_data, user_address):
	
	# print("Launching - email_to_link")

	"""
		
	"""

	# initialize
	# -----------------------
	
	link_contact     =  msg_obj.contact['msg_contact']
	link_id          =  msg_obj.link_id
	
	link_type      	 = []
	link_response_id = []
	link_response    = []
	link_reply_id    = []
	link_reply       = []

	# classify links
	# -----------------------
	for i in link_contact:
	
		link_type_tmp = np.nan

		if msg_obj.inbox_outbox=='inbox': 
	
			if user_address in msg_obj.contact['msg_to']['address']:
				link_type_tmp = 'from > you'
			elif pd.isnull(link_type_tmp) and user_address in msg_obj.contact['msg_cc']['address']:
				link_type_tmp = 'from > you (cc)'
			elif pd.isnull(link_type_tmp) and user_address in msg_obj.contact['msg_bcc']['address']:
				link_type_tmp = 'from > you (bcc)'
		
		elif msg_obj.inbox_outbox=='outbox': 
	
			if i in msg_obj.contact['msg_to']['address']:
				link_type_tmp = 'you > to'
			elif pd.isnull(link_type_tmp) and i in msg_obj.contact['msg_cc']['address']:
				link_type_tmp = 'you > to (cc)'
			elif pd.isnull(link_type_tmp) and i in msg_obj.contact['msg_bcc']['address']:
				link_type_tmp = 'you > to (bcc)'

		link_type.append(link_type_tmp)

	# response analysis
	# -----------------------
	if len(msg_obj.msg_response_id)>0:

		for i in link_contact:

			link_response_tmp = []

			for x in msg_obj.msg_response_id:

				msg_response_contact     = msg_data[x].contact['msg_contact']

				if i in msg_response_contact:
					
					link_response_tmp.append(x)
				
			link_response.append(int(len(link_response_tmp)>0))
			link_response_id.append(link_response_tmp)

	else:

		link_response    = global_fun.fill_array(len(link_contact),0)
		link_response_id = global_fun.fill_array(len(link_contact),[])

	# reply analysis
	# -----------------------
	if len(msg_obj.msg_reply_id)>0 and msg_obj.msg_reply_id!='nan':

		for i in link_contact:

			link_reply_tmp = []

			for x in [msg_obj.msg_reply_id]:

				msg_reply_contact     = msg_data[x].contact['msg_contact']

				if i in msg_reply_contact:
					
					link_reply_tmp.append(x)
				
			link_reply.append(int(len(link_reply_tmp)>0))
			link_reply_id.append(link_reply_tmp)

	else:

		link_reply    = global_fun.fill_array(len(link_contact),0)
		link_reply_id = global_fun.fill_array(len(link_contact),[])
	

	# generate list
	# -----------------------
	link_list = []

	for i in range(0,len(link_contact)):

		link_list_tmp = dict(msg_id=msg_obj.msg_id, link_id=link_id[i],link_contact=link_contact[i],link_type=link_type[i], link_response=link_response[i], link_response_id=link_response_id[i], link_reply=link_reply[i], link_reply_id=link_reply_id[i])
		link_list.append(link_list_tmp)
	
	# return
	# print("Successfully Completed - email_to_link")
	return(link_list)



#---------------------------------------------#

         
	


