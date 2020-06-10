from nltk.tokenize import word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.corpus import stopwords
import operator
import nltk

#set filepath to java
import os
java_path = r"C:\Program Files\Java\jdk-13.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

def tokenize_text(text):
	tokens = word_tokenize(text)
	return tokens

# A function to create a tagger using StanfordPOSTagger
def make_tagger():
	stanford_dir = r"C:\Users\dkncu\Desktop\Twitter Bot\stanford-tagger-4.0.0" # change it into your own path
	modelfile = stanford_dir + r"\models\english-bidirectional-distsim.tagger" # model file
	jarfile = stanford_dir + r"\stanford-postagger.jar"# jar file
	st = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile) # create a tagger
	return st

# A function to remove the stop words
def remove_stopwords(tokens):
	# Remove the stop words by using the english stop words provided by NLTK 
	e_stopwords = set(stopwords.words('english'))
	clean_tokens = [tok for tok in tokens if len(tok.lower())>1 and (tok.lower() not in e_stopwords)]
	return clean_tokens

# A function to tag the words and return the result
def tag(tokens):
	clean_tokens = remove_stopwords(tokens) # First, remove the stop words and get the clean tokens
	tagger = make_tagger()
	tagged_data = tagger.tag(clean_tokens) # Tag the tokens with the tagger

	# print the result in a file with the format "word/tag (frequency=num)"
	data = ""
	for word, tag in tagged_data:
		data += word + "/" + tag + '\n' 

	return data

# A function to call all the functions above
def stanford_pos_tagger(text_string):
	tokens = tokenize_text(text_string) # split into tokens
	data = tag(tokens)
	return data

# main function
if __name__ == '__main__':
	data = stanford_pos_tagger("LIVE: Donald Trump tear gasses protestors in front of the White House")
	print(data)
