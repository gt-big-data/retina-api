from dbco import *
import time
from Timeline import *

def largestTopics(days, limit):
    limit = int(limit); days = int(days)
    startTime = time.time() - days * 24 * 3600
    endTime = time.time()
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : limit}
    topicCounts = list(db.qdoc.aggregate([match, group, sort, limit]))
    topicIds = [t['_id'] for t in topicCounts]
    topics = list(db.topic.find({'_id': {'$in': topicIds}}))
    topicNames = {}
    
    for tu in topics:
        topicNames[tu['_id']] = ' '.join([kw['keyword'] for kw in tu['keywords']][:3])

    for topic in topicCounts:
        topic['name'] = topicNames.get(topic['_id'], '')

    return topicCounts

def largestTopicsTimelines(days, limit):
    topicList = [t['_id'] for t in largestTopics(days, limit)]
    topicNames = {}
    topics = list(db.topic.find({'_id': {'$in': topicList}}))
    for tu in topics:
        topicNames[tu['_id']] = ' '.join([kw['keyword'] for kw in tu['keywords']][:3])

    timelines = []
    for topic in topicList:
        obj = {'name': topicNames.get(topic, ''), 'topic': topic, 'timeline': topicTimeline(topic)}
        timelines.append(obj)

    return timelines

if __name__ == "__main__":
    print(getLargestXTopicsInYDays(10, 1))
