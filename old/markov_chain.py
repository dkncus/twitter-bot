import random
from collections import OrderedDict
import re

#Gets a dictionary from a given URL string
def get_dict(urlstring):
	dictionary = open(urlstring)

	line = dictionary.readline()
	words = []

	while line:
		if line != None:
			line = line.rstrip('\n')
			words.append(line)
		line = dictionary.readline()

	return words

def print_sentence(words, length):
	sentence = ""
	for n in range(length):
		word = words[random.randint(0, len(words))]
		if n != 0:
			sentence += " " + word
		else:
			sentence += word

	return sentence

def histogram(source):
	#Histogram object
	histogram = {}

	#Read each line, create list of words
	text = open(source, encoding="utf8")
	line = text.readline()

	#for each line of the source text
	while line:
		#if there is a line here
		if line != None:
			#makes line lowercase and removes all special characters
			line = line.lower()
			line = re.sub('[\W_]+', ' ', line) 

			#split the line into its component words
			split = line.split()
			
			#for each word, check if it's in the histogram already
			for word in split:
				if word in histogram:
					histogram[word] += 1
				else:
					histogram[word] = 1
		#read the next line
		line = text.readline()

		histogram = dict(OrderedDict(sorted(histogram.items(), key=lambda kv: kv[1], reverse = True)))
	#Return the histogram as sorted
	return histogram

def gen_probabilities(histogram):
	#Get data from the list where - words : Population, freq : Frequency of each word, total : Total number of words, probs = Probabilites of each occurance
	words = list(histogram)
	freqs = list(histogram.values())
	total = sum(freqs)
	probs = []

	for freq in freqs:
		probs.append(freq / total)

	return probs

def random_word(hist, probs):
	#Choose a random word with the weighting from probs[]
	words = list(hist)
	word = random.choices(population=words, weights=probs)
	return word[0]

if __name__ == '__main__':
	#words = GetDict('words.txt')
	#print(PrintSentence(words, 5))
	hist = histogram('holmes.txt')
	probabilities = gen_probabilities(hist)
	for i in range(50):
		print(random_word(hist, probabilities))