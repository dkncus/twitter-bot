import textgen
import random
class MarkovChain:
	def __init__(self, corpus):
		#Create a histogram of the most used words
		self.histogram, corpus_words = textgen.histogram(corpus)

		#Create a set of probabilities (0-1) that each word in the histogram will occur
		self.probabilities = textgen.gen_probabilities(self.histogram)

		#Markov Chain - Dictionary Object
		#markov_chain = {"<word>": [["word", .05], ["word", .21], ... ["word", .1]]}
		self.markov_chain = {}

		for i in range(len(corpus_words) - 1):
			current_word = corpus_words[i]  #current word being tested against
			next_word = corpus_words[i + 1] #next word being tested against

			#if the word is not already in the markov chain
			if current_word not in self.markov_chain:
				#new starting word added to the chain, with its following word and probability
				self.markov_chain[current_word] = [[next_word, self.probabilities[next_word]]];
			else:
				#if the next word is not in the links of the current word's markov chain
				current_links = self.markov_chain[current_word]
				linked_words = []
				for n in current_links:
					linked_words.append(n[0])

				if next_word not in linked_words:
					current_links.append([next_word, self.probabilities[next_word]])
					self.markov_chain[current_word] = current_links

	def walk(self, steps, starting_word):

		#start the chain with the starting word
		links = self.markov_chain[starting_word]
		sentence = starting_word
		steps -= 1

		#for each word that needs to be found
		for i in range(steps):
			#file each word and probability of a given link into these 2 lists
			words = []
			probs = []
			for link in links:
				words.append(link[0])
				probs.append(1)

			chosen_word = random.choices(population=words, weights=probs)
			print(chose)
			sentence += " " + chosen_word[0]

		return sentence