from bson import json_util
from dbco import *
from flask import Flask, request
import json
import pymongo

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/article/recent/<limit>')
def getRecentArticles(limit):
    limit = min(int(limit), 1000)
    articles = db.qdoc.find().sort('timestamp', pymongo.DESCENDING).limit(limit)
    articleList = list(articles)
    for article in articleList:
        article['_id'] = str(article['_id'])
    return json.dumps(articleList, default=json_util.default)

def main():
    app.debug=True
    app.run(host='0.0.0.0', port=5000)
   
if __name__ == '__main__':
    main()
