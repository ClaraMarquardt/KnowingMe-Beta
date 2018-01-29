# Test NLTK Models / Corpus

# path
import os, sys
app_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  

# dependencies
import nltk

# initialize
nltk_dir = os.path.normpath(os.path.join(app_root, 'dependencies', 'nltk'))

# test
nltk.data.path.append(nltk_dir)

try: 

	## punkt (tokenizer)
	nltk.tokenize.word_tokenize('This is a red giraffe')

	## wordnet (corpus)
	from nltk.corpus import wordnet as wn
	wn.synsets('happiness')
	
	print("## : ) SUCCESS > NLTK successfully configured (nltk_test.py)")

except Exception as e: 
	
	print("## :( ERROR > NLTK not properly configured (nltk_test.py)")

