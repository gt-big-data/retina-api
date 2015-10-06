import pymongo
from bson import json_util
import json
from dbco import *
import time

def keywordTimelineUsingAggregation(keyword):

    hours = 10
    startTime = time.time() - hours * 3600
    endTime = time.time()
    
    matchKeyword = {'$match': {'keywords': keyword}}
    matchTimestamp = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}}}
    project = {'$project': {'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', 3600]}]}}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}
    
    pipeline = [matchKeyword, matchTimestamp, project, group, sort]
    return list(db.qdoc.aggregate(pipeline))

def topicTimelineUsingAggregation(topic):

    bucketNumber = 100
    
    matchTopic = {'$match': {'topic': topic}}

    groupToFindRange = {'$group': {'_id': None, 'minTimestamp': {'$min': '$timestamp'}, 'maxTimestamp': {'$max': '$timestamp'}}}
    timeinfo = list(db.qdoc.aggregate([matchTopic,groupToFindRange]))[0]
    startTime = timeinfo['minTimestamp']
    endTime = timeinfo['maxTimestamp']
    bucketSize = int((endTime - startTime) / bucketNumber)
    
    matchTimestamp = {'$match': {'timestamp': {'$gte': startTime, '$lt': endTime}}}
    project = {'$project': {'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketSize]}]}}}
    group = {'$group': {'_id': '$tsMod', 'count': {'$sum': 1}}}
    sort = {'$sort': {'_id': 1}}
    
    pipeline = [matchTopic, matchTimestamp, project, group, sort]
    return list(db.qdoc.aggregate(pipeline))



if __name__ == "__main__":
    print keywordTimelineUsingAggregation("obama")
    print topicTimelineUsingAggregation(293)
