from nltk.corpus import stopwords
from dbco import *
import time, re, json

def loadTweets(delay, amount):
	articles = list(db.tweet.find({'timestamp': {'$gte': time.time()-delay, '$lte': time.time()-delay+amount}}))
	tweets = [article['text'] for article in articles]

	stopW = set(stopwords.words('english'))
	commW = ['http', 'like', 'ga', 'job', 'love', 'atlanta', 'amp', 'hiring', 'day', 'lol', 'know', 'time', 'want', 'got', 'good', 'shit', 'need', 'people', 'thank', 'today', 'really', 'make', 'careerarc', 'work', 'happy', 'great', 'going', 'nigga', 'think', 'come', 'new', 'life', 'school', 'right', 'll', 'feel', 'look', 'girl', 'night', 'thing', 'man', 'say', 've', 'friend', 'let', 'fuck', 'year', 'best', 'alway', 'way', 'wanna', 'tonight', 'game', 'better', 'birthday', 'mi', 'hate', 'latest', 'ain', 'im', 'tomorrow', 'u', 'gonna', 'home', 'god', 'getting', 'week', 'real', 'guy', 'oh', 'bad', 'sleep', 'morning', 'hope', 'tell', 'gotta', 'opening', 'bitch', 'said', 'click', 'baby', 'wait', 'ready', 'yall', 'boy', 'stop', 'didn', 'lmao', 'ya', 'start', 'damn', 'cause', 'talk', 'retail', 'team', 'follow', 'little', 'clas', 'mean', 'play']
	commW.extend(stopW)
	common_words = set(commW) 

	def remove_non_ascii_1(text):
	    return ''.join(i for i in text if ord(i)<128)

	jsonObj = []

	for tweet in tweets:
		tweetString = re.sub('[()!\.,\?&;]', '', tweet).lower()
		tweetString = remove_non_ascii_1(tweetString)
		tweetString = tweetString.replace('\n', '')
		words = tweetString.split(' ')
		words = [w for w in words if ('http' not in w and len(w) > 0)]
		jsonObj.append({'tweet': tweet, 'keywords': words})

	return json.dumps(jsonObj)