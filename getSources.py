from dbco import *

def sourceList():
	return list(db.feed.find({}).sort([['active', 1], ['crawlFreq', 1]]))

def changeStatus(feed, status):
	db.feed.update({'feed': feed}, {'$set': {'active': (status!='false')}})