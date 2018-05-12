# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_msg_class_mod
# Purpose:      Module - Define msg classification analysis functions
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
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','analysis')))
from analysis_helper import analysis_clean_mod, analysis_sentiment_mod, analysis_parse_mod, analysis_token_mod, analysis_bag_of_word_mod, analysis_polite_mod, analysis_conver_mod

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                  Class Definition                               #
#----------------------------------------------------------------------------#

# msg
#---------------------------------------------#

class msg:

	"""
	
	"""
 
	def __init__(self, msg_data, conver_data, user_address):

		## initialize
		## --------------
		msg_data 					      = msg_data.reset_index(drop=True, inplace=False)
		msg_data 						  = msg_data.iloc[0]

		## id
		## --------------
		self.msg_threadid                 = msg_data.msg_threadid
		self.msg_id                       = msg_data.msg_id

		## attributes
		## --------------
		
		# * meta
		self.label                        = msg_data.msg_label
		self.subject                  	  = analysis_clean_mod.clean_text(msg_data.msg_subject)

		# * date
		self.date                     	  = dict(msg_date=msg_data.msg_date)
		self.date['msg_date_date'], self.date['msg_date_day'],self.date['msg_date_week'],self.date['msg_date_hour'],self.date['msg_date_daypart'],self.date['msg_date_month'], self.date['msg_date_weekday'], self.date['msg_date_weekday_hour']       = analysis_clean_mod.add_date(self.date['msg_date'])

		# * flags
		self.inbox_outbox             	  = msg_data.msg_inbox_outbox

		# * contact
		self.contact                  	  = dict(msg_from=analysis_clean_mod.clean_contact(msg_data.msg_from),msg_to=analysis_clean_mod.clean_contact(msg_data.msg_to),msg_cc=analysis_clean_mod.clean_contact(msg_data.msg_cc), msg_bcc=analysis_clean_mod.clean_contact(msg_data.msg_bcc))
		
		# warnings.simplefilter(action='ignore', category=FutureWarning)
		if self.inbox_outbox=='inbox' and (user_address not in sum([self.contact['msg_to']['address'].tolist(),self.contact['msg_cc']['address'].tolist(),self.contact['msg_bcc']['address'].tolist()], [])):
			self.contact['msg_to']['address'] = np.array([user_address])
		elif self.inbox_outbox=='outbox' and (user_address not in self.contact['msg_from']['address'].tolist()):
			self.contact['msg_from']['address'] = np.array([user_address])

		if self.inbox_outbox=='inbox':
			self.contact['msg_contact']   = self.contact['msg_from']['address'].tolist()
		elif self.inbox_outbox=='outbox':
			self.contact['msg_contact']   = sum([self.contact['msg_to']['address'].tolist(), self.contact['msg_bcc']['address'].tolist(), self.contact['msg_cc']['address'].tolist()], [])

		# * conversation 

		## conversation chronological
		if self.msg_id in conver_data[self.msg_threadid].msg_id:
			self.conversation_pos  = conver_data[self.msg_threadid].msg_id.tolist().index(self.msg_id) 
		else:
			self.conversation_pos  = np.nan

		if self.conversation_pos>0:
			self.conversation_pre  = conver_data[self.msg_threadid].msg_id[self.conversation_pos-1]
		else:
			self.conversation_pre  = np.nan

		if self.conversation_pos<(len(conver_data[self.msg_threadid].msg_id)-1):
			self.conversation_post = conver_data[self.msg_threadid].msg_id[self.conversation_pos+1]
		else:
			self.conversation_post = np.nan
		
		self.conversation_first    = int(self.conversation_pos==0)
		self.conversation_last     = int(self.conversation_pos==(len(conver_data[self.msg_threadid].msg_id)-1))

		## conversation reply-based
		if np.any(pd.notnull(msg_data.msg_reply_id)):
			self.msg_reply_id              = msg_data.msg_reply_id
		else:
			self.msg_reply_id              = []

		if np.any(pd.notnull(msg_data.msg_response_id)):
			self.msg_response_id           = msg_data.msg_response_id
		else:
			self.msg_response_id           = []

		# * links
		self.link_id                       = [self.msg_id +'_'+ str(x) for x in range(0, len(self.contact['msg_contact']))]

			
# link
#---------------------------------------------#

