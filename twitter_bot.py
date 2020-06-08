import tweepy

#Get most common trending hashtags over last 30 mins
#Tag top 3 in the body of our tweet

#Use common words on twitter to build text embedding model

#Get the text language from those tweets

#Generate text embedding model from that language data

#Start the tweet with 'READ:', 'WATCH:', 'LISTEN:', etc. 
#Post tweet with https://bit.ly link

if __name__ == '__main__':
	auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
	auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET") 

	api = tweepy.API(auth)

	api.update_status("Hello Tweepy")