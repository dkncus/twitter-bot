import tweepy
from NE_Frequency import NE_Frequency
import random
import selenium
from selenium import webdriver
import re
import urllib.request
import os, shutil
import math
import threading

TAG_TYPES = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL']

try:
	accessfile = open('./access_keys/keys.txt')
except:
	print("No access keys available to be read.")
	print("You may need a Twitter Developer account to gain access.")
	print("If you already have a Developer Account, do the following:")
	print("\t1. Go to your app - https://developer.twitter.com/apps/<YOUR APP ID HERE>/")
	print("\t2. Navigate to 'Keys and Tokens'.")
	print("\t3. From the 'Consumer API keys', copy both values, and paste them onto their own lines in a blank .txt file.")
	print("\t4. Generate Access tokens, copy both values, and paste them into onto their own lines under the Consumer API in the .txt file.")
	print("\t5. Create a new directory in the same folder as twitter_bot.py named '/access_keys/'.")
	print("\t6. Save the .txt file in the '/access_keys/' directory, named 'keys.txt'.")
	print("\t7. Run the program again. :)")
	quit()

CONSUMER_KEY = accessfile.readline().rstrip('\n')
CONSUMER_SECRET = accessfile.readline().rstrip('\n')
ACCESS_TOKEN = accessfile.readline().rstrip('\n')
ACCESS_TOKEN_SECRET = accessfile.readline().rstrip('\n')

SITE_ADDRESSES = ["https://bit.ly/2YKAK5d", "https://bit.ly/3hFqkwg", "https://bit.ly/2UUvvij", "https://bit.ly/2ABojAT", "https://bit.ly/3eg9sKA"]

#Where-on-Earth ID number for the United States
US_WOEID = 23424977

headlines = []

data_sets = {'WORK_OF_ART' : [], 'LAW' : [], 'LANGUAGE' : [], 'TIME' : [], 'PERCENT' : [], 'MONEY' : [], 'CARDINAL' : [], 'ORDINAL' :[]}

#Fills in the spaces of given tags in a fillable news headline
def fill_spaces(fillable, common_ne):
	#Generate probabilistic frequency map from Logistic function
	frequency_map = logistic_replace(common_ne.frequency_map)

	#iterate through the list of tags for each in the given 
	for tag in TAG_TYPES:
		if tag in fillable:
			occurances = fillable.count(tag)
			for i in range(occurances):
				if tag == 'NORP' or tag == 'GPE' or tag == 'PERSON' or tag == 'ORG' or tag == 'EVENT' or tag == 'FAC' or tag == 'LOC' or tag == 'PRODUCT' or tag == 'DATE':
					replacement = get_probable_fillable(frequency_map_sigmoid = frequency_map, tag = tag)
					fillable = fillable.replace(tag, replacement, 1)
				else:
					replacement = data_sets[tag][random.randint(0, len(data_sets[tag]) - 1)]
					fillable = fillable.replace(tag, replacement, 1)

	fillable = fillable[0].upper() + fillable[1:len(fillable)]
	return fillable

#Generate probability word will be selected based on its frequency on twitter
def logistic_replace(frequency_map):
	for tag in frequency_map:
		max_value = frequency_map[tag][0][1]
		for i, entity in enumerate(frequency_map[tag]):
			x = entity[1]/max_value #input to the function, between 0 and 1 (bounded)
			fx = 0.5 / ( 1 + math.exp( -25 * ( x - 0.5 ) ) ) #Logistic Function of Probability based on Frequency
			frequency_map[tag][i] = (entity[0], fx)

	return frequency_map

#Get the probable filible after the signmoid curve has been applied to the set
def get_probable_fillable(frequency_map_sigmoid, tag):
	population = []
	weights = []

	for entity in frequency_map_sigmoid[tag]:
		population.append(entity[0])
		weights.append(entity[1])

	if len(population) == 0:
		return 'thing'
	
	c = random.choices(population = population, weights = weights, k=1)
	return c[0]

#Load data into a list from a text file
def load_data(location):
	tmp = []
	file = open(location)
	line = file.readline()

	while line:
		tmp.append(line.rstrip('\n'))
		line = file.readline()

	return tmp

#Initialize the datasets (e.g. NORP_Common, etc.)
def init_datasets():
	#Generates headlines with mad-lib-esque cut out Named Entities
	print("Loading headlines for substitution...")
	headlines = load_data(r'.\datasets\fillable_headlines.txt')

	print("Loading header data...")
	headers_common = load_data('./datasets/modifiers/header.txt')

	#Initialize Common Replacements from .txt datasets
	print("Loading common replacements...")
	data_sets['WORK_OF_ART'] = load_data('./datasets/tag_replacements/work_of_art/work_of_art_common.txt')
	data_sets['LAW'] = load_data('./datasets/tag_replacements/law/law_common.txt')
	data_sets['LANGUAGE'] = load_data('./datasets/tag_replacements/language/language_common.txt')
	data_sets['TIME'] = load_data('./datasets/tag_replacements/time/time_common.txt')
	data_sets['PERCENT'] = ['83%']
	data_sets['CARDINAL'] = load_data('./datasets/tag_replacements/cardinal/cardinal.txt')
	data_sets['ORDINAL'] = load_data('./datasets/tag_replacements/ordinal/ordinal.txt')
	data_sets['MONEY']= load_data('./datasets/tag_replacements/money/money.txt')

	print("Initialization Completed.\n")

	return headlines, headers_common

