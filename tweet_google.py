import tweepy
import configparser
import pandas as pd
import time
import requests
from urllib.parse import urlencode
import json
import folium

# read credentials from config file
# read credentials from config file
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret  = config['twitter']['access_token_secret']

#place credentials in variables
# api_key = "TnNYRUSaBujPtmgV7Raqv78jg"
# api_key_secret = "Bhl5Rlq8tifgwOYUKdnAesoGpLOHV9G7DtTrxWCrRzq9pqjMWLE"
# access_token = "1499667878609571840-yjV5JgZRRLC1pk8iUNiZGNSZJNseHu"
# access_token_secret  = "6SE9lWjGg2lJNj8r6NK1HcvPOZxqv5oMFC7QLPC6n6IBh"

#authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

SearchWord = input("Enter a word to search for: ")
print("Searching for tweet locations")

tick_insertion = time.perf_counter()
places = api.search_geo(query="profile country: South Africa",granularity="country")
place_id = places[0].id
tweets = list(tweepy.Cursor(api.search_tweets, q =f"({SearchWord}) place:{place_id}").items(30))
tock_insertion = time.perf_counter()
insertiontime = f"{tock_insertion - tick_insertion:0.10f} seconds"
print("Processing time =", insertiontime)

columns = ['Tweet', 'Location']
data = []

for tweet in tweets:
    data.append([tweet.text, tweet.user.location])
    df = pd.DataFrame(data, columns=columns)
    print(df)
    df.to_csv('tweets.csv')
    df["LAT"] = None
    df["LON"] = None
    
def extract_lat_lng(address_or_postalcode, components, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": "AIzaSyDn1FXv39nfyZ2mGXtj404nuvAzHQmW2Uk", 'components':components}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

for i in range(0, len(df)):
	geocode_result = extract_lat_lng(df.iat[i,1], {'country':['ZA']})
	try:
		lat = geocode_result[0]
		lon = geocode_result[1]
		df.iat[i, df.columns.get_loc("LAT")] = lat
		df.iat[i, df.columns.get_loc("LON")] = lon

	except:
		lat = None
		lon = None

#e=[]
#for in range(len(df)):
#   df(i)[0]=<34,00 and >=35,00#latide
#    append.df

print(df)

df.to_csv('tweets.csv')

df_geo = df.dropna(subset=["LAT","LON"], axis=0, inplace=False)
print("We have {} geotagged rows".format(len(df_geo)))
print(df_geo.tail())

def df_to_geojson(df, properties, lat='LAT', lon='LON'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson

cols = ['Tweet', 'Location', 'LAT', 'LON']
geojson = df_to_geojson(df_geo, cols)

print()
output_filename = "geotweets.geojson"
with open(output_filename, 'w') as output_file:
    output_file.write('')
    json.dump(geojson, output_file, indent=2)

#######################################################################################################################################################################
m = folium.Map(location = [-28.84467368077178, 25.1806640625], zoom_start=5)
outfp = "TweetMap.html"
    #tooltip = "Tweet"

    #print(lats[2], lons[2])
    #print(pointsmetadata[2][0], pointsmetadata[2][1])
    #print()
    #if len(lats) == len(lons):
for i in range(len(df_geo)):
    folium.Marker([df_geo.iat[i, 2], df_geo.iat[i, 3]], tooltip=f"Phrase to geolocate: {SearchWord} <br> Location: {df_geo.iat[i,1]} <br> Tweet: {df_geo.iat[i,0]}").add_to(m)
    print(f"Just mapped point at {df_geo.iat[i,1]}")

m.save(outfp)


import webbrowser
webbrowser.open_new_tab('TweetMap.html')
print()