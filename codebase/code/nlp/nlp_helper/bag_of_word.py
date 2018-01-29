## Module    > bag_of_word 
## Functions > word_bag, sentiment_word_bag, pos_word_bag

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
app_root             = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",".."))  

# Modules
sys.path.append(os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_helper')))
# from .... import *

sys.path.append(os.path.normpath(os.path.join(app_root,'code')))
from cross import *

# Other Paths
sentiment_dict_path  = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'sentiment', 'sentiment_dict.json'))
pos_dict_path        = os.path.normpath(os.path.join(app_root, 'code','nlp','nlp_model', 'coordination', 'pos_dict.json'))

# Dependencies - External
#---------------------------------------------#
import numpy as np
import pandas as pd
import json

#----------------------------------------------------------------------------#
#			                Function Definition                              #
#----------------------------------------------------------------------------#

# word_bag
#---------------------------------------------#

def word_bag(msg_unigram, msg_bigram, word_dictionary):

	# print("Launching - word_bag")

	# """
		
	# """

	# initialize
	count_list      = []
	count_set       = []
	count_pos       = []
	count_indic     = []

	# count
	for word_list_name in word_dictionary.keys():
		
		word_list     = word_dictionary[word_list_name]

		unigram_set   = list(set([x for x in msg_unigram if x in word_list]))
		bigram_set    = list(set([x for x in msg_bigram if x in word_list]))
		
		unigram_pos   = [msg_unigram.index(x) for x in unigram_set]

		total_set     = sum([unigram_set, bigram_set], [])
		total_set     = list(set(sum([x.split() for x in total_set], [])))
		
		total_pos     = list(set(sum([unigram_pos], [])))
		
		total_count   = len(total_set)
		total_indic   = min(1,total_count)

		count_list.append(total_count)
		count_set.append(total_set)
		count_pos.append(total_pos)
		count_indic.append(total_indic)

	# format
	word_bag_count = dict([(x,y) for (x,y) in zip(word_dictionary.keys(), count_list)])
	word_bag_set   = dict([(x,y) for (x,y) in zip(word_dictionary.keys(), count_set)])
	word_bag_pos   = dict([(x,y) for (x,y) in zip(word_dictionary.keys(), count_pos)])
	word_bag_indic = dict([(x,y) for (x,y) in zip(word_dictionary.keys(), count_indic)])

	# return
	# print("Successfully Completed - word_bag")
	return(word_bag_count, word_bag_set, word_bag_pos,word_bag_indic)

# sentiment_word_bag
#---------------------------------------------#

def sentiment_word_bag(msg_unigram, msg_bigram, dict_path=sentiment_dict_path):

	# print("Launching - sentiment_word_bag")

	# """
		
	# """

	# load the dictionary
	with open(sentiment_dict_path) as f:
		sentiment_dict = json.load(f)

	# format
	msg_unigram    = [x for l in msg_unigram for x in l]
	msg_bigram     = [x for l in msg_bigram for x in l]
	msg_bigram     = [' '.join(x) for x in msg_bigram]

	# process
	sentiment_word_bag_count, sentiment_word_bag_set, sentiment_word_bag_pos, sentiment_word_bag_indic = word_bag(msg_unigram, msg_bigram, sentiment_dict)

	# combine the word set
	sentiment_word_bag_set_agg = sentiment_word_bag_set
	
	for word_list_name in sentiment_word_bag_set_agg.keys():
		if len(sentiment_word_bag_set_agg[word_list_name])>1:
			sentiment_word_bag_set_agg[word_list_name] = ', '.join(sentiment_word_bag_set_agg[word_list_name])
		else:
			sentiment_word_bag_set_agg[word_list_name] = sentiment_word_bag_set_agg[word_list_name]
	
	# return
	# print("Successfully Completed - sentiment_word_bag")
	return(sentiment_word_bag_count, sentiment_word_bag_set, sentiment_word_bag_set_agg, sentiment_word_bag_indic)


def pos_word_bag(msg_pos_dict, dict_path=pos_dict_path):
#---------------------------------------------#

	# print("Launching - pos_word_bag")

	# """
		
	# """

	# load the dictionary
	with open(pos_dict_path) as f:
		pos_dict = json.load(f)

	# format
	msg_pos = [msg_pos_dict[x]['tag'] for x in msg_pos_dict.keys()]

	# process
	pos_word_bag_count, pos_word_bag_set, pos_word_bag_pos,pos_word_bag_indic = word_bag(msg_pos,[], pos_dict)

	# obtain the words 

	## initialize
	pos_word_bag_set_mod =  {}

	## extract
	for word_list_name in pos_word_bag_pos.keys():
		
		word_pos     = np.array(pos_word_bag_pos[word_list_name])
		unigram_set  = []
		if len(word_pos)>0:
			unigram_set=[msg_pos_dict[x]['word'] for x in word_pos]
		pos_word_bag_set_mod[word_list_name] = unigram_set

	# combine the word set
	pos_word_bag_set_mod_agg = pos_word_bag_set_mod
	
	for word_list_name in pos_word_bag_set_mod_agg.keys():
		if len(pos_word_bag_set_mod_agg[word_list_name])>1:
			pos_word_bag_set_mod_agg[word_list_name] = ', '.join(pos_word_bag_set_mod_agg[word_list_name])
		else:
			pos_word_bag_set_mod_agg[word_list_name] = pos_word_bag_set_mod_agg[word_list_name]
	
	# return
	# print("Successfully Completed - pos_word_bag")
	return(pos_word_bag_count, pos_word_bag_set_mod,pos_word_bag_set_mod_agg, pos_word_bag_indic)


#---------------------------------------------#
