## Module    > dataprep
## Functions > prepare_browser_vis

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..","..")) 


sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import pandas as pd
import numpy as np
import re

# Function Definition
#---------------------------------------------#

# prepare_browser_vis
#---------------#

def prepare_browser_vis(feat_df,feat_df_dict, email_array, internal_email_id, link_id_store, reload):

	# subset feature dt
	email_id            = re.sub("(.*email_)([^_]*)(_.*p$)","\\2",email_array[internal_email_id])
	email_feat_df       = feat_df[feat_df['msg_id']==email_id]

	# meta    - df
	col = feat_df_dict['id_col'] + feat_df_dict['date_col'] + feat_df_dict['contact_col'] + feat_df_dict['text_rel_col'] + feat_df_dict['label_col']
	col = [x for x in col if x in email_feat_df.columns]
	email_meta_df     = email_feat_df[np.array(col)]

	# text    - df
	col = ['link_id'] + feat_df_dict['text_col'] 
	col = [x for x in col if x in email_feat_df.columns]
	email_text_df   = email_feat_df[np.array(col)]
	
	# text _decom   - df
	col = ['link_id'] + feat_df_dict['text_extra_col'] 
	col = [x for x in col if x in email_feat_df.columns]
	email_decom_text_df   = email_feat_df[np.array(col)]

	# insight - df
	col = ['link_id'] + feat_df_dict['flag_col'] + feat_df_dict['group_col'] + feat_df_dict['insight_col'] + feat_df_dict['insight_interm_col']
	col = sorted(col)
	col = [x for x in col if x in email_feat_df.columns]
	email_insight_df = email_feat_df[np.array(col)]

	# link - df
	link_df = pd.DataFrame({'link_id':np.array(email_feat_df['link_id']),
		'link_contact':np.array(email_feat_df['link_contact']), 
		'link_type':np.array(email_feat_df['link_type'])})
	link_df['link_desc'] = link_df['link_contact'] + " | " + link_df['link_type']
	link_df.reset_index(drop=True, inplace=True)
	
	if reload==False:

		if link_id_store=='-1':
			link_id = str(np.array(link_df['link_id'][0]))
		else:
			link_id = str(link_id_store)

	else:
		
		link_id       = str(np.array(link_df['link_id'][0]))
		link_id_store = '-1'

	# subset to 1st link & format
	email_meta_df_link    	 = email_meta_df[email_meta_df['link_id']==link_id].drop('link_id', axis=1)
	email_meta_df_link    	 = global_fun.pd_htmlformat(email_meta_df_link)

	email_insight_df_link 	 = email_insight_df[email_insight_df['link_id']==link_id].drop('link_id', axis=1)
	email_insight_df_link 	 = global_fun.pd_htmlformat(email_insight_df_link).replace('<tbody', '<tbody id="fbody"')

	email_decom_text_df_link = email_decom_text_df[email_decom_text_df['link_id']==link_id].drop('link_id', axis=1)
	email_decom_text_df_link = global_fun.pd_htmlformat(email_decom_text_df_link)

	email_text_df_link    = email_text_df[email_text_df['link_id']==link_id][feat_df_dict['text_col']]
	email_text_df_link.reset_index(drop=True, inplace=True)
	if len(email_text_df_link) > 0:
		email_text_df_link    = str(email_text_df_link['text'][0])
	else:
		email_text_df_link    = str('')
	
	email_decom_text_df_link    = email_decom_text_df[email_decom_text_df['link_id']==link_id]['misc*msg_sentence']
	email_decom_text_df_link.reset_index(drop=True, inplace=True)
	
	if len(email_decom_text_df_link) > 0:
		if pd.notnull(email_decom_text_df_link[0]):
			email_decom_text_df_link    = str(email_decom_text_df_link[0].encode('utf-8','ignore'))
			
	return(email_meta_df_link,email_insight_df_link,email_text_df_link,email_decom_text_df_link,link_df,link_id_store)

#---------------------------------------------#


