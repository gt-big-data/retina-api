from bson import json_util
import pymongo, json, time
from datetime import datetime, timedelta
from dbco import *

def byKeyword(keyword, daysLoad, bucketNumber=100):

    endTime = datetime.now()
    startTime = endTime - timedelta(days=int(daysLoad))
    bucketSize = int((endTime - startTime).total_seconds() / bucketNumber)
    
    match = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}, 'keywords': keyword}}
    projTs = {'$project': {'keywords': 1, 'timestamp': {'$divide': [{'$subtract': ['$timestamp', datetime.fromtimestamp(0)]}, 1000]}}}
    project = {'$project': {'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}
    
    pipeline = [match, projTs, project, group, sort]
    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def byTopic(topic, bucketNumber=50):
    originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]    
    topic = int(topic);

    matchTopic = {'$match': {'entTopic': topic}} #, 'source': {'$in': originalSources}

    groupToFindRange = {'$group': {'_id': None, 'minTimestamp': {'$min': '$timestamp'}, 'maxTimestamp': {'$max': '$timestamp'}}}
    timeinfo = list(db.qdoc.aggregate([matchTopic,groupToFindRange]))[0]
    startTime = timeinfo['minTimestamp']; endTime = timeinfo['maxTimestamp']
    bucketSize = int((endTime - startTime).total_seconds() / bucketNumber)

    projTs = {'$project': {'keywords': 1, 'title': 1, 'timestamp': {'$divide': [{'$subtract': ['$timestamp', datetime.fromtimestamp(0)]}, 1000]}}}
    project = {'$project': {'title': True, 'timestamp': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}, 'titleScore': {'$ifNull': ['$titleScore', -1]}}}
    sort1 = {'$sort': {'titleScore': -1}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}, 'headline': {'$first': '$title'}}}
    sort2 = {'$sort': {'_id': 1}}
    
    pipeline = [matchTopic, projTs, project, sort1, group, sort2]

    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def allSources(bucketSize=86400):
    endTime = datetime.now()
    startTime = endTime-timedelta(days=90)
    matchRange = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}}}

    projTs = {'$project': {'source': 1, 'timestamp': {'$divide': [{'$subtract': ['$timestamp', datetime.fromtimestamp(0)]}, 1000]}}}
    project = {'$project': {'source': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    group = {'$group': {'_id': {'source': '$source', 'tsMod': '$tsMod'}, 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id.source': 1, '_id.tsMod': 1}}

    pipeline = [matchRange, projTs, project, group, sort]
    returnList = []
    fullObj = list(db.qdoc.aggregate(pipeline))
    for source in db.qdoc.distinct('source'):
        obj = []
        for o in fullObj:
            if o['_id']['source'] == source:
                obj.append({'_id': o['_id']['tsMod'], 'count': o['count']})
        returnList.append({'name': source, 'timeline': returnObj(obj, startTime, endTime, bucketSize)})
    return returnList

def sourceTimeline(source, bucketSize=21600):
    
    endTime = datetime.now()
    startTime = endTime-timedelta(days=30)
    matchSource = {'$match': {'source': source, 'timestamp': {'$gte': startTime, '$lt': endTime}}}
    projTs = {'$project': {'source': 1, 'timestamp': {'$divide': [{'$subtract': ['$timestamp', datetime.fromtimestamp(0)]}, 1000]}}}
    project = {'$project': {'source': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}

    pipeline = [matchSource, projTs, project, group, sort]

    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def returnObj(obj, minTime, maxTime, bucketSize):
    minTime = (minTime-datetime.fromtimestamp(0)).total_seconds()
    maxTime = (maxTime-datetime.fromtimestamp(0)).total_seconds()

    newReturn = []
    minTime = minTime-(minTime%bucketSize); maxTime = maxTime-(maxTime%bucketSize)
    time = minTime; u = 0;
    while time <= maxTime:
        ob = {'_id': 0, 'count':0, 'headline': ''}
        if len(obj) > u:
            ob = obj[u]
        if ob['_id'] == time:
            newReturn.append({'timestamp': int(ob['_id']), 'count': ob['count'], 'headline': ob.get('headline', '')})
            u += 1
        else:
            newReturn.append({'timestamp': int(time), 'count': 0, 'headline': ''})
        time += bucketSize
    return newReturn

if __name__ == "__main__":
    print tweetTimeline("obama", 20)
    # print topicTimeline(293)