from bson.objectid import ObjectId
from bson import json_util
from dbco import *
import json

def articleById(articleId):
    return list(db.qdoc.find({'_id': ObjectId(articleId)}))

def articlesXHours(hours):
    return list(db.qdoc.find({'timestamp': {'$gte': time.time()- int(hours)*60*60}}))

def articlesWithKeywords(keywordsInput):
    return list(db.qdoc.find({'keywords' : { "$in" : keywordsInput}}).limit(2000))

def recentArticlesByPage(page, perPage):
    page = int(page); perPage = int(perPage)
    return list(db.qdoc.find(projection={'content': False}).sort('timestamp', -1).limit(perPage).skip((page - 1) * perPage))

def getArticlesFromSource(source, limit):
    return list(db.qdoc.find({'source':source}).sort('timestamp', -1).limit(int(limit)))

if __name__ == "__main__":
	print getArticleById("55f02653a6b867b094a58f1e")