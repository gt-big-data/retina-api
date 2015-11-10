from dbco import *
import time

endTime = time.time()
startTime = endTime-3*86400

# match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
# unwind = {"$unwind": '$keywords'}
# group = {"$group" : {"_id" : "$keywords", "count" : {"$sum" : 1}}}
# sort = {'$sort': {'count': -1}}
# limit = {'$limit': 50}

# keywordCounts = list(db.qdoc.aggregate([match, unwind, group, sort, limit]))
# for key in keywordCounts:
# 	print key

# match = {'$match': {'keywords': 'percent', 'timestamp': {"$gt" : startTime, "$lt" : endTime}}}
# group = {'$group': {"_id": '$source', "count": {'$sum': 1}}}
# sort = {'$sort': {'count': -1}}
# sourceCounts = list(db.qdoc.aggregate([match, group, sort]))

# for key in sourceCounts:
# 	print key

match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
project = {'$project': {'keywords': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', 86400]}]}}}
unwind = {"$unwind": '$keywords'}
group = {'$group': {'_id': {'tsMod': '$tsMod', 'keywords': '$keywords'}, 'count': {'$sum': 1}}}
match2 = {'$match': {'count': {'$gte': 4}}}
sort = {'$sort': {'_id.tsmod': 1, 'count': -1}}
group2 = {'$group': {'_id': '$_id.tsMod', 'dictCount': {'$push': {'keywords': '$_id.keywords', 'count': '$count'}}}}
sort2 = {'$sort': {'_id': 1}}

func = db.qdoc.aggregate([match,project,unwind,group,match2,sort,group2,sort2])
	# group,
	# sort,
	# group2
	# ])

for day in func:
	print day['_id']
	for kw in day['dictCount'][:10]:
		print kw
	print "-----------------------------------"