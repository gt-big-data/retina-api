from dbco import *
from bson import json_util
import time, re, json

def byTimerange(start, end):
	start = int(start); end = int(end);
	return list(db.tweet.find({'timestamp': {'$gte': start, '$lte': end}}).limit(1000))