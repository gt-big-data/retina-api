from dateutil import parser
from bson import ObjectId
from dbco import *
import random, time, json
from datetime import datetime, timedelta

def kwGraph(startDate, endDate):
	startDatetime = parser.parse(startDate)
	endDatetime = parser.parse(endDate)
	originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]
	match = {'$match': {'timestamp': {'$gte': startDatetime, '$lte': endDatetime}, 'source': {'$in': originalSources}}}
	proj = {'$project': {'id': '$_id', 'name': '$title', 'group': {'$ifNull': ['$topic', int(500*random.random())]}, 'keywords': 1}}

	nodes = list(db.qdoc.aggregate([match, proj]))
	for n in nodes:
		n['keywords'] = set(n.get('keywords', []))

	edges = []; pageWithEdge = set([])
	for i in range(0,len(nodes)):
		for j in range(i+1,len(nodes)):
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 2:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': nodes[i]['id'], 'target': nodes[j]['id'], 'value': le})
	for n in nodes:
		n['keywords'] = list(n['keywords'])
	return {'nodes': [n for n in nodes if n['id'] in pageWithEdge], 'edges': edges}

def byEntity():
	startDatetime = datetime.utcnow()-timedelta(days=30)
	match = {'$match': {'timestamp': {'$gte': startDatetime}}}
	project = {'$project': {'entities': 1, '_id': 1}}
	unwind = {'$unwind': '$entities'}
	group = {'$group': {'_id': '$entities.wdid', 'aIds': {'$push': '$_id'}, 'count': {'$sum': 1}}}
	sort = {'$sort': {'count': -1}}
	limit = {'$limit': 400}
	lookup = {'$lookup': {'from': 'entities', 'localField': '_id', 'foreignField': '_id', 'as': 'entInfo'}}
	unwind2 = {'$unwind': '$entInfo'}
	project2 = {'$project': {'_id': 1, 'aIds': 1, 'count': 1, 'name': '$entInfo.title'}}
	nodes = []
	i = 0
	for d in db.qdoc.aggregate([match, project, unwind, group, sort, limit, lookup, unwind2, project2]):
		d['id'] = i
		del d['_id']; i += 1
		d['aIds'] = set([str(r) for r in d.get('aIds', [])])
		nodes.append(d)
	edges = []
	for i in range(len(nodes)):
		for j in range(i+1, len(nodes)):
			size = len(nodes[i]['aIds']&nodes[j]['aIds'])
			if size > 50:
				edges.append({'source': i, 'target': j, 'count': size})
		del nodes[i]['aIds']
	f = open('data.json', 'w'); f.write(json.dumps({'nodes': nodes, 'links': edges})); f.close();

def entGraph(startDate, endDate):
	startDatetime = parser.parse(startDate)
	endDatetime = parser.parse(endDate)
	originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]
	match = {'$match': {'timestamp': {'$gte': startDatetime, '$lte': endDatetime}, 'source': {'$in': originalSources}}}
	proj = {'$project': {'name': '$title', 'group': {'$ifNull': ['$topic', int(500*random.random())]}, 'entities': 1}}

	nodes = list(db.qdoc.aggregate([match, proj]))
	wdids = set([])

	for n in nodes:
		n['keywords'] = set([e['wdid'] for e in n.get('entities', {}) if e['count'] > 1 and e['wdid'] is not None])
		wdids |= n['keywords']
		if 'entities' in n:
			del n['entities']

	entDict = {w['_id']: w['title'] for w in db.entities.find({'_id': {'$in': list(wdids)}})}

	edges = []; pageWithEdge = set([])
	for i in range(0,len(nodes)):
		nodes[i]['id'] = i;
		for j in range(i+1,len(nodes)):
			nodes[j]['id'] = j
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 3:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': i, 'target': j, 'value': le})

	for n in nodes:
		n['keywords'] = list(n['keywords'])
	return {'nodes': [n for n in nodes if n['id'] in pageWithEdge], 'links': edges, 'entityDict': entDict}

if __name__ == '__main__':
	byEntity()