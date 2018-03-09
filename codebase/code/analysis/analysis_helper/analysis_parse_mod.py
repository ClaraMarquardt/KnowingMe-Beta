# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_parse_mod
# Purpose:      Module - Define parse analysis functions
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

# dep_parse
#---------------------------------------------#

def dep_parse(msg_sentence, english):
	
	# print("Launching - dep_parse")

	"""
		
	"""

	# dependency parsing successful
	try: 

		if english==1:

			# initialize
			msg_text_parse     = []

			# parse
			for s in msg_sentence:
				bak = s
				s   = ""
				for x in bak:
					if x in string.punctuation:
						s += " "
					else:
						s += x
				s = ' '.join(s.split())	
				doc = nlp(unicode(s))
				cur = []
				for sent in doc.sents: 
					pos = sent.start
					for tok in sent:
						ele = "%s(%s-%d, %s-%d)"%(tok.dep_, tok.head.text, tok.head.i + 1 - pos, tok.text, tok.i + 1 - pos)
						cur.append(ele)
					msg_text_parse.append(cur)

		else:

			msg_text_parse = dict()

	# dependency parsing unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - dep_parse [text]")
		print(e)

		msg_text_parse = dict()
	
	# return
	# print("Successfully Completed - dep_parse")
	return(msg_text_parse)



# pos_tag
#---------------------------------------------#

def pos_tag(msg_sentence, english, sent_count=5):
	
	# print("Launching - pos_tag")

	"""
		
	"""

	# position tagging successful
	try: 

		if english==1:

			# initialize
			word_pos          = 0
			msg_text_pos      = []
			msg_text_pos_dict = {}

			# iterate
			if (len(msg_sentence)>0):
			
				# parse
				for s in msg_sentence[0:np.min([sent_count, len(msg_sentence)])]: 
				
					doc  = nlp(unicode(s))
			
					for word in doc:
				
						word_tag = word.tag_
				
						msg_text_pos.append(word_tag)
						msg_text_pos_dict[word_pos] = dict(word=str(word), tag=word_tag)

						word_pos = word_pos + 1

		else: 

			msg_text_pos      = []
			msg_text_pos_dict = {}

	# position tagging unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - pos_tag [text]")
		print(e)

		msg_text_pos      = []
		msg_text_pos_dict = {}

	# return
	# print("Successfully Completed - pos_tag")
	return(msg_text_pos, msg_text_pos_dict)


# lang_parse
#---------------------------------------------#

def lang_parse(msg_text):
	
	# print("Launching - lang_parse")

	"""
		
	"""

	# language parsing successful
	try: 

		if (len(msg_text)>0): 

			lang        = detect(str(''.join(x for x in msg_text if x in string.printable)))
		
			if (lang=="en"):
				eng  	= 1
			else:
				eng 	= 0
		
		else: 
			lang  = ''
			eng   = 0

	# language parsing unsuccessful (NO NEED TO REPORT ERROR)
	except Exception as e: 

		# error message
		# print("Error Encountered - lang_parse [text]")
		# print(e)

		lang  = ''
		eng   = 0
	
	# return
	# print("Successfully Completed - lang_parse")

	return(lang, eng)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#