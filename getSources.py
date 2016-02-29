from dbco import *

def fullList():
	return list(db.feed.find({}).sort([['active', 1], ['crawlFreq', 1]]))