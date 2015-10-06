from dbco import *
import time

def getLargestXTopicsInYDays(amountTopics, timeFrame):
    startTime = time.time() - timeFrame * 3600 * 24
    endTime = time.time()
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : amountTopics}
    topics = (list(db.qdoc.aggregate([match, group, sort, limit])))
    # for topic in topics:
    #     print(topic['_id'], " => ", topic['count'])
    return topics

if __name__ == "__main__":
    print(getLargestXTopicsInYDays(10, 1))