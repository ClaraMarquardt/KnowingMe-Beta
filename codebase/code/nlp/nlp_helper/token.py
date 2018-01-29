## Module    > token
## Functions > tokenize, unigram_bigram

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  
	 
# Modules
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
# from * import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Dependencies - External
#---------------------------------------------#
import nltk
import re
import string
import numpy as np

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# tokenize
#---------------------------------------------#

def tokenize(msg_text, token_unit):
	
	# print("Launching - tokenize")

	"""
		
	"""

	# initialize
	msg_text_tmp = unicode(msg_text, 'utf-8')

	# tokenization successful
	try: 
	
		if token_unit=='character':
		# ----------------------

			## Base Python

			# prepare
			token_set = re.sub("[ ]*", "", msg_text_tmp)

			# apply
			token_set  = list(token_set)

			# clean 
			
			## remove punctuation
			token_set = [x for x in token_set if not re.match('[' + string.punctuation + ']+', x)]

		elif token_unit=='word':
		# ----------------------

			## NLTK - nltk.tokenize.word_tokenize > Recommended Word Tokenizer 
			### TreebankWordTokenizer (Regx) + PunktSentenceTokenizer (Algorithmic + Language-Specific)

			# apply
			token_set  = nltk.tokenize.word_tokenize(msg_text_tmp)

			# clean 
			
			## remove punctuation (i.e. punctuation only words such as "!"" vs. keep "n't")
			token_set = [x for x in token_set if not re.match('[' + string.punctuation + ']+', x)]
		
		elif token_unit=='sentence':
		# ----------------------

			## NLTK - nltk.tokenize.sent_tokenize > Recommended Sentence Tokenizer 
			### PunktSentenceTokenizer (Algorithmic + Language-Specific)

			# apply
			token_set    = nltk.tokenize.sent_tokenize(msg_text_tmp)
			
	# tokenization unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - token [text]")
		print(e)

		token_set = [msg_text]

	# return
	# print("Successfully Completed - tokenize")
	return(token_set)

# unigram_bigram
#---------------------------------------------#

def unigram_bigram(msg_sentence):
	
	# print("Launching - unigram_bigram")

	# """
		
	# """

	# unigram/bigram identification successful
	try: 

		msg_text_unigram =  [[y for y in t] for t in map(lambda x: nltk.word_tokenize(x), msg_sentence)]
		msg_text_bigram  =  [[y for y in l] for l in map(lambda x: nltk.bigrams(x), msg_text_unigram)]

	# position tagging unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - unigram_bigram [text]")
		print(e)

		msg_text_unigram = [np.nan]
		msg_text_bigram  = [np.nan]

	# return
	# print("Successfully Completed - unigram_bigram")
	return(msg_text_unigram,msg_text_bigram)


#---------------------------------------------#
