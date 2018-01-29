## Module    > contact 
## Functions > contact_list, contact_labeller


# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
# from .... import *

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

# contact_list
#---------------------------------------------#

def contact_list(msg_data):
	
	# print("Launching - contact_list")

	"""
		
	"""

	## initialize
	inbox_outbox				= np.array([msg_data[x].inbox_outbox for x in msg_data.keys()])
	msg_contact_to              = np.array([msg_data[x].contact['msg_to']['address'] for x in msg_data.keys()])
	msg_contact_from            = np.array([msg_data[x].contact['msg_from']['address'] for x in msg_data.keys()])
	msg_contact_cc              = np.array([msg_data[x].contact['msg_cc']['address'] for x in msg_data.keys()])
	msg_contact_bcc             = np.array([msg_data[x].contact['msg_bcc']['address'] for x in msg_data.keys()])
	msg_contact_to_name         = np.array([msg_data[x].contact['msg_to']['name'] for x in msg_data.keys()])
	msg_contact_from_name       = np.array([msg_data[x].contact['msg_from']['name'] for x in msg_data.keys()])
	msg_contact_cc_name         = np.array([msg_data[x].contact['msg_cc']['name'] for x in msg_data.keys()])
	msg_contact_bcc_name        = np.array([msg_data[x].contact['msg_bcc']['name'] for x in msg_data.keys()])
	
	## inbox contacts -- from
	if (len(msg_contact_from[inbox_outbox=="inbox"])>0):
		inbox_contact_from          = np.concatenate(msg_contact_from[inbox_outbox=="inbox"])
		inbox_contact               = np.concatenate([inbox_contact_from])

		inbox_contact_from_name     = np.concatenate(msg_contact_from_name[inbox_outbox=="inbox"])
		inbox_contact_name          = np.concatenate([inbox_contact_from_name])
 
		inbox_contact_name_df       = pd.DataFrame({"contact":inbox_contact,"contact_name":inbox_contact_name})
		inbox_contact_name_df       = inbox_contact_name_df.drop_duplicates("contact", inplace=False)
		inbox_contact_name_df       = inbox_contact_name_df.reset_index(drop=True, inplace=False)
	 
		inbox_contact               = global_fun.freq_tabulate(inbox_contact, ['freq_inbox','contact'])

	else:
		
		inbox_contact  				= pdf.DataFrame({"freq_inbox":np.nan, 'contact':['']})
		inbox_contact_name_df 		= pd.DataFrame({"contact":[''], 'contact_name':['']})

	## outbox contacts -- to, cc, bcc
	if (len(msg_contact_to[inbox_outbox=="outbox"])>0):

		outbox_contact_to          = np.concatenate(msg_contact_to[inbox_outbox=="outbox"])
		outbox_contact_cc          = np.concatenate(msg_contact_cc[inbox_outbox=="outbox"])
		outbox_contact_bcc         = np.concatenate(msg_contact_bcc[inbox_outbox=="outbox"])
		outbox_contact             = np.concatenate([outbox_contact_to, outbox_contact_cc, outbox_contact_bcc])

		outbox_contact_to_name     = np.concatenate(msg_contact_to_name[inbox_outbox=="outbox"])
		outbox_contact_cc_name     = np.concatenate(msg_contact_cc_name[inbox_outbox=="outbox"])
		outbox_contact_bcc_name    = np.concatenate(msg_contact_bcc_name[inbox_outbox=="outbox"])
		outbox_contact_name        = np.concatenate([outbox_contact_to_name, outbox_contact_cc_name, outbox_contact_bcc_name])
 
		outbox_contact_name_df     = pd.DataFrame({"contact":outbox_contact,"contact_name":outbox_contact_name})
		outbox_contact_name_df     = outbox_contact_name_df.drop_duplicates("contact", inplace=False)
		outbox_contact_name_df     = outbox_contact_name_df.reset_index(drop=True, inplace=False)

		outbox_contact             = global_fun.freq_tabulate(outbox_contact, ['freq_outbox','contact'])
	
	else:
		
		outbox_contact         = pd.DataFrame({"freq_outbox":np.nan, 'contact':['']})
		outbox_contact_name_df = pd.DataFrame({"contact":[''], 'contact_name':['']})


	## combine > aggregate contact
	agg_contact_df             = pd.merge(outbox_contact, inbox_contact, on='contact', how='outer')
	agg_contact_df             = agg_contact_df.loc[(~np.isnan(agg_contact_df['freq_outbox']) )| (~np.isnan(agg_contact_df['freq_inbox']) )]
	agg_contact_df             = agg_contact_df.fillna(value=0)
	agg_contact_df['freq_agg'] = agg_contact_df['freq_inbox'] + agg_contact_df['freq_outbox']
	agg_contact_df             = global_fun.df_sort(agg_contact_df, ['freq_agg'], [True])

	agg_contact_df_name        = pd.concat([inbox_contact_name_df, outbox_contact_name_df], ignore_index=True)
	agg_contact_df_name        = agg_contact_df_name.drop_duplicates("contact", inplace=False)
	agg_contact_df_name        = agg_contact_df_name.reset_index(drop=True, inplace=False)

	## merge in the names
	agg_contact_df             = pd.merge(agg_contact_df, agg_contact_df_name, on='contact', how='inner')
	
	# return
	# print("Successfully Completed - contact_list")
	return(agg_contact_df)


