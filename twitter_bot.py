import tweepy
from NE_Frequency import NE_Frequency
from Headline_Gen import Headline_Gen
import random

TAG_TYPES = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL']

file = open('./access_keys/keys.txt')

CONSUMER_KEY = file.readline().rstrip('\n')
CONSUMER_SECRET = file.readline().rstrip('\n')
ACCESS_TOKEN = file.readline().rstrip('\n')
ACCESS_TOKEN_SECRET = file.readline().rstrip('\n')

SITE_ADDRESS = "https://bit.ly/"

def fill_spaces(fillable):
	filled = fillable
	for tag in TAG_TYPES:
		if tag in fillable:
			occurances = fillable.count(tag)
			for i in range(occurances):
				filled.replace(tag, 1, 1)

def load_data(location):
	tmp = []
	file = open(location)
	line = file.readline()

	while line:
		tmp.append(line.rstrip('\n'))
		line = file.readline()

	return tmp

def generate_tweet():
	#Select random news headline with spaCy fillables
	#Fill those fillables
	#Add header tag
	#Add footer hashtags
	#Add footer bit.ly link
	return

if __name__ == '__main__':
	#Stores the frequency of Named Entities
	print("Initializing Named Entity Frequency Map...")
	ne = NE_Frequency(tweet_data_loc = r'.\datasets\reference\tweets_1.txt')

	#Generates headlines with mad-lib-esque cut out Named Entities
	print("Generating headlines for substitution...")
	headline_gen = Headline_Gen(fileloc_dataset = r"datasets\reference\non_clickbait_data.txt")

	print("Initialization Completed.\n")
	print("Initiating Connection to Twitter API...")

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 

	api = tweepy.API(auth)
 	print("Connection Successful!\n")
	for i in range(10):
		article_index = random.randint(0, len(headline_gen.fillable_headlines) - 1)
		a = headline_gen.fillable_headlines[article_index]
		print(a)
		#fill_spaces(a)

	#api.update_status()