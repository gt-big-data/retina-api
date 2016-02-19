from dbco import *
from bson import json_util
import datetime, json

def getCoKeywords(term):
    match = {'$match': {'timestamp': {'$gte': (datetime.datetime.now()-datetime.timedelta(days=1))}, 'keywords': term}}
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    
    compatible = lambda x: {'keyword': x['_id'], 'total': x['total']}
    data = [compatible(d) for d in query_result if d['_id'] != term]

    return data

def getTrendingKeywords():
    match = {'$match': {'timestamp': {'$gte': (datetime.datetime.now()-datetime.timedelta(days=1))}}}
    project = {'$unwind': '$keywords'}
    group = {'$group': {'_id': '$keywords', 'total': {'$sum': 1} }}
    sort = {'$sort': {'total': -1}}
    limit  = {'$limit': 10}
    pipeline = [match, project, group, sort, limit]
    query_result = db.qdoc.aggregate(pipeline)
    front_end_compatable = lambda x: {'keyword': x['_id'], 'total': x['total']}
    return map(front_end_compatable, query_result)