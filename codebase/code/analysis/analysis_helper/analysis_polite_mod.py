# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_polite_mod
# Purpose:      Module - Define polite analysis functions
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
sys.path.append(os.path.normpath(os.path.join(app_root,'code','analysis','analysis_model', 'politeness','politeness_feature')))
from vectorizer import * 
from politeness_strategies import * 

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from misc import *

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# polite_score
#---------------------------------------------#

def polite_score(msg_sentence, msg_parse, msg_unigram, msg_bigram, msg_sentence_request,polite_model_path=polite_model_path):
	
	# print("Launching - polite_score")
	
	"""

	"""

	# politeness scoring successful
	try: 
		request_sentence = np.array(msg_sentence).tolist()
		
		if len(request_sentence)>0 and len(msg_sentence_request)>0:
		
			# initialize
			polite_score_list = []

			# initialize model
			request_sentence = np.array(msg_sentence)[np.array(msg_sentence_request)].tolist()
			request_unigram  = np.array(msg_unigram)[np.array(msg_sentence_request)].tolist()
			request_bigram   = np.array(msg_bigram)[np.array(msg_sentence_request)].tolist()
			request_parses   = np.array(msg_parse)[np.array(msg_sentence_request)].tolist()
			
			if len(request_sentence)>0:
		
				# Load model, initialize vectorizer
				clf 	   = cPickle.load(open(polite_model_path))
				vectorizer = PolitenessFeatureVectorizer()
		
				# Loop over sentences
				for i in range(0,len(request_sentence)): 
									
					# Generate dictionary
					request_text_temp    = request_sentence[i]
					request_unigram_temp = request_unigram[i]
					request_bigram_temp  = request_bigram[i]
					request_bigram_temp  = [tuple(x) for x in request_bigram_temp]		
					request_parses_temp  = request_parses[i]

					request         = {"text":request_text_temp, "sentences":request_text_temp, "bigrams":request_bigram_temp, "unigrams":request_unigram_temp, "parses":request_parses_temp}
				
					# vectorizer returns {feature-name: value} dict
					features   = vectorizer.features(request)
					fv         = [features[f] for f in sorted(features.iterkeys())]
			
					# single-row sparse matrix
					X     = csr_matrix(np.asarray([fv]))
					probs = clf.predict_proba(X)
			
					# return format
					polite_score = probs[0][0]

					# append
					polite_score_list.append(polite_score)
			
				# aggregate
				polite_score_list = sorted(polite_score_list)
				# polite_score    = polite_score_list[int(np.argmax([np.absolute(x-0.5) for x in polite_score_list]))]
				polite_score      = np.min(polite_score_list)
			
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

def request_identification(sentence, sentence_parsed, english):

	# print("Launching - request_identification")

	"""
		
	"""

	# request identification successful
	try: 
		
		if (english==1): 

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


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#