from bson.objectid import ObjectId
from bson import json_util
from dbco import *
from datetime import datetime, timedelta
import json

def byId(articleId):
	return db.qdoc.find_one({'_id': ObjectId(articleId)})

def byHours(hours):
	gte = datetime.utcnow()-timedelta(hours=int(hours))
	return list(db.qdoc.find({'timestamp': {'$gte': gte}}).limit(1000))

def byKeywords(keywordsInput):
	return list(db.qdoc.find({'keywords' : { "$in" : keywordsInput}}).limit(2000))

def recentByPage(page, perPage):
	page = int(page); perPage = int(perPage)
	return list(db.qdoc.find(projection={'content': False}).sort('timestamp', -1).limit(perPage).skip((page - 1) * perPage))

def recentBySource(source, limit):
	return list(db.qdoc.find({'source':source}).sort('timestamp', -1).limit(int(limit)))

if __name__ == "__main__":
	print getArticleById("55f02653a6b867b094a58f1e")