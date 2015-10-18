from dbco import *
from bson import json_util
import time, re, json

def loadTweets(delay, amount):
	delay = int(delay); amount = int(amount);
	return list(db.tweet.find({'timestamp': {'$gte': time.time()-delay, '$lte': time.time()-delay+amount}}))