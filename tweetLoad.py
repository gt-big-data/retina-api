from dbco import *
from bson import json_util
import time, re, json

def loadTweets(delay, amount):
	articles = list(db.tweet.find({'timestamp': {'$gte': time.time()-delay, '$lte': time.time()-delay+amount}}))
	return json.dumps(articles, default=json_util.default)