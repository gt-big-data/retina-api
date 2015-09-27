import pymongo
from bson import json_util
import json
from dbco import *
from collections import Counter

def getArticlesWithKeywordsFunc(keywordsInput):
    articlesWithKeywords = list(db.qdoc.find(
        {'keywords' : { "$in" : keywordsInput}}).limit(10))
    return json.dumps(articlesWithKeywords, default = json_util.default)
