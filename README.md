# GeoTweetsZA
The goal if this python app to geolocate and visualize on a web map where Tweets with particular words/phrases are being tweeted from withing the geographical bounds of South Africa. The Tweepy package and GoogleMaps API were used to achive this outcome.

## Running GeoTweetsZA locally

GeoTweetsZA requires that python 3 be installed on the machine it runs on.

To utilize GeoTweetsZA on your machine, clone this repository or download the Zip file and unzip the contents in a folder on your machine.

Some libraries have to be installed first, to ensure that they are installed on you machine. Open the command line terminal in the directory where the repo has been cloned or unzipped and enter this command:

```bash
pip install -r requirements.txt
```

To run the app enter this command in the command line editor:
```bash
python3 GeoTweetsZA.py
```

or run it in your favourite IDE.

In the terminal window, you will be asked to enter a word to search on Twitter and geolocate.
Press ENTER after typing the word and all the tweets that contain that word will appear on the terminal screen.
After a few seconds your default web browser will open and a web map visualizing the locations of the user provided locations of all the tweets will appear. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
