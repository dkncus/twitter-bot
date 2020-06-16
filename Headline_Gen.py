import nltk
from nltk import word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags, ne_chunk
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

class Headline_Gen:
	#Initialization function
	def __init__(self, fileloc_dataset = r"datasets\reference\non_clickbait_data.txt"):
		print("Generating POS tags for dataset:", fileloc_dataset)
		self.untagged, self.tagged_headlines = self.preprocess(fileloc_dataset)

		#Tag with proper NE recognition
		print("Generating spaCy named entity recognition tags")
		self.spacy_headlines = self.gen_spacy_tags(self.untagged)

	#Generate POS tags for each headline, dependent on how many NNP's there are in the sentence
	def preprocess(self, fileloc):
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
				if self.tot_caps(line) < int(len(line.split()) * 0.7):
					tagged_headlines.append(tagged)
					originals.append(line)
				
				#Get the next line
				line = headlines.readline()

			except:
				n = 0
		return originals, tagged_headlines

	#Returns the number of capitalized words in a string
	def tot_caps(self, string):
		#Split words into a list
		words = string.split()
		count = 0

		#For each word, check if it is capital, if it is, add 1 to count
		for w in words:
			if w[0].isupper():
				count = count + 1

		return count

	#Returns the parsed tokens 
	def chunk(self, pattern, tagged_headlines):
		parsed = []
		chunker = nltk.RegexpParser(pattern)
		for hl in tagged_headlines:
			parsed = chunker.parse(hl)
			parsed.append(parsed)

		return parsed

	#Recognize named entities using NE Chunks
	def create_trees(self, tagged_headlines):
		ne_chunks = []
		for hl in tagged_headlines:
			ne_chunks.append(ne_chunk(hl))
		return ne_chunk

	#Create SpaCY tags for NER, (e.g. NORP, ORG, MONEY, DATE, etc.)
	def gen_spacy_tags(self, untagged):
		tagged_headlines = []
		for hl in untagged:
			doc = nlp(hl)
			tagged_headlines.append(doc)

		return tagged_headlines

if __name__ == '__main__':
	#Tag headlines from the dataset
	h = Headline_Gen()

	for i, hl in enumerate(h.spacy_headlines):
		#print(i, ":", hl)
		rep_ents = []
		return_string = str(hl.text)
		for x in hl.ents:
			#print('\t', x.text, x.label_)
			rep_ents.append([x.text, x.label_])
		for rep in rep_ents:
			return_string = return_string.replace(str(rep[0]), str(rep[1]))

		print(return_string)
		print()
		
	print("Number of Headlines:", len(h.tagged_headlines))