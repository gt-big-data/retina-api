import datetime
from bson import json_util
from dbco import *
from flask import Flask, request, jsonify
import json, pymongo, time
from flask.ext.cors import CORS
from articlesWithKeywords import *
from articlesFromSource import *
from articleByID import *
from tweetLoad import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/article/recent/<int:page>')
def getRecentArticles(page):
    items_per_page = request.args.get('limit')
    if items_per_page:
        items_per_page = int(items_per_page)
    else:
        items_per_page = 20
    articles = db.qdoc.find(projection={'content': False}).sort('timestamp', pymongo.DESCENDING).limit(items_per_page).skip((page - 1) * items_per_page)
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

@app.route('/article/id/<articleId>')
def getArticleByIdFunc(articleId):
    return getArticleById(articleId)

@app.route('/article/sources')
def getSourcesList():
    """ Get a list of all the sources """
    sources = db.qdoc.distinct('source')
    return jsonify(data=sources)

@app.route('/article/source/<source>/limit/<limit>')
def getRecentFromSource(source, limit):
    """ Get <limit> most recent articles from source <source> """
    return getArticlesFromSource(source, int(limit))

@app.route('/article/keywords/<keywords>')
def getArticlesWithKeywords(keywords):
    """
    Get articles who share at least one keyword with one of the keywords
        provided in the params.
        Params:
            keywords (list<str>):
                list of keywords to match
    """
    keywords = keywords.split(',')
    return getArticlesWithKeywordsFunc(keywords)

@app.route('/user')
def getUser():
    """
    Get a users info (blocked until we get facebook login working on flask)
    Params:
        userId
    """
    pass

@app.route('/article/timeline/:keyword')
def getTimeSeriesData(keyword):
    """
    Get the frequency distribution of articles that contain the keyword. The
    start and end date will most likely be request parameters.
    """
    pass

@app.route('/trending')
def get_trending_keywords():
    limit = request.args.get('limit')
    today = datetime.datetime.now() - datetime.timedelta(hours=24)
    time_stamp = int(today.strftime('%s'))
    match = {'$match': {'timestamp': {'$gte': time_stamp}}}
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    front_end_compatable = lambda x: {'keyword': x['_id'], 'total': x['total']}
    return jsonify(data=map(front_end_compatable, query_result))

@app.route('/cokeywords')
def get_cokeywords():
    term = request.args.get('keyword')
    today = datetime.datetime.now() - datetime.timedelta(hours=24)
    time_stamp = int(today.strftime('%s'))
    match = {'$match':
                {'timestamp': {'$gte': time_stamp},
                 'keywords': term}
            }
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    front_end_compatable = lambda x: {'keyword': x['_id'], 'total': x['total']}
    data = [front_end_compatable(doc) for doc in query_result if doc['_id'] != term]
    return jsonify(data={'keyword': term, 'children': data})

@app.route('/tweet/delay/<delay>/amount/<amount>')
def getTweets(delay, amount):
    delay = int(delay); amount = int(amount);
    return loadTweets(delay, amount)

def main():
    app.debug=True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
