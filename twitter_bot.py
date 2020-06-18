import tweepy
from NE_Frequency import NE_Frequency
from Headline_Gen import Headline_Gen
import random

TAG_TYPES = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL']

accessfile = open('./access_keys/keys.txt')
CONSUMER_KEY = accessfile.readline().rstrip('\n')
CONSUMER_SECRET = accessfile.readline().rstrip('\n')
ACCESS_TOKEN = accessfile.readline().rstrip('\n')
ACCESS_TOKEN_SECRET = accessfile.readline().rstrip('\n')

SITE_ADDRESSES = ["https://bit.ly/2YKAK5d", "https://bit.ly/3hFqkwg", "https://bit.ly/2UUvvij", "https://bit.ly/2ABojAT", "https://bit.ly/3eg9sKA"]

norps_common = []
gpes_common = []
cardinals_common = []
ordinals_common = []
orgs_common = []
money_common = []
date_common = []
headers_common = []

def fill_spaces(fillable, common_ne):
	#print(fillable)

	#iterate through the list of tags for each in the given 
	for tag in TAG_TYPES:
		if tag in fillable:
			occurances = fillable.count(tag)
			for i in range(occurances):
				if tag == 'NORP':
					index = random.randint(0, len(norps_common) - 1)
					fillable = fillable.replace(tag, norps_common[index], 1)
				elif tag == 'GPE':
					index = random.randint(0, len(gpes_common) - 1)
					fillable = fillable.replace(tag, gpes_common[index], 1)
				elif tag == 'CARDINAL':
					index = random.randint(0, len(cardinals_common) - 1)
					fillable = fillable.replace(tag, cardinals_common[index], 1)
				elif tag == 'ORDINAL':
					index = random.randint(0, len(ordinals_common) - 1)
					fillable = fillable.replace(tag, ordinals_common[index], 1)
				elif tag == 'ORG':
					r = random.randint(0, 10)
					if r <= 4:
						index = random.randint(0, len(orgs_common) - 1)
						fillable = fillable.replace(tag, orgs_common[index], 1)
					else:
						index = random.randint(0, int((len(common_ne.frequency_map[tag]) - 1) * 0.1))
						fillable = fillable.replace(tag, common_ne.frequency_map[tag][index][0], 1)
				elif tag == 'PERCENT':
					fillable = fillable.replace(tag, '83%', 1)
				elif tag == 'DATE':
					if 'die' in fillable or 'pass' in fillable:
						fillable = fillable.replace(tag, 'age ' + str(random.randint(50, 110)), 1)
					else:
						index = random.randint(0, len(date_common) - 1)
						fillable = fillable.replace(tag, date_common[index], 1)
				elif tag == 'MONEY':
					index = random.randint(0, len(money_common) - 1)
					fillable = fillable.replace(tag, money_common[index], 1)
				else:
					index = random.randint(0, len(common_ne.frequency_map[tag]) - 1)
					fillable = fillable.replace(tag, common_ne.frequency_map[tag][index][0], 1)

	fillable = fillable[0].upper() + fillable[1:len(fillable)]
	return fillable

def load_data(location):
	tmp = []
	file = open(location)
	line = file.readline()

	while line:
		tmp.append(line.rstrip('\n'))
		line = file.readline()

	return tmp

def generate_tweet():
	body = fill_spaces(headlines[random.randint(0, len(headlines) - 1)], ne)
	
	header = headers_common[random.randint(0, len(headers_common) - 1)]

	tweet = ""

	if header == "":
		tweet = body + ': ' + SITE_ADDRESSES[random.randint(0, 4)]
	else:
		tweet = header + " " + body + ': ' + SITE_ADDRESSES[random.randint(0, 4)]

	return tweet

if __name__ == '__main__':
	#Stores the frequency of Named Entities
	print("Initializing Named Entity Frequency Map...")
	ne = NE_Frequency(tweet_data_loc = r'.\datasets\reference\tweets_1.txt')

	#Generates headlines with mad-lib-esque cut out Named Entities
	print("Loading headlines for substitution...")
	headlines = load_data(r'.\datasets\fillable_headlines.txt')

	#Initialize Common Replacements from .txt datasets
	print("Loading common replacements...")
	norps_common = load_data('./datasets/tag_replacements/norp/norp_combined.txt')
	gpes_common = load_data('./datasets/tag_replacements/gpe/gpe_combined.txt')
	cardinals_common = load_data('./datasets/tag_replacements/cardinal/cardinal.txt')
	ordinals_common = load_data('./datasets/tag_replacements/ordinal/ordinal.txt')
	orgs_common = load_data('./datasets/tag_replacements/org/org_companies.txt')
	money_common = load_data('./datasets/tag_replacements/money/money.txt')
	date_common = load_data('./datasets/tag_replacements/date/date.txt')
	headers_common = load_data('./datasets/modifiers/header.txt')
	print("Initialization Completed.\n")
	
	#Create Twitter Authorization
	print("Initiating Connection to Twitter API...")
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
	api = tweepy.API(auth)
	print("Connection Successful!\n")

	#api.update_status(status = generate_tweet())

	data = api.get_status(generate_tweet)
	print(data)
	#Delete ALL TWEETS from timeline
	'''
	for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
                print("Deleted:", status.id)
            except:
                print("Failed to delete:", status.id)
    ''' 