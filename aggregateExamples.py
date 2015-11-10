from dbco import *
import time

endTime = time.time()
startTime = endTime-3*86400

# Example 1: count the keyword occurrence in a time slice
match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
unwind = {"$unwind": '$keywords'}
group = {"$group" : {"_id" : "$keywords", "count" : {"$sum" : 1}}}
sort = {'$sort': {'count': -1}}
limit = {'$limit': 50}

keywordCounts = list(db.qdoc.aggregate([match, unwind, group, sort, limit]))
for key in keywordCounts:
	print key

# Example 2: count the count of the number of articles by source for a specific keyword
kw = 'percent'
match = {'$match': {'keywords': kw, 'timestamp': {"$gt" : startTime, "$lt" : endTime}}}
group = {'$group': {"_id": '$source', "count": {'$sum': 1}}}
sort = {'$sort': {'count': -1}}
sourceCounts = list(db.qdoc.aggregate([match, group, sort]))

for key in sourceCounts:
	print key

# Example 3: Most important keywords in each slice of 86400 seconds (1 day) in the last 3 days
match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
project = {'$project': {'keywords': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', 86400]}]}}}
unwind = {"$unwind": '$keywords'}
group = {'$group': {'_id': {'tsMod': '$tsMod', 'keywords': '$keywords'}, 'count': {'$sum': 1}}}
match2 = {'$match': {'count': {'$gte': 4}}}
sort = {'$sort': {'_id.tsmod': 1, 'count': -1}}
group2 = {'$group': {'_id': '$_id.tsMod', 'dictCount': {'$push': {'keywords': '$_id.keywords', 'count': '$count'}}}}
sort2 = {'$sort': {'_id': 1}}

func = db.qdoc.aggregate([match,project,unwind,group,match2,sort,group2,sort2])

for day in func:
	print day['_id']
	for kw in day['dictCount'][:10]:
		print kw
	print "-----------------------------------"