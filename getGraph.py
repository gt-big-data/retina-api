from dateutil import parser
from dbco import *
import random

def kwGraph(startDate, endDate):
	startDatetime = parser.parse(startDate)
	endDatetime = parser.parse(endDate)
	originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]
	match = {'$match': {'timestamp': {'$gte': startDatetime, '$lte': endDatetime}, 'source': {'$in': originalSources}}}
	proj = {'$project': {'id': '$_id', 'name': '$title', 'group': {'$ifNull': ['$topic', int(500*random.random())]}, 'keywords': 1}}

	nodes = list(db.qdoc.aggregate([match, proj]))
	for n in nodes:
		n['keywords'] = set(n.get('keywords', []))

	edges = []; pageWithEdge = set([])
	for i in range(0,len(nodes)):
		for j in range(i+1,len(nodes)):
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 2:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': nodes[i]['id'], 'target': nodes[j]['id'], 'value': le})
	for n in nodes:
		n['keywords'] = list(n['keywords'])
	return {'nodes': [n for n in nodes if n['id'] in pageWithEdge], 'edges': edges}

def getTweetsToday():
    startTime = time.time() - 3600
    matchTime = {'$match': {'timestamp': {'$gte': startTime}}}
    return list(db.tweet.aggregate([matchTime]))

def numOfSameWords(tweet1, tweet2):
    commonWords = set(tweet1['words']) & set(tweet2['words'])
    return len(commonWords)

def tweetGraph():
    tweetsPool = getTweetsToday()
    nodesList = []
    edgesList = []
    for tweet in tweetsPool:
        nodesList.append({'keywords': tweet['words'], 'id': tweet['guid'], 'name': tweet['text'], 'source': tweet['author'], 'url': "", 'group': 233})
        for anotherTweet in tweetsPool:
            if (not anotherTweet == tweet) and (numOfSameWords(tweet, anotherTweet) > 2):
                edgesList.append({'source': tweet['guid'], 'target': anotherTweet['guid'], 'value': numOfSameWords(tweet, anotherTweet)})
    return {'nodes': nodesList, 'edges': edgesList}