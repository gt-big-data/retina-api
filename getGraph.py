from bson.code import Code
import calendar, datetime, random
from datetime import *
from dbco import *

def dateGraph(day):
	thisDay = calendar.timegm(datetime.strptime(day, '%Y-%m-%d').timetuple())
	prevDay = thisDay - 1.5*24*60*60

	return dateRangeGraph(prevDay, thisDay)

def dateRangeGraph(startTime, endTime):
	startTime = int(startTime); endTime = int(endTime)
	originalSources = ["reuters.com", "theguardian.com", "cnn.com", "bbc.co.uk", "france24.com", "aljazeera.com", "ap.org", "wikinews.org", "nytimes.com", "euronews.com", "middleeasteye.net", "aa.com.tr", "independent.co.uk", "indiatimes.com", "rt.com", "latimes.com", "mercopress.com", "bnamericas.com", "chinadaily.com.cn", "allafrica.com"]
	nodes = list(db.qdoc.find({'timestamp': {'$gte': startTime, '$lte': endTime}, 'source': {'$in': originalSources}}, ['_id', 'keywords', 'source', 'title', 'topic', 'url']))
	for n in nodes:
		n['keywords'] = set(n['keywords'])
		n['name'] = n['title']
		n['id'] = n['_id']
		n['group'] = n.get('topic', int(500*random.random()))
		del n['title']
		del n['_id']
		if 'topic' in n:
			del n['topic']
	edges = []; pageWithEdge = set([])
	for i in range(0,len(nodes)):
		for j in range(i+1,len(nodes)):
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 2:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': nodes[i]['id'], 'target': nodes[j]['id'], 'value': le})
	for n in nodes:
		n['keywords'] = list(n['keywords'])

	connectNodes = [n for n in nodes if n['id'] in pageWithEdge]	

	return {'nodes': connectNodes, 'edges': edges}

def topicGraph(topic):
	topic = int(topic)
	nodes = list(db.qdoc.find({'topic': topic}, ['_id', 'keywords', 'source', 'title', 'topic', 'url']))
	for n in nodes:
		n['keywords'] = set(n['keywords'])
		n['name'] = n['title']
		n['id'] = n['_id']
		n['group'] = n.get('topic', int(500*random.random()));
		del n['title']
		del n['_id']
		if 'topic' in n:
			del n['topic']
	edges = []; pageWithEdge = set([]); 
	for i in range(0,len(nodes)):
		for j in range(i+1,len(nodes)):
			le = len(nodes[i]['keywords']&nodes[j]['keywords'])
			if le >= 2:
				pageWithEdge.add(nodes[i]['id']); pageWithEdge.add(nodes[j]['id']);
				edges.append({'source': nodes[i]['id'], 'target': nodes[j]['id'], 'value': le})
	for n in nodes:
		n['keywords'] = list(n['keywords'])

	connectNodes = [n for n in nodes if n['id'] in pageWithEdge]	

	return {'nodes': connectNodes, 'edges': edges}
