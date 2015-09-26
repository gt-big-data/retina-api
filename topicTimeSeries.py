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
        for j in articleList:
            bucket[i][0] = startTime + i * bucketSize
            bucket[i][1] = startTime + (i + 1) * bucketSize
            if j['timestamp'] >= startTime + i * bucketSize and j['timestamp'] < startTime + (i + 1) * bucketSize:
                bucket[i][2] += 1

    for i in range(0, bucketNumber):
        sys.stdout.write("%d ~ " % bucket[i][0])
        sys.stdout.write("%d : " % bucket[i][1])
        for j in range(0, bucket[i][2]):
            sys.stdout.write("[]")
        sys.stdout.write('\n')

timeSeriesData("obama")