from bson import json_util
import pymongo, json, time
from datetime import datetime
from dbco import *

def getKeywordTimeline(keyword, daysLoad, bucketNumber=100):

    startTime = time.time() - int(daysLoad)* 24 * 3600
    endTime = time.time()
    bucketSize = int((endTime - startTime) / bucketNumber)
    
    match = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}, 'keywords': keyword}}
    project = {'$project': {'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}
    
    pipeline = [match, project, group, sort]
    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def getKeywordTweetTimeline(keyword, daysLoad, bucketNumber=100):

    startTime = time.time() - int(daysLoad)* 24 * 3600; endTime = time.time()
    bucketSize = int((endTime - startTime) / bucketNumber)

    match = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}, 'words': keyword}}
    project = {'$project': {'content': True, '_id': True, 'tsmod': {'$mod': ['timestamp', 1000]}}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}
    
    pipeline = [match, project, group, sort]
    return returnObj(list(db.tweet.aggregate(pipeline)), startTime, endTime, bucketSize)

def topicTimeline(topic, bucketNumber=50):
    topic = int(topic);
    matchTopic = {'$match': {'topic': topic}}

    groupToFindRange = {'$group': {'_id': None, 'minTimestamp': {'$min': '$timestamp'}, 'maxTimestamp': {'$max': '$timestamp'}}}
    timeinfo = list(db.qdoc.aggregate([matchTopic,groupToFindRange]))[0]
    startTime = timeinfo['minTimestamp']; endTime = timeinfo['maxTimestamp']
    bucketSize = int((endTime - startTime) / bucketNumber)
    
    matchTimestamp = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}}}
    project = {'$project': {'title': True, 'timestamp': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}, 'titleScore': {'$ifNull': ['$titleScore', -1]}}}
    sort1 = {'$sort': {'titleScore': -1}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}, 'headline': {'$first': '$title'}}}
    sort2 = {'$sort': {'_id': 1}}
    
    pipeline = [matchTopic, matchTimestamp, project, sort1, group, sort2]

    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def allSourcesTimeline(bucketSize=86400):

    sourceList = list(db.qdoc.distinct('source'))
    print sourceList
    
    startTime = time.time()-90*86400
    endTime = time.time()
    matchSource = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}}}
    project = {'$project': {'source': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    group = {'$group': {'_id': {'source': '$source', 'tsMod': '$tsMod'}, 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id.source': 1, '_id.tsMod': 1}}

    pipeline = [matchSource, project, group, sort]
    returnList = []
    fullObj = list(db.qdoc.aggregate(pipeline))
    for source in sourceList:
        obj = []
        for o in fullObj:
            if o['_id']['source'] == source:
                obj.append({'_id': o['_id']['tsMod'], 'count': o['count']})
        returnList.append({'name': source, 'timeline': returnObj(obj, startTime, endTime, bucketSize)})
    return returnList

def sourceTimeline(source, bucketSize=21600): # 6*3600
    
    startTime = time.time()-30*86400
    endTime = time.time()
    matchSource = {'$match': {'source': source, 'timestamp': {'$gte': startTime, '$lt': endTime}}}
    project = {'$project': {'source': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}

    pipeline = [matchSource, project, group, sort]

    return returnObj(list(db.qdoc.aggregate(pipeline)), startTime, endTime, bucketSize)

def returnObj(obj, minTime, maxTime, bucketSize):
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