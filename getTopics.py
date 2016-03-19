from datetime import datetime, timedelta
from dbco import *

def bySize(days, limit):
    limit = int(limit); days = int(days)
    endTime = datetime.utcnow()
    startTime = endTime - timedelta(days=days)
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : limit}
    topicCounts = list(db.qdoc.aggregate([match, group, sort, limit]))

    topics = list(db.topic.find({'_id': {'$in': [t['_id'] for t in topicCounts]}}))
    topicNames = {tu['_id']: ' '.join([kw['keyword'] for kw in tu['keywords']][:3]) for tu in topics}
    
    for topic in topicCounts:
        topic['name'] = topicNames.get(topic['_id'], '')
    return topicCounts

if __name__ == "__main__":
    print(bySize(3,10))