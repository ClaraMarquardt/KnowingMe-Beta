## Module > vectorizer 
## Class > PolitenessFeatureVectorizer

# misc
from __future__ import unicode_literals

# Dependencies - Internal
#---------------------------------------------#

# Path
import os, sys
local_dir  = os.path.split(__file__)[0]
app_root   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..","..","..",".."))  

from politeness_strategies import get_politeness_strategy_features

# Dependencies - External
#---------------------------------------------#
import os
import cPickle
import string
import nltk
from itertools import chain
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
import json
import re

# Class Definition
#---------------------------------------------#

# PolitenessFeatureVectorizer
#---------------#

class PolitenessFeatureVectorizer:

    """
    Returns document features based on-
        - unigrams and bigrams
        - politeness strategies
            (inspired by B&L, modeled using dependency parses)
    """

    unigram_filename = os.path.join(local_dir, "featunigrams.p")
    bigram_filename  = os.path.join(local_dir, "featbigrams.p")

    def __init__(self):
        """
        Load pickled lists of unigram and bigram features
        These lists can be generated using the training set
        and PolitenessFeatureVectorizer.generate_bow_features
        """
        self.unigrams = cPickle.load(open(self.unigram_filename))
        self.bigrams  = cPickle.load(open(self.bigram_filename))


    def features(self, document):
        """
        document must be a dict of the following format--
            {
                'text': "text str",
            }
        """
        feature_dict = {}
        
        # Add unigram, bigram features:
        feature_dict.update(self._get_term_features(document))
        
        # Add politeness strategy features:
        feature_dict.update(get_politeness_strategy_features(document))
        return feature_dict

    def _get_term_features(self, document):
        
        # One binary feature per ngram in in self.unigrams and self.bigrams
        unigrams, bigrams = document['unigrams'], document['bigrams'] 
        
        # Add unigrams to document for later use
        unigrams, bigrams = set(unigrams), set(bigrams)
        f = {}
        f.update(dict(map(lambda x: ("UNIGRAM_" + str(x), 1 if x in unigrams else 0), self.unigrams)))
        f.update(dict(map(lambda x: ("BIGRAM_" + str(x), 1 if x in bigrams else 0), self.bigrams)))
        return f 


#---------------------------------------------#

