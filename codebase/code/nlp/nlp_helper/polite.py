## Module    > polite 
## Functions > polite_score, request_identification

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root     = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root,'code','nlp','nlp_model', 'politeness','politeness_feature')))
from vectorizer import * 
from politeness_strategies import * 

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Other Paths
polite_model = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'politeness','politeness_svm.p')) 

# Dependencies - External
#---------------------------------------------#
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import numpy as np
import pandas as pd
import cPickle
from scipy.sparse import csr_matrix

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# polite_score
#---------------------------------------------#

def polite_score(msg_sentence, msg_parse, msg_unigram, msg_bigram, msg_sentence_request,polite_model=polite_model):
	
	# print("Launching - polite_score")
	
	"""

	"""


	# politeness scoring successful
	try: 
		request_sentence = np.array(msg_sentence).tolist()
		
		if len(request_sentence)>0 and len(msg_sentence_request)>0:
		
			# Initialize
			request_sentence = np.array(msg_sentence)[np.array(msg_sentence_request)].tolist()
			request_unigram  = np.array(msg_unigram)[np.array(msg_sentence_request)].tolist()
			request_bigram   = np.array(msg_bigram)[np.array(msg_sentence_request)].tolist()
			request_parses   = np.array(msg_parse)[np.array(msg_sentence_request)].tolist()
			
			if len(request_sentence)>0:
		
				# Generate dictionary
				request_text    = ' '.join(request_sentence)
				request_unigram = sum(request_unigram, [])
				request_bigram  = sum(request_bigram, [])
				request_bigram  = [tuple(x) for x in request_bigram]		
		
				request         = {"text":request_text, "sentences":request_sentence, "bigrams":request_bigram, "unigrams":request_unigram, "parses":request_parses}
				
				# Load model, initialize vectorizer
				clf 	   = cPickle.load(open(polite_model))
				vectorizer = PolitenessFeatureVectorizer()
			
				# vectorizer returns {feature-name: value} dict
				features   = vectorizer.features(request)
				fv         = [features[f] for f in sorted(features.iterkeys())]
			
				# Single-row sparse matrix
				X     = csr_matrix(np.asarray([fv]))
				probs = clf.predict_proba(X)
			
				# Massage return format
				polite_score = probs[0][0]
			
			else:
		
				polite_score = np.nan
		
		else:
		
			polite_score = np.nan

	# politeness scoring unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - polite_score")
		print(e)

		polite_score   = np.nan

	# return
	# print("Successfully Completed - polite_score")
	return(polite_score)

# request_identification
#---------------------------------------------#

def request_identification(sentence, sentence_parsed):

	# print("Launching - request_identification")

	"""
		
	"""

	# request identification successful
	try: 
	
		if "?" in sentence:
			request = True
		elif check_elems_for_strategy(sentence_parsed, initial_polar) or check_elems_for_strategy(sentence_parsed, aux_polar):
			request = True
		else:
			request = False

	# request identification unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - request_identification")
		print(e)

		request = False

	# return
	# print("Successfully Completed - request_identification")
	return(request)


#---------------------------------------------#
