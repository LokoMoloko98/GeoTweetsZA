import tweepy
import configparser
import pandas as pd
import time

# read credentials from config file
config = configparser.ConfigParser()
config.read("config.ini")

#place credentials in variables
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret  = config['twitter']['access_token_secret']

#authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tick_insertion = time.perf_counter()
places = api.search_geo(query="profile country: South Africa",granularity="country")
place_id = places[0].id
nsfas_tweets = list(tweepy.Cursor(api.search_tweets, q ="(PSG) place:%s" % place_id).items(20))
tock_insertion = time.perf_counter()
insertiontime = f"{tock_insertion - tick_insertion:0.10f} seconds"
print("Processing time =", insertiontime)

columns = ['Tweet', 'Location']
data = []

for tweet in nsfas_tweets:
	data.append([tweet.text, tweet.user.location])
	df = pd.DataFrame(data, columns=columns)

print(df)