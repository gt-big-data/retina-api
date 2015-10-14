from dbco import *
from bson import json_util
import time, json

def coKeywords(term):
    match = {'$match': {'timestamp': {'$gte': time.time()-24*3600}, 'keywords': term}}
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    
    compatible = lambda x: {'keyword': x['_id'], 'total': x['total']}
    data = [compatible(d) for d in query_result if d['_id'] != term]

    return json.dumps(data, default=json_util.default)

def trendingKeywords():
    match = {'$match': {'timestamp': {'$gte': time.time()-24*3600}}}
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    front_end_compatable = lambda x: {'keyword': x['_id'], 'total': x['total']}
    return json.dumps(map(front_end_compatable, query_result), default=json_util.default)
