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
import spacy, re

# Initialize Spacy
platform  = sys.platform
if bool(re.match("win", platform))==True:
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy_win','en_core_web_sm','en_core_web_sm-2.0.0'))

else: 
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy','en_core_web_sm-1.2.0','en_core_web_sm','en_core_web_sm-1.2.0'))

# ------------------------------------------------------------------------ #
# Test Installation
# ------------------------------------------------------------------------ #

try: 

	# initialize
	nlp = spacy.load(spacy_dir)

	# test
	doc = nlp(u'This is a Spacy test. These are two purple elephants.')
	doc.sents
	
	print("## : ) SUCCESS > Spacy successfully configured (spacy_test.py)")

except Exception as e: 
	
	print("## : ( ERROR > Spacy not properly configured (spacy_test.py)")

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
