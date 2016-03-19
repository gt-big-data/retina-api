from getTopics import *
from getTimeline import *
from collections import Counter
import networkx as nx
from dbco import *
import numpy as np
import time, datetime

def hasNumbers(str):
	return any(char.isdigit() for char in str)

def buildTitleImportance(topic):
	t = byTopic(topic)
	bucketLength = t[1]['timestamp']-t[0]['timestamp']

	match = {'$match': {'topic': topic}}
    projTs = {'$project': {'keywords': 1, 'timestamp': {'$divide': [{'$subtract': ['$timestamp', datetime.datetime.fromtimestamp(0)]}, 1000]}}}
	project1 = {'$project': {'_id': True, 'title': True, 'keywords': True, 'timestamp': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketLength]}]}}}
	sort = {'$sort': {'timestamp': 1}}

	articles = list(db.qdoc.aggregate([match, projTs, project1, sort]))
	idsFromTitle = {}
	keywordPerBucket = {}; titlesPerBucket = {}
	keywordEdges = {}
	totalKeywords = []

	for a in articles:
		idsFromTitle[a['title']] = a['_id']
		thisBucket = int(a['tsMod'])
		if thisBucket not in keywordPerBucket:
			keywordPerBucket[thisBucket] = [];
			titlesPerBucket[thisBucket] = [];
			keywordEdges[thisBucket] = [];
		if 'keywords' in a:
			kws = [k for k in a['keywords'] if ' ' not in k and not hasNumbers(k)][:8]
			for k1 in kws:
				keywordEdges[thisBucket].extend([(k1, k2) for k2 in kws if k1 != k2])

			keywordPerBucket[thisBucket].extend(kws)
			totalKeywords.extend(kws)
		titlesPerBucket[thisBucket].append(a['title'])

	totalKeywordsCount = float(len(totalKeywords))
	totalKeywords = Counter(totalKeywords)

	titleScoreUpdate = db.qdoc.initialize_unordered_bulk_op()
	for bucket in keywordPerBucket:
		if len(titlesPerBucket[bucket]) > 0:
			keywordPerBucket[bucket] = Counter(keywordPerBucket[bucket])
			keywordScores = {}
			for kw in keywordPerBucket[bucket]:
				kw = kw.lower()
				keywordScores[kw] = (keywordPerBucket[bucket][kw]/float(sum(keywordPerBucket[bucket].values())))/(totalKeywords[kw]/totalKeywordsCount)

			G = nx.Graph()
			G.add_edges_from(keywordEdges[bucket])
			PR = nx.pagerank(G)

			titleScores = {}
			for title in titlesPerBucket[bucket]:
				words = title.lower().encode('utf-8').translate(None, "-,.!?:;").split(' ')
				titleScore = sum([keywordScores.get(w,0.0) for w in words])*pow(0.98, (len(words)-5))
				titlePRScore = sum([PR.get(w,0.0) for w in words])*pow(0.98, (len(words)-5))
				titleScores[title.encode('utf-8')] = titlePRScore
				titleScoreUpdate.find({'_id': idsFromTitle[title]}).upsert().update({
					'$set': {
						'titleScore': titlePRScore,
					},
				})
	titleScoreUpdate.execute()
	print topic

match = {'$match': {'topic': {'$exists': True}, 'timestamp': {'$gte': datetime.datetime.now()-datetime.timedelta(days=7)}}}
project = {'$project': {'_id': True, 'topic': True, 'titleScore': {'$ifNull': ['$titleScore', -1]}}}
group = {'$group': {'_id': '$topic', 'articleCount': {'$sum': 1}, 'noScoreCount': {'$sum': {'$cond' : {'if': {'$eq': [ "$titleScore", -1 ] }, 'then': 1, 'else': 0 }}}}}
match2 = {'$match': {'noScoreCount': {'$gt': 2}, 'articleCount': {'$gt': 15}}}
sort = {'$sort': {'_id': -1}}
limit = {'$limit': 200}
topics2Update = list(db.qdoc.aggregate([match, project, group, match2, sort, limit]))
for t in topics2Update:
	buildTitleImportance(t['_id'])