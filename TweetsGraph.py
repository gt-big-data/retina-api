from dbco import *
import pymongo
import time


def getTweetsToday():
    startTime = time.time() - 3600
    matchTime = {'$match': {'timestamp': {'$gte': startTime}}}
    return list(db.tweet.aggregate([matchTime]))

def numOfSameWords(tweet1, tweet2):
    commonWords = set(tweet1['words']) & set(tweet2['words'])
    return len(commonWords)

def buildNodesAndEdges():
    tweetsPool = getTweetsToday()
    nodesList = []
    edgesList = []
    for tweet in tweetsPool:
        nodesList.append({'keywords': tweet['words'], 'id': tweet['guid'], 'name': tweet['text'], 'source': tweet['author'], 'url': "", 'group': 233})
        for anotherTweet in tweetsPool:
            if (not anotherTweet == tweet) and (numOfSameWords(tweet, anotherTweet) > 2):
                edgesList.append({'source': tweet['guid'], 'target': anotherTweet['guid'], 'value': numOfSameWords(tweet, anotherTweet)})
    return {'nodes': nodesList, 'edges': edgesList}