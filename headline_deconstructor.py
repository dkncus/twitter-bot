import nltk
from nltk import word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags, ne_chunk

import pprint

import spacy
from spacy import displacy

from collections import Counter

import en_core_web_sm
nlp = en_core_web_sm.load()

cities = []
states = []
countries = []

#Initialize the locations
def init_locations(cities_loc, states_loc, countries_loc):
	cities_file = open(cities_loc)
	states_file = open(states_loc)
	countries_file = open(countries_loc)

	#Initialize cities
	line = cities_file.readline()
	while line:
		line = line.rstrip("\n")
		cities.append(line)
		line = cities_file.readline()

	#Initialize states
	line = states_file.readline()
	while line:
		line = line.rstrip("\n")
		states.append(line)
		line = states_file.readline()

	#Initialize countries
	line = countries_file.readline()
	while line:
		line = line.rstrip("\n")
		countries.append(line)
		line = countries_file.readline()

	return 0

#Generate POS tags for each headline, dependent on how many NNP's there are in the sentence
def preprocess(fileloc):
	#Datasets, will be returned at the end
	tagged_headlines = []
	originals = []

	#Open the given file
	headlines = open(fileloc)
	line = headlines.readline()

	#for each line in the file
	while line:
		try:
			#Strip the line of the \n tag, tokenize and POS tag the line
			line = line.rstrip("\n")
			tagged = nltk.pos_tag(word_tokenize(line))

			#Check if the string is empty, if not, append to the list
			if len(tagged) > 0 and tot_caps(line) < int(len(line.split()) * 0.7):
				tagged_headlines.append(tagged)
				originals.append(line)
			
			#Get the next line
			line = headlines.readline()

		except: #Cannot read characters from the file
			n = 0

	return originals, tagged_headlines

#Returns the number of capitalized words in a string
def tot_caps(string):
	#Split words into a list
	words = string.split()
	count = 0

	#For each word, check if it is capital, if it is, add 1 to count
	for w in words:
		if w[0].isupper():
			count = count + 1

	return count

#Returns the parsed tokens 
def chunk(pattern, tagged_headlines):
	parsed = []
	chunker = nltk.RegexpParser(pattern)
	for hl in tagged_headlines:
		parsed = chunker.parse(hl)
		parsed.append(parsed)

	return parsed

#Recognize named entities using NE Chunks
def create_trees(tagged_headlines):
	ne_chunks = []
	for hl in tagged_headlines:
		ne_chunks.append(ne_chunk(hl))
	return ne_chunk

if __name__ == '__main__':
	#Initialize location data (cities, states countries)
	init_locations(r"datasets\cities.txt", r"datasets\states.txt", r"datasets\countries.txt")

	#Tag headlines from the dataset
	untagged, tagged_headlines = preprocess(r"datasets\non_clickbait_data.txt")

	processed_headlines = chunk('NP: {<DT>?<JJ>*<NN>}', tagged_headlines)

	ne_trees = create_trees(tagged_headlines)

	#Print the number of headlines tagged
	print("Number of Headlines:", len(tagged_headlines))