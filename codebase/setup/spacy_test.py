# Test Spacy Models / Corpus

# path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  

# dependencies
import spacy
import re

# initialize
platform  = sys.platform
if bool(re.match("win", platform))==True:
	print("windows")
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy_win','en_core_web_sm','en_core_web_sm-2.0.0'))

else: 
	print("non-windows")
	spacy_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'spacy','en_core_web_sm-1.2.0','en_core_web_sm','en_core_web_sm-1.2.0'))

# test
try: 

	nlp = spacy.load(spacy_dir)
	doc = nlp(u'This is a Spacy test. These are two purple elephants.')
	doc.sents
	
	print("## : ) SUCCESS > Spacy successfully configured (spacy_test.py)")

except Exception as e: 
	
	print("## :( ERROR > Spacy not properly configured (spacy_test.py)")
