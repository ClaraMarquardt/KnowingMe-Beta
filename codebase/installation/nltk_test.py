# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         nltk_test
# Purpose:      Test installation of nltk package
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialisation
# ------------------------------------------------------------------------ #

# Paths
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  

# Dependencies
import nltk
nltk_dir          = os.path.normpath(os.path.join(app_root_init, 'dependencies', 'nltk'))

# ------------------------------------------------------------------------ #
# Test Installation
# ------------------------------------------------------------------------ #

try: 

	## initialize
	nltk.data.path.append(nltk_dir)

	## punkt (tokenizer)
	nltk.tokenize.word_tokenize('This is a red giraffe')

	## wordnet (corpus)
	from nltk.corpus import wordnet as wn
	wn.synsets('happiness')
	
	print("## : ) SUCCESS > NLTK successfully configured (nltk_test.py)")

except Exception as e: 
	
	print("## : ( ERROR > NLTK not properly configured (nltk_test.py)")

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