# contact_labeller
#---------------------------------------------#

def contact_labeller(contact_xwalk_contact, contact_xwalk_label, contact_link, msg_id, msg_threadid):
	
	# print("Launching - contact_labeller")

	"""
		
	"""

	# initialize
	contact_df_temp = pd.DataFrame({"contact":contact_link, "msg_id":msg_id, "msg_threadid":msg_threadid})
	contact_df_temp['id_tmp'] 				   = range(0, len(contact_df_temp))
	contact_df_temp['contact_label']           = 'no_label'

	xwalk_df_temp = pd.DataFrame({"contact":contact_xwalk_contact,"label":contact_xwalk_label})

	# loop over labels
	label_unique = xwalk_df_temp['label'].unique()
	
	for label in label_unique:

		label_contact = xwalk_df_temp.loc[(xwalk_df_temp['label']==label) & (pd.notnull(xwalk_df_temp['contact'])),'contact']
		label_contact = [re.sub("\|", "", str(x)) for x in label_contact]
		
		contact_df_temp.loc[(contact_df_temp['contact'].apply(lambda x: x in label_contact)) & ~(contact_df_temp['contact_label']=="no_label"), 'contact_label'] = "error"
		contact_df_temp.loc[(contact_df_temp['contact'].apply(lambda x: x in label_contact)) & (contact_df_temp['contact_label']=="no_label"), 'contact_label'] = label

	# contact label aggregation
	contact_label_msg    = contact_df_temp.groupby('msg_id').apply(lambda x: '|'.join(x['contact_label'].unique()))
	contact_label_msg    = pd.DataFrame({'msg_id':contact_label_msg.index, 'contact_label_msg':contact_label_msg})
	contact_df_temp      = pd.merge(contact_label_msg, contact_df_temp, on='msg_id', how='outer')

	contact_label_thread = contact_df_temp.groupby('msg_threadid').apply(lambda x: '|'.join(x['contact_label'].unique()))
	contact_label_thread = pd.DataFrame({'msg_threadid':contact_label_thread.index, 'contact_label_thread':contact_label_thread})
	contact_df_temp      = pd.merge(contact_label_thread, contact_df_temp, on='msg_threadid', how='outer')

	contact_df_temp      = contact_df_temp.sort_values(by=['id_tmp'], ascending=[True])

	# return
	# print("Successfully Completed - contact_labeller")
	return(np.array(contact_df_temp['contact_label']), np.array(contact_df_temp['contact_label_msg']),np.array(contact_df_temp['contact_label_thread']))




#---------------------------------------------#

         
	


