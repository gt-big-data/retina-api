from dbco import *
import flask, json, pymongo, time, logger
from flask import Flask, request
from flask.ext.cors import CORS
import getArticle, getTweets, getKeywords, getSources
import getTimeline, getGraph, getTopics
from jsonify import *
from favicon import *

app = Flask(__name__)
CORS(app)

@app.before_request
def log_request():
    logger.log(flask.request)

@app.route('/')
@app.route('/docs')
@app.errorhandler(404)
def documentation(e=1):
    return flask.render_template('doc.html')
@app.route('/manageFeeds')
def manageFeeds():
    return flask.render_template('manage.html')
@app.route('/article/recent/<int:page>')
@app.route('/article/recent/page/<int:page>')
@app.route('/article/recent/page/<page>/perPage/<perPage>')
def getRecentArticlesByPage(page, perPage=20):
    return jsonify(getArticle.recentByPage(page, 20))

@app.route('/article/id/<articleId>')
def getArticleById(articleId):
    return jsonify(getArticle.byId(articleId))

@app.route('/article/lasthours/<hours>')
def getLastHoursArticles(hours):
    return jsonify(getArticle.byHours(hours))

@app.route('/article/sources')
def getSourcesList(): #Get a list of all the sources
    return jsonify(db.qdoc.distinct('source'))

@app.route('/article/feeds')
def getFeeds(): #Get a list of all the sources
    return jsonify(getSources.fullList())

@app.route('/feed/updateStatus/<status>')
def feedUpdateStatus(status): #Get a list of all the sources
    return getFeeds()

@app.route('/sources/timeline')
def getSourcesTimeline(): #Get a timeline for a specific source
    return jsonify(getTimeline.allSources())

@app.route('/source/<source>/timeline')
def getSourceTimeline(source): #Get a timeline for a specific source
    return jsonify(sourceTimeline(source))

@app.route('/article/source/<source>/limit/<limit>')
def getRecentFromSource(source, limit): #Get <limit> most recent articles from source <source>
    return jsonify(getArticle.recentBySource(source, limit))

@app.route('/article/keywords/<keywords>')
def getArticlesWithKeywords(keywords): #Get articles who share at least one keyword with one of the keywords provided in the params.
    keywords = keywords.split(',')
    return jsonify(articlesWithKeywords(keywords))

@app.route('/article/timeline/<keyword>/days/<days>')
def keywordTimeline(keyword, days):
    return jsonify(getTimeline.byKeyword(keyword, days))

@app.route('/article/kwgraph/start/<start>/end/<end>')
def daterangeGraph(start, end):
    return jsonify(getGraph.kwGraph(start, end))

@app.route('/article/entgraph/start/<start>/end/<end>')
def daterangeGraphKw(start, end):
    return jsonify(getGraph.kwGraph(start, end))

@app.route('/topic/largest/days/<days>/limit/<limit>')
def getLargestTopicsEnt(days, limit):
    return jsonify(getTopics.bySize(days, limit))

@app.route('/topic/largestTimelines/days/<days>/limit/<limit>')
def getLargestTopicsTimelines(days, limit):
    fullObject = [{'name': t['name'], 'topic': t['_id'], 'timeline': getTimeline.byTopic(t['_id'])} for t in getTopics.bySize(days, limit)]
    return jsonify(fullObject)

@app.route('/topic/timeline/<topic>')
def getTopicTimeline(topic):
    return jsonify(getTimeline.byTopic(topic))

@app.route('/favicon/<source>')
def getFavicon(source):
    return get_favicon(source)

@app.route('/trending')
def trendingKeywords():
    return jsonify(getKeywords.byTrending())

@app.route('/cokeywords/<keyword>')
def cokeywords(keyword):
    return jsonify(getKeywords.coKw(keyword))

@app.route('/tweet/start/<start>/end/<end>')
def getTweets(start, end):
    return jsonify(getTweets.byTimerange(start, end))

@app.route('/tweet/timeline/<keyword>/days/<days>')
def keywordTweetTimeline(keyword, days):
    return jsonify(getKeywordTweetTimeline(keyword, days))

def main():
    app.run(host='0.0.0.0', port=4000) #, debug=True

if __name__ == '__main__':
    main()