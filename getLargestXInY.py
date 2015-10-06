from dbco import *
import time

def getLargestXTopicsInYDays(amountTopics, lastDays):
    startTime = time.time() - lastDays * 24 * 3600
    endTime = time.time()
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : amountTopics}
    return list(db.qdoc.aggregate([match, group, sort, limit]))

if __name__ == "__main__":
    print(getLargestXTopicsInYDays(10, 1))