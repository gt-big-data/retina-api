from bson import json_util
from dbco import *
from flask import Flask
import json
import pymongo

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ask')
def getRecentArticles():
    articles = list(db.qdoc.find().sort('timestamp', pymongo.DESCENDING).limit(50))
    for article in articles:
        article['_id'] = str(article['_id'])
    return json.dumps(articles, default=json_util.default)

def main():
    app.run(host='0.0.0.0', port=5000)
   
if __name__ == '__main__':
    main()
