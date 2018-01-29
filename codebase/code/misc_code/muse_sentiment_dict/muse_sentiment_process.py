# Generate the sentiment dictionary

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root             = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  
sentiment_dict_path  = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'sentiment', 'sentiment_dict.json'))

sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'sentiment')))
import muse_sentiment

# Dependencies - External
#---------------------------------------------#
import numpy as np
import pandas as pd
import nltk
import json
from nltk.corpus import wordnet as wn 

# [0] Initialize
#---------------------------------------------#
sentiment_dict = muse_sentiment.sentiment_dict

## STATUS
print(sum([len(sentiment_dict[x]) for x in sentiment_dict.keys()]))

# [1] Expand the dictionary (synonyms)
#---------------------------------------------#
for wordlist_name in sentiment_dict.keys():

	# initialize
	wordlist_raw = sentiment_dict[wordlist_name]
	wordlist_mod = []

	print(wordlist_name)
	print(len(wordlist_raw))

	# expand 
	for word in wordlist_raw:
		wordlist_mod.append(unicode(word))
		for i in wn.synsets(word): 
			for j in i.lemmas(): 
				for k in j.derivationally_related_forms(): 
					wordlist_mod.append(unicode(k.name()))

	# combine & set to unique
	wordlist_mod = set(wordlist_mod)
	print(len(wordlist_mod))

	# update
	sentiment_dict[wordlist_name] = wordlist_mod

# [2] Drop words length > bigram & that contain an '
#---------------------------------------------#
for wordlist_name in sentiment_dict.keys():

	# initialize
	wordlist_raw = sentiment_dict[wordlist_name]
	
	print(wordlist_name)
	print(len(wordlist_raw))

	# subset
	wordlist_mod = [x for x in wordlist_raw if len(nltk.word_tokenize(x))<=2]
	wordlist_mod = [x for x in wordlist_raw if "'" not in x]

	print(len(wordlist_mod))

	# update
	sentiment_dict[wordlist_name] = wordlist_mod

## STATUS
print(sum([len(sentiment_dict[x]) for x in sentiment_dict.keys()]))

# [3] Generate aggregated categories
#---------------------------------------------#
sentiment_dict['aggregate']          = np.concatenate([sentiment_dict[x] for x in sentiment_dict.keys()]).tolist()
sentiment_dict['positive_aggregate'] = np.concatenate([sentiment_dict['wow'],sentiment_dict['gratitude'],sentiment_dict['pride'],sentiment_dict['joy'],sentiment_dict['nice'],sentiment_dict['pos_surprise'],sentiment_dict['humor']]).tolist()
sentiment_dict['negative_aggregate'] = np.concatenate([sentiment_dict['shame'],sentiment_dict['disappointment'],sentiment_dict['emotion'],sentiment_dict['anxiety'],sentiment_dict['sorry'],sentiment_dict['pity'],sentiment_dict['worry'],sentiment_dict['embarassment'],sentiment_dict['contempt'],sentiment_dict['hate'],sentiment_dict['jealousy'],sentiment_dict['despair'],sentiment_dict['fear'],sentiment_dict['shock'],sentiment_dict['sadness'],sentiment_dict['conflict'],sentiment_dict['guilt']]).tolist()
sentiment_dict['other_aggregate']    = [x for x in sentiment_dict['aggregate'] if x not in np.concatenate([sentiment_dict['positive_aggregate'], sentiment_dict['negative_aggregate']])]


# [4] Save
#---------------------------------------------#
with open(sentiment_dict_path, 'w') as f:
    json.dump(sentiment_dict, f, indent=4)


#---------------------------------------------#

