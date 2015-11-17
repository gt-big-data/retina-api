from dbco import *
import flask, json, pymongo, time
from flask import Flask, request
from flask.ext.cors import CORS
from bson import json_util
from getArticles import *
from getKeywords import *
from getTweets import *
from getTimeline import *
from getTopics import *
from getGraph import *
from TweetsGraph import *

from jsonify import *

app = Flask(__name__)
CORS(app)
@app.route('/')
@app.route('/docs')
@app.errorhandler(404)
def documentation(e=1):
    return flask.render_template('doc.html')

@app.route('/article/recent/<int:page>')
@app.route('/article/recent/page/<int:page>')
@app.route('/article/recent/page/<page>/perPage/<perPage>')
def getRecentArticlesByPage(page, perPage=20):
    articleList = recentArticlesByPage(page, 20)
    return jsonify(articleList)

@app.route('/article/id/<articleId>')
def getArticleById(articleId):
    return jsonify(articleById(articleId))


@app.route('/article/lasthours/<hours>')
def getLastHoursArticles(hours):
    return jsonify(articlesXHours(hours))

@app.route('/article/sources')
def getSourcesList(): #Get a list of all the sources
    return jsonify(db.qdoc.distinct('source'))

@app.route('/article/source/<source>/limit/<limit>')
def getRecentFromSource(source, limit): #Get <limit> most recent articles from source <source>
    return jsonify(getArticlesFromSource(source, limit))

@app.route('/article/keywords/<keywords>')
def getArticlesWithKeywords(keywords): #Get articles who share at least one keyword with one of the keywords provided in the params.
    keywords = keywords.split(',')
    return jsonify(articlesWithKeywords(keywords))

@app.route('/article/timeline/<keyword>/days/<days>')
def keywordTimeline(keyword, days):
    return jsonify(getKeywordTimeline(keyword, days))

@app.route('/article/graph/start/<start>/end/<end>')
def daterangeGraph(start, end):
    return jsonify(dateRangeGraph(start, end))

@app.route('/topic/largest/days/<days>/limit/<limit>')
def getLargestTopics(days, limit):
    return jsonify(largestTopics(days, limit))

@app.route('/topic/largestTimelines/days/<days>/limit/<limit>')
def getLargestTopicsTimelines(days, limit):
    return jsonify(largestTopicsTimelines(days, limit))

@app.route('/topic/timeline/<topic>')
def getTopicTimeline(topic):
    return jsonify(topicTimeline(topic))

@app.route('/topic/graph/<date>')
def getDateGraph(date):
    return jsonify(dateGraph(date))

@app.route('/topic/tweet')
def getTweetsGraph():
    return jsonify(buildNodesAndEdges())

@app.route('/trending')
def trendingKeywords():
    return jsonify(getTrendingKeywords())


@app.route('/cokeywords/<keyword>')
def cokeywords(keyword):
    return jsonify(getCoKeywords(keyword))

@app.route('/tweet/start/<start>/end/<end>')
def getTweets(start, end):
    return jsonify(loadTweets(start, end))

@app.route('/tweet/timeline/<keyword>/days/<days>')
def keywordTweetTimeline(keyword, days):
    return jsonify(getKeywordTweetTimeline(keyword, days))

def main():
    app.debug=True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()