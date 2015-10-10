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
    return list(db.qdoc.aggregate([match, group, sort, limit]))

def largestTopicsTimelines(days, limit):
	topicList = [t['_id'] for t in largestTopics(days, limit)]
	topicNames = {}
	topics = list(db.topic.find({'_id': {'$in': topicList}}))
	for tu in topics:
		topicNames[tu['_id']] = ' '.join([kw['keyword'] for kw in tu['keywords']][:3])

	timelines = []
	for topic in topicList:
		obj = {'name': topicNames[topic], 'topic': topic, 'timeline': topicTimeline(topic)}
		timelines.append(obj)

	return timelines

if __name__ == "__main__":
    print(getLargestXTopicsInYDays(10, 1))