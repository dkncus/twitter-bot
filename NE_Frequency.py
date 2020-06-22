from collections import Counter
import string
import spacy
import en_core_web_sm
import emoji
nlp = en_core_web_sm.load()

class NE_Frequency:
	#Types of spaCy tags
	def __init__(self, plaintext_tweets):
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
		self.tweets = plaintext_tweets
		self.tokenized_tweets = self.tokenize_tweets(self.tweets)
		self.frequency_map = self.get_entity_frequencies(self.tokenized_tweets)
		for s in self.frequency_map:
			if self.frequency_map[s] == []:
				self.frequency_map[s].append(('thing', 1))
		
	#Read in the tweets to the tweet list

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
				dictionary[entity.label_].append(entity.text.rstrip(r'\'s'))

		#If same object is recognized in multiple categories, remove it, keep in category it appears most frequently in
		for category in dictionary:
			freq_map = Counter(dictionary[category]).most_common()
			dictionary[category] = freq_map

		#Check dictionary entries for extraneous characters (#, links, emoji, etc.) and remove
		for category in dictionary:
			entity_list = []
			for entity in dictionary[category]:
				has_emoji = False
				for character in entity[0]:
					if character in emoji.UNICODE_EMOJI:
						has_emoji = True
				if '#' in entity[0] or 'http' in entity[0] or '@' in entity[0] or has_emoji:
					entity_list.append(entity)
			for entity in entity_list:
				dictionary[category].remove(entity)

		return dictionary

	#Print out the given tokenized tweets
	def print_tokenized(self, tokenized_tweets):
		for i, tweet in enumerate(tokenized_tweets):
			print(i, ":", tweet)
			for entity in tweet.ents:
				print('\t', entity.text, entity.label_)
			print()

	#Print dictionary
	def print_freq_map(self, threshold_value):
		for category in self.frequency_map:
			print(category)
			for entity in self.frequency_map[category]:
				if entity[1] >= threshold_value:
					print('\t', entity)
			print()