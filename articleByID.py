from bson.objectid import ObjectId
from bson import json_util
from dbco import *
import json

def getArticleById(articleId):
    articles = db.qdoc.find({'_id': ObjectId(articleId)})
    articles = list(articles)
    return json.dumps(articles[0], default=json_util.default)
# print getArticleById("55f02653a6b867b094a58f1e") 