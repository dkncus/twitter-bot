import tweepy
from NE_Frequency import NE_Frequency
from Headline_Gen import Headline_Gen
import random
import selenium
from selenium import webdriver
import re
import urllib.request
import os, shutil
import json

TAG_TYPES = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL']

try:
	accessfile = open('./access_keys/keys.txt')
except:
	print("No access keys available to be read.")

CONSUMER_KEY = accessfile.readline().rstrip('\n')
CONSUMER_SECRET = accessfile.readline().rstrip('\n')
ACCESS_TOKEN = accessfile.readline().rstrip('\n')
ACCESS_TOKEN_SECRET = accessfile.readline().rstrip('\n')

SITE_ADDRESSES = ["https://bit.ly/2YKAK5d", "https://bit.ly/3hFqkwg", "https://bit.ly/2UUvvij", "https://bit.ly/2ABojAT", "https://bit.ly/3eg9sKA"]

#Where-on-Earth ID number for the United States
US_WOEID = 23424977

headlines = []
norps_common = []
gpes_common = []
cardinals_common = []
ordinals_common = []
orgs_common = []
money_common = []
date_common = []
headers_common = []

hashtags_common = ['#BREAKING', '#NEWS', '#BREAKINGNEWS']

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

def init_datasets():
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

	return headlines, norps_common, gpes_common, cardinals_common, ordinals_common, orgs_common, money_common, date_common, headers_common

def authenticate():
	#Create Twitter Authorization
	print("Initiating Connection to Twitter API...")
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
	api = tweepy.API(auth)
	print("Connection Successful!\n")

	return api

def delete_all(api):
	for status in tweepy.Cursor(api.user_timeline).items():
		try:
			api.destroy_status(status.id)
			print("Deleted:", status.id)
		except:
			print("Failed to delete:", status.id)

	print("All tweets deleted.")

def get_google_image(search_string):
	#https://www.google.com/search?q=<SEARCH QUERY HERE>&tbm=isch&tbs=sur%3Af
	#https://www.google.com/search?		q=hello  &tbm=isch  &tbs=sur%3Af
									#    Query	  image 	 lisencing 	
	words = search_string.split()
	string = ""
	for i, word in enumerate(words):
		if i == len(words) - 1:
			string += word.lower().rstrip(',')
		else:
			string += word.lower().rstrip(',') + '%20'

	url_string = 'https://www.google.com/search?q=' + string + '&tbm=isch' + '&tbs=isz%3Am%2Csur%3Af'

	print(url_string)

	#Prep selenium options
	options = selenium.webdriver.chrome.options.Options()
	options.headless = True

	#Open instance of chrome with Selenium, searching based on parameters
	DRIVER_PATH = 'C:/bin/chromedriver.exe'
	driver = webdriver.Chrome(options = options, executable_path=DRIVER_PATH)
	driver.get(url_string)
	lines = driver.page_source.splitlines()

	#Harvest image links from search page
	image_links = []
	for line in lines:
		if ('.jpg"' in line) and "</script>" not in line:
			line = re.search(r"(?P<url>https?://[^\s]+)", line).group("url")
			image_links.append(line[:(line.find('"'))])
	driver.quit()

	#download image
	try:
		if len(image_links) == 0:
			print("No images found, using default image")
			shutil.copy('./images/rep_img/default.jpg', "./images/image.jpg")
		else:
			urllib.request.urlretrieve(image_links[0], "./images/image.jpg")
			print("URLlib request successful:", image_links[0])
	except:
		try:
			urllib.request.urlretrieve(image_links[1], "./images/image.jpg")
			print("URLlib request successful:", image_links[1])
		except:
			try:
				urllib.request.urlretrieve(image_links[2], "./images/image.jpg")
				print("URLlib request successful:", image_links[2])
			except:
				print("URLlib Request Failed, using default image")
				shutil.copy('./images/rep_img/default.jpg', "./images/image.jpg")

def get_trends(api, woeid):
	string = api.trends_place(woeid)
	trends = []
	for trend in string[0]['trends']:
		trends.append(trend['name'])

	return trends

def get_tweets_from_trends(trends, api, num_tweets):
	name_mentions = {}

	tweets_set = []

	for query in trends:
		#Filter out retweets if needed
		query = query + ' -filter:retweets'

		#Search for the tweets of a given trend
		tweets = tweepy.Cursor(api.search, q = query, lang="en", tweet_mode='extended').items(num_tweets)

		for tweet in tweets:
			#tweet_text = tweet.full_text
			tweets_set.append(tweet)
			#Check if a mention occurs in the tweet, get all mentions if so
			users = tweet.entities['user_mentions']
			for user in users:
				if user['screen_name'] in name_mentions:
					num_mentions = name_mentions[user['screen_name']][1] + 1
					name_mentions[user['screen_name']] = [user['name'], num_mentions]
				else:
					name_mentions[user['screen_name']] = [user['name'], 1]

	return tweets_set, name_mentions

def generate_tweet():
	index = random.randint(0, len(headlines) - 1)
	body = fill_spaces(headlines[index], ne)
	
	header = headers_common[random.randint(0, len(headers_common) - 1)]

	tweet = ""
	hashtags = random.sample(hashtags_common, k=3)

	if header == "":
		tweet = body + '\n\n' + '>> ' + SITE_ADDRESSES[random.randint(0, 4)] + ' <<' + '\n' + hashtags[0] + " " + hashtags[1] + " " + hashtags[2]
	else:
		tweet = header + " " + body + '\n\n' + header.rstrip(":") + ' NOW >> ' + SITE_ADDRESSES[random.randint(0, 4)] + ' <<' + '\n' + hashtags[0] + " " + hashtags[1] + " " + hashtags[2]

	return body, tweet

if __name__ == '__main__':
	#Initialize datasets (e.g. headlines, norp_common, etc.)
	headlines, norps_common, gpes_common, cardinals_common, ordinals_common, orgs_common, money_common, date_common, headers_common = init_datasets()

	#Initiate connection to Twitter
	api = authenticate()

	print("Getting current trend data...")
	trends = get_trends(api, US_WOEID)

	print("Getting tweets from list of current trending topics...")
	tweets, mentions = get_tweets_from_trends(trends = trends[:20], api = api, num_tweets = 10)

	tweets_text = []
	for tweet in tweets:
		tweets_text.append(tweet.full_text)

	print("TRENDING TOPICS")
	for topic in trends:
		print('\t', topic)

	for topic in trends:
		if '#' in topic:
			hashtags_common.append(topic)

	print("Generating named entity frequency map")
	ne = NE_Frequency(plaintext_tweets = tweets_text)

	ne.print_freq_map(threshold_value = 2)
	
	#Post several tweets
	for i in range(12):
		#Generate actual tweet text
		print("Generating tweet...")
		body, tweet = generate_tweet()

		#Generate related image
		print("Getting image related to '", body, "'...")
		get_google_image(body)
		res = api.media_upload('./images/image.jpg')
		media_id = [res.media_id]

		#Post the actual tweet
		print("Posting tweet...")
		api.update_status(status = tweet, media_ids = media_id)

		#Reset the images
		os.remove("./images/image.jpg")

		print("Tweet posted:\n", tweet)
		print()