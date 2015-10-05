from dbco import *
import time

hours = 10
startTime = time.time()-10*3600
endTime = time.time()

match = {'$match': {'timestamp': {'$gt': startTime, '$lt': endTime}}}
proj = {'$project': {'tsMod': {'$subtract':["$timestamp", {'$mod':["$timestamp",3600]}]}}}
group = {'$group': {'_id':"$tsMod", 'c':{'$sum':1}}}
sort = {'$sort': {'_id': 1}}
print db.qdoc.find({'timestamp': {'$gte': startTime, '$lte': endTime}}).count()
print db.qdoc.aggregate([match, proj, group, sort])['result']