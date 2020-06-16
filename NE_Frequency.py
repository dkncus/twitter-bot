from collections import Counter
import string
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

class NE_Frequency:
	#Types of spaCy tags
	def __init__(self, tweet_data_loc):
		self.tag_types = [	'PERSON', 
							'NORP', 
							'FAC', 
							'ORG', 
							'GPE', 
							'LOC', 
							'PRODUCT', 
							'EVENT', 
							'WORK_OF_ART', 
							'LAW', 
							'LANGUAGE', 
							'DATE', 
							'TIME', 
							'PERCENT', 
							'MONEY', 
							'QUANTITY', 
							'CARDINAL', 
							'ORDINAL']
		self.word_frequencies = {}
		self.hash_freq = []
		self.tweets = self.read_tweets(tweet_data_loc)
		self.tokenized_tweets = self.tokenize_tweets(self.tweets)
		self.frequency_map = self.get_entity_frequencies(self.tokenized_tweets)

	#Read in the tweets to the tweet list
	def read_tweets(self, fileloc):
		tweets = []
		file = open(fileloc)
		line = file.readline()
		hashtags = []

		#Read each line and clean the data for the parser
		while line:
			#split the line into its individual words
			words = line.split()
			string = ""

			#For every word in those words
			for word in words:
				#Clean lines for # and @ symbols, as well as hyperlinks
				if not (('#' in word) or ('@' in word) or ('http:' in word) or ('https:' in word) or ('&' in word) or('www.' in word)):
					string = string + word + ' '
				elif '#' == word[0]:
					hashtags.append(word)

			tweets.append(string)
			line = file.readline()

		self.hash_freq = Counter(map(str.lower, hashtags)).most_common()
		return tweets

	#Break tweets into tokens and Named Entities and return
	def tokenize_tweets(self, tweets):
		tokenized_tweets = []
		for tweet in tweets:
			doc = nlp(tweet)
			if len(doc.ents) > 0:
				tokenized_tweets.append(doc)

		return tokenized_tweets

	#Get the number of times each entity is mentioned, stored and returned in a dictionary
	def get_entity_frequencies(self, tokenized_tweets):
		dictionary = {}

		#Initialize the Dictionary
		for tag in self.tag_types:
			dictionary[tag] = []

		#Fill in the dictionary with each individual word recognized
		for tweet in tokenized_tweets:
			for entity in tweet.ents:
				dictionary[entity.label_].append(entity.text)

		#If same object is recognized in multiple categories, remove it, keep in category it appears most frequently in
		for category in dictionary:
			freq_map = Counter(dictionary[category]).most_common()
			dictionary[category] = freq_map

		return dictionary

	#Print out the given tokenized tweets
	def print_tokenized(self, tokenized_tweets):
		for i, tweet in enumerate(tokenized_tweets):
			print(i, ":", tweet)
			for entity in tweet.ents:
				print('\t', entity.text, entity.label_)
			print()

	#Print dictionary
	def print_freq_map(self, freq_map):
		for category in freq_map:
			print(category)
			for entity in freq_map[category]:
				print('\t', entity)
			print()

if __name__ == '__main__':
	NE = NE_Frequency()
	#NE.print_tokenized(NE.tokenized_tweets)
	#NE.print_freq_map(NE.frequency_map)