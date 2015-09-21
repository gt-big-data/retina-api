from bson import json_util
from dbco import *
from flask import Flask, request
import json, pymongo, time
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/article/lasthours/<hours>')
def getLastHoursArticles(hours):
    timestamp = time.time()- int(hours)*60*60
    articles = db.qdoc.find({'timestamp': {'$gte': timestamp}}).limit(10000)
    articleList = list(articles)
    articleReturn = []
    for a in articleList:
	top = ''
	if 'topic' in a:
		top = a['topic']
        articleReturn.append({'title': a['title'], 'timestamp': a['timestamp'],  'keywords': a['keywords'], 'topic': top, 'source': a['source']})
    return json.dumps(articleReturn, default=json_util.default)

@app.route('/articles/:id')
def getArticleById(id):
    """ Get an article by its id."""
    pass

@app.route('/articles/sources')
def getSourcesList():
    """ Get a list of all the sources """
    pass

@app.route('/articles/keywords')
def getArticlesWithKeywords():
    """
    Get articles who share at least one keyword with one of the keywords
        provided in the params.

        Params:
            keywords (list<str>):
                list of keywords to match
    """
    pass

@app.route('/user')
def getUser():
    """
    Get a users info (blocked until we get facebook login working on flask)

    Params:
        userId
    """
    pass

@app.route('/articles/timeline/:keyword')
def getTimeSeriesData(keyword):
    """
    Get the frequency distribution of articles that contain the keyword. The
    start and end date will most likely be request parameters.
    """
    pass

def main():
    app.debug=True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
