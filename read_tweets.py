import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

#Types of spaCy tags
tag_types = [	'PERSON', 
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

def read_tweets(fileloc):
	tweets = []
	file = open(fileloc)
	line = file.readline()

	#Read each line and clean the data for the parser
	while line:

		#split the line into its individual words
		words = line.split()
		string = ""

		#For every word in those words
		for word in words:
			#Clean lines for # and @ symbols, as well as hyperlinks
			if not (('#' in word) or ('@' in word) or ('http:' in word) or ('https:' in word) or ('&' in word)):
				string = string + word + ' '

		tweets.append(string)
		line = file.readline()

	return tweets

def tokenize_tweets(tweets):
	tokenized_tweets = []
	for tweet in tweets:
		doc = nlp(tweet)
		if len(doc.ents) > 0:
			tokenized_tweets.append(doc)

	for i, t in enumerate(tokenized_tweets):
		print(i, ":", t)
		for x in t.ents:
			print('\t', x.text, x.label_)
		print()

	return tokenized_tweets

if __name__ == '__main__':
	tweets_loc = r'.\datasets\reference\tweets_1.txt'

	tweets = read_tweets(tweets_loc)

	tokenized_tweets = tokenize_tweets(tweets)