class link:

	"""
	
	"""
 

	def __init__(self, link_data):

		## id
		## --------------
		self.msg_id                = link_data['msg_id']
		self.link_id               = link_data['link_id']

		## attributes
		## --------------
	
		self.link_contact          = link_data['link_contact']
		self.link_type             = link_data['link_type']
		
		self.link_response         = link_data['link_response']
		self.link_response_id      = link_data['link_response_id']
		self.link_response_count   = len(self.link_response_id)
		self.link_response_id_pair = [[self.msg_id, x] for x in self.link_response_id]

		self.link_reply            = link_data['link_reply']
		self.link_reply_id         = link_data['link_reply_id']
		self.link_reply_count      = len(self.link_reply_id)
		self.link_reply_id_pair    = [[self.msg_id, x] for x in self.link_reply_id]

# contact
#---------------------------------------------#

class contact:

	"""
	
	"""
 

	def __init__(self, contact, link_data, msg_data):

		## id
		## --------------
		self.contact_id            = contact

		## attributes
		## --------------
		
		# initialize
		link_id_outbox     = []
		link_id_inbox      = []

		# loop over links
		for x in link_data.keys():

			link_obj = link_data[x]

			if link_obj.link_contact==contact and msg_data[link_obj.msg_id].inbox_outbox=='outbox':
				
				link_id_outbox.append(link_obj.link_id)

			elif link_obj.link_contact==contact and msg_data[link_obj.msg_id].inbox_outbox=='inbox':

				link_id_inbox.append(link_obj.link_id)

		self.link_id_outbox = link_id_outbox
		self.link_id_inbox  = link_id_inbox
		
	
# conver
#---------------------------------------------#

class conver:

	"""
	

	"""
 
	def __init__(self,thread_data):

		## initialize
		## --------------
		thread_data                  = thread_data.sort_values(by=['msg_date'], ascending=[True])
		thread_data 		         = thread_data.reset_index(drop=True, inplace=False)

		## id
		## --------------
		self.msg_threadid            = thread_data['msg_threadid'][0]
		self.msg_id                  = np.array(thread_data['msg_id'])

		## attributes
		## --------------
		
		# * conversation 
		self.conversation            = int(len(thread_data)>1)
		self.conversation_length     = len(thread_data)
		

# text
#---------------------------------------------#

class text:

	"""
	

	"""
 
	def __init__(self, msg_text, msg_id):

		## initialize
		## --------------

		## id
		## --------------
		self.msg_id                  = msg_id

		## attributes
		## --------------

		## BASICS

		# * basic tokenization
		self.text                    = analysis_clean_mod.clean_text(msg_text)
		self.sentence                = analysis_token_mod.tokenize(self.text, "sentence")
		self.word                    = analysis_token_mod.tokenize(self.text, "word")
		self.character            	 = analysis_token_mod.tokenize(self.text, "character")

		# * other tokenizations
		self.unigram,  self.bigram   = analysis_token_mod.unigram_bigram(self.sentence)

		# * meta attributes
		self.sentence_count          = len(self.sentence)
		self.word_count              = len(self.word)
		self.character_count         = len(self.character)

		# * linguistic attributes
		self.lang, self.eng                                             = analysis_parse_mod.lang_parse(self.text)
		
		## > NOTE BELOW ONLY GENERATED FOR ENGLISH MESSAGES
		self.parse                   								    = analysis_parse_mod.dep_parse(self.sentence,  self.eng)
			
		self.pos, self.pos_dict      							        = analysis_parse_mod.pos_tag(self.sentence, self.eng)
		self.pos_count, self.pos_set,self.pos_set_agg, self.pos_indic   = analysis_bag_of_word_mod.pos_word_bag(self.pos_dict,self.eng)
		
		# * misc
		self.message_sentence        = ' ///\n\n '.join(self.sentence)

		## INSIGHT SPECIFIC 

		# * politeness 
		self.request                 = [analysis_polite_mod.request_identification(x, y, z) for (x,y, z) in zip(self.sentence, self.parse, np.tile(self.eng, len(self.sentence)))]
		self.polite                  = analysis_polite_mod.polite_score(self.sentence, self.parse, self.unigram, self.bigram, self.request)
		
		# * sentiment 
		self.sentiment_score_score_vader, self.sentiment_score_dist_vader, self.sentiment_score_score, self.sentiment_score_score_label, self.sentiment_score_dist, self.sentiment_score_dist_score, self.sentiment_score_dist_label = analysis_sentiment_mod.sentiment_score(self.sentence, self.eng)
		self.sentiment_count, self.sentiment_set,self.sentiment_set_agg, self.sentiment_indic   = analysis_bag_of_word_mod.sentiment_word_bag(self.unigram, self.bigram, self.eng)


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#