#Authenticate the user to the Twitter API, return the API object
def authenticate():
	#Create Twitter Authorization
	print("Initiating Connection to Twitter API...")
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
	api = tweepy.API(auth)
	print("Connection Successful!\n")

	return api

#DELETE ALL TWEETS (Self-destruct button)
def delete_all(api):
	for status in tweepy.Cursor(api.user_timeline).items():
		try:
			api.destroy_status(status.id)
			print("Deleted:", status.id)
		except:
			print("Failed to delete:", status.id)

	print("All tweets deleted.")

#Get a non-copyright Google image from a search string
def get_google_image(search_string):
	#https://www.google.com/search?q=<SEARCH QUERY HERE>&tbm=isch&tbs=sur%3Af
	#https://www.google.com/search?		q=hello  &tbm=isch  &tbs=sur%3Af
									#    Query	  image 	 lisencing 

	print("Getting image related to '", search_string, "'...")
	words = search_string.split()
	string = ""
	for i, word in enumerate(words):
		if i == len(words) - 1:
			string += word.lower().rstrip(',')
		else:
			string += word.lower().rstrip(',') + '%20'

	url_string = 'https://www.google.com/search?q=' + string + '&tbm=isch' + '&tbs=isz%3Am%2Csur%3Af'

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

#Get the trending topics of a particular WOEID (Where on Earth ID) at the current moment
def get_trends(api, woeid):
	print("Getting current trend data...")
	string = api.trends_place(woeid)
	trends = []
	for trend in string[0]['trends']:
		trends.append(trend['name'])

	return trends

#Get tweets corresponding to a set of trending topics
def get_tweets_from_trends(trends, api, num_tweets):
	print("Getting tweets from list of current trending topics...")

	#Mentions that will be returned and later factored into the PERSON tag in the NE frequency map
	name_mentions = {}

	#Set of tweet objects
	tweets_set = []

	for query in trends:
		#Filter out retweets if needed
		query = query + ' -filter:retweets'

		#Search for the tweets of a given trend
		tweets = tweepy.Cursor(api.search, q = query, lang='en', tweet_mode='extended').items(num_tweets)

		#For each tweet in the returned tweets from tweepy.Cursor
		for tweet in tweets:
			#tweet_text = tweet.full_text
			tweets_set.append(tweet)
			#Check if a mention occurs in the tweet, get all mentions if so
			users = tweet.entities['user_mentions']
			for user in users:	#Add those mentions to the set of name mentions
				if user['screen_name'] in name_mentions:
					num_mentions = name_mentions[user['screen_name']][1] + 1
					name_mentions[user['screen_name']] = [user['name'], num_mentions]
				else:
					name_mentions[user['screen_name']] = [user['name'], 1]

	return tweets_set, name_mentions

#Create the text of a tweet
def generate_tweet(common_ne, hashtags_common):
	print("Generating tweet...")
	index = random.randint(0, len(headlines) - 1)
	body = fill_spaces(headlines[index], common_ne)
	
	header = headers_common[random.randint(0, len(headers_common) - 1)]

	tweet = ""
	hashtags = random.sample(hashtags_common, k=3)

	if header == "":
		tweet = body + '\n\n' + '>> ' + SITE_ADDRESSES[random.randint(0, 4)] + ' <<' + '\n' + hashtags[0] + " " + hashtags[1] + " " + hashtags[2]
	else:
		tweet = header + " " + body + '\n\n >> ' + SITE_ADDRESSES[random.randint(0, 4)] + ' <<' + '\n' + hashtags[0] + " " + hashtags[1] + " " + hashtags[2]

	return body, tweet

def write_and_post_tweet(api, tweets_per_topic = 40, total_trends = 40, hashtags_common = ['#BREAKING', '#NEWS', '#BREAKINGNEWS'], timed = True, interval = 900.0):
	#Start the next posting in 15 minutes if the timed toggle is on
	if timed:
		print("Starting timer for", interval, "s. before next tweet posted.")
		threading.Timer(interval, write_and_post_tweet, [api]).start()

	#Print out current trending topics, append hashtags
	trends = get_trends(api, US_WOEID)
	print("TRENDING TOPICS")
	for i, topic in enumerate(trends):
		if '#' in topic and i < 11:
			hashtags_common.append(topic)
		if i <= 15:
			print('\t', i, ':', topic)
	print('\t...')

	#Clamp trends to only 40 total, remove filler hashtags if necessary
	if len(trends) > total_trends:
		trends = trends[:total_trends]
	if len(hashtags_common) >= 6:
		hashtags_common = hashtags_common[3:]

	#Fetch the top 40 tweets from all the currently trending topics
	tweets, mentions = get_tweets_from_trends(trends = trends, api = api, num_tweets = tweets_per_topic)
	tweets_text = []
	for tweet in tweets:
		tweets_text.append(tweet.full_text)

	print("Generating named entity frequency map...")
	ne = NE_Frequency(plaintext_tweets = tweets_text)

	#Generate actual tweet text
	body, tweet = generate_tweet(common_ne = ne, hashtags_common = hashtags_common)

	#Generate related image
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
	return 0

if __name__ == '__main__':
	#Initialize datasets (e.g. headlines, norp_common, etc.)
	headlines, headers_common = init_datasets()

	#Initiate connection to Twitter
	api = authenticate()

	#Actual creation and posting of tweet at Post_Offset intervals
	status = write_and_post_tweet(api = api)