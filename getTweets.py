from dbco import *
from bson import json_util
import time, re, json

def loadTweets(start, end):
	start = int(start); end = int(end);
	return list(db.tweet.find({'timestamp': {'$gte': start, '$lte': end}}))