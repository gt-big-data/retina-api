from bson.objectid import ObjectId
from bson import json_util
from dbco import *
import json, datetime

def articleById(articleId):
    return list(db.qdoc.find({'_id': ObjectId(articleId)}))[0]

def articlesXHours(hours):
    return list(db.qdoc.find({'timestamp': {'$gte': (datetime.datetime.now()-datetime.timedelta(hours=int(hours)))}}))

def articlesWithKeywords(keywordsInput):
    return list(db.qdoc.find({'keywords' : { "$in" : keywordsInput}}).limit(2000))

def recentArticlesByPage(page, perPage):
    page = int(page); perPage = int(perPage)
    return list(db.qdoc.find(projection={'content': False}).sort('timestamp', -1).limit(perPage).skip((page - 1) * perPage))

def getArticlesFromSource(source, limit):
    return list(db.qdoc.find({'source':source}).sort('timestamp', -1).limit(int(limit)))

if __name__ == "__main__":
	print getArticleById("55f02653a6b867b094a58f1e")