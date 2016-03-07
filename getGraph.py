from dateutil import parser
from dbco import *
import random, time

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

def entGraph(startDate, endDate):
	startDatetime = parser.parse(startDate)
	endDatetime = parser.parse(endDate)
	originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]
	match = {'$match': {'timestamp': {'$gte': startDatetime, '$lte': endDatetime}, 'source': {'$in': originalSources}}}
	proj = {'$project': {'id': '$_id', 'name': '$title', 'group': {'$ifNull': ['$topic', int(500*random.random())]}, 'entities': 1}}

	nodes = list(db.qdoc.aggregate([match, proj]))
	for n in nodes:
		n['keywords'] = set([e['wdid'] for e in n.get('entities', {}) if e['count'] > 1])

	edges = []; pageWithEdge = set([])
	for i in range(0,len(nodes)):
		for j in range(i+1,len(nodes)):
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 3:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': nodes[i]['id'], 'target': nodes[j]['id'], 'value': le})
	for n in nodes:
		n['keywords'] = list(n['keywords'])
	return {'nodes': [n for n in nodes if n['id'] in pageWithEdge], 'edges': edges}