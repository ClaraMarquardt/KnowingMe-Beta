# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         analysis_sentiment_mod
# Purpose:      Module - Define sentiment analysis functions
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

# sentiment_score
#---------------------------------------------#

def sentiment_score(msg_sentence, english):
	
	# print("Launching - polite_score")
	
	"""

	"""
	# sentiment scoring successful
	try: 

		if (english==1): 
			
			sentiment_text        = ' '.join(msg_sentence[0:int(np.min([4, len(msg_sentence)]))])
			sentiment_text        = str(''.join(x for x in sentiment_text if x in string.printable))
	
			## vader
			## ----------

			# initialize
			sentiment_score_vader       = []
			sentiment_score_vader_dist  = []
		
			# iterate
			sentiment_score_vader_temp = vader_nlp.polarity_scores(sentiment_text) 

			sentiment_score_vader_temp_score = sentiment_score_vader_temp['compound']
			sentiment_score_vader_temp_score = (float(sentiment_score_vader_temp_score) + 1)/2
			sentiment_score_vader.append(sentiment_score_vader_temp_score)

			sentiment_score_vader_temp_dist  = [sentiment_score_vader_temp['neg'],
				sentiment_score_vader_temp['neu'],sentiment_score_vader_temp['pos']]
			sentiment_score_vader_dist.append(sentiment_score_vader_temp_dist)

			sentiment_score_vader         = np.nanmean(np.array(sentiment_score_vader))
		
			sentiment_vader_dist_neg      = np.nanmean([x[0] for x in sentiment_score_vader_dist])
			sentiment_vader_dist_neu      = np.nanmean([x[1] for x in sentiment_score_vader_dist])
			sentiment_vader_dist_pos      = np.nanmean([x[2] for x in sentiment_score_vader_dist])
			sentiment_vader_dist          = [sentiment_vader_dist_neg,sentiment_vader_dist_neu,sentiment_vader_dist_pos]
			# sentiment_vader_dist        = [x/sum(sentiment_vader_dist) for x in sentiment_vader_dist]
			sentiment_vader_dist          = '/'.join(str(x) for x in sentiment_vader_dist)

			## core nlp (ON HOLD)
			## ----------

			sentiment_score         = np.nan
			sentiment_label_score   = ''
			sentiment_dist          = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan', 'np.nan', 'np.nan'])
			sentiment_score_dist    = np.nan
			sentiment_label_dist    = ''

			# # initialize
			# sentiment_score_dict = []
			# sentiment_dist_dict  = []
	
			# # iterate
			# if (len(sentiment_text)>0):
				
			# 	# analyze email
			# 	sentiment_score_temp = core_nlp.annotate(sentiment_text, 
			# 		properties={"outputFormat": "json","annotators": "sentiment", "threads":4})
				
			# 	if (isinstance(sentiment_score_temp,dict)): 
								
			# 		# parse results
			# 		for result_raw in sentiment_score_temp['sentences']:
			# 			sentiment_score_temp        = int(result_raw['sentimentValue'])
			# 			sentiment_dist_temp         = result_raw['sentimentDistribution']
			# 			sentiment_score_dict.append(sentiment_score_temp)
			# 			sentiment_dist_dict.append(sentiment_dist_temp)
	
			# 		# aggregate at the text level
			# 		sentiment_score       = np.nanmean(np.array(sentiment_score_dict))
			# 		sentiment_label_score = ["very_neg","neg","neutral","pos","very_pos"][int(np.round(sentiment_score))]
			# 		sentiment_score       = sentiment_score/4
	
			# 		sentiment_dist_0      = np.nanmean([x[0] for x in sentiment_dist_dict]) # very negative
			# 		sentiment_dist_1      = np.nanmean([x[1] for x in sentiment_dist_dict]) # negative
			# 		sentiment_dist_2      = np.nanmean([x[2] for x in sentiment_dist_dict]) # neutral
			# 		sentiment_dist_3      = np.nanmean([x[3] for x in sentiment_dist_dict]) # positive
			# 		sentiment_dist_4      = np.nanmean([x[4] for x in sentiment_dist_dict]) # very positive
			# 		sentiment_dist        = [sentiment_dist_0,sentiment_dist_1,sentiment_dist_2,sentiment_dist_3,sentiment_dist_4]
			# 		# sentiment_dist        = [x/sum(sentiment_dist) for x in sentiment_dist]
	
			# 		sentiment_score_dist  = [0,1,2,3,4][np.argmax(sentiment_dist)]
			# 		sentiment_label_dist  = ["very_neg","neg","neutral","pos","very_pos"][np.argmax(sentiment_dist)]
			# 		sentiment_score_dist  = sentiment_score_dist/4
					
			# 		sentiment_dist        = '/'.join(str(x) for x in sentiment_dist)
			
				# else:
	
				# 	sentiment_score         = np.nan
				# 	sentiment_label_score   = ''
				# 	sentiment_dist          = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan', 'np.nan', 'np.nan'])
				# 	sentiment_score_dist    = np.nan
				# 	sentiment_label_dist    = ''
	
			# else:
	
			# 	sentiment_score         = np.nan
			# 	sentiment_label_score   = ''
			# 	sentiment_dist          = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan', 'np.nan', 'np.nan'])
			# 	sentiment_score_dist    = np.nan
			# 	sentiment_label_dist    = ''
		
		
		else: 
				
				sentiment_score_vader   = np.nan
				sentiment_vader_dist    = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan'])
				sentiment_score         = np.nan
				sentiment_label_score   = ''
				sentiment_dist          = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan', 'np.nan', 'np.nan'])
				sentiment_score_dist    = np.nan
				sentiment_label_dist    = ''

	# sentiment scoring unsuccessful
	except Exception as e: 

		# error message
		print("Error Encountered - sentiment_score")
		print(e)

		sentiment_score_vader   = np.nan
		sentiment_vader_dist    = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan'])
		sentiment_score         = np.nan
		sentiment_label_score   = ''
		sentiment_dist          = '/'.join(str(x) for x in ['np.nan', 'np.nan', 'np.nan', 'np.nan', 'np.nan'])
		sentiment_score_dist    = np.nan
		sentiment_label_dist    = ''

	# print("Successfully Completed - sentiment_score")
	return(sentiment_score_vader, sentiment_vader_dist, sentiment_score,sentiment_label_score,sentiment_dist,sentiment_score_dist, sentiment_label_dist)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#