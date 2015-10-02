import pymongo
from bson import json_util
import json
from dbco import *
from collections import Counter
import sys

def timeSeriesData(keyword):
    articlePool = db.qdoc.find({'keywords' : {'$in' : [keyword]}}).sort('timestamp', pymongo.DESCENDING)
    articleList = list(articlePool)
    bucketNumber = 100;
    startTime = articleList[len(articleList) - 1]['timestamp']
    endTime = articleList[0]['timestamp']
    duringTime = endTime - startTime
    bucketSize = duringTime / bucketNumber
    bucket = []

    for i in range(0, bucketNumber):
        bucket.append([0, 0, 0])
        bucket[i][0] = startTime + i * bucketSize
        bucket[i][1] = startTime + (i + 1) * bucketSize
    for article in articleList:
        bucket[int((article['timestamp'] - startTime) / bucketSize)][2] += 1

    data = []
    for i in range(len(bucket)):
        data.append({'start' : bucket[i][0], 'end' : bucket[i][1], 'count' : bucket[i][2]})
    print data

##    for i in range(0, bucketNumber):
##        sys.stdout.write("%d ~ " % bucket[i][0])
##        sys.stdout.write("%d : " % bucket[i][1])
##        for j in range(0, bucket[i][2]):
##            sys.stdout.write("[]")
##        sys.stdout.write('\n')

    return json.dumps(articleWithKeywords, default = json_util.default)
