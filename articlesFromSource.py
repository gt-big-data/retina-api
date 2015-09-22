import pymongo
from dbco import *
from bson import json_util
from flask import Flask, request, jsonify
import json

def getArticlesFromSource(source, limit):
    doc = list(db.qdoc.find({'source':source}).sort('timestamp', pymongo.DESCENDING).limit(limit))
    return json.dumps(doc, default=json_util.default)
# def userInput():
#     source = input("Enter a news source:")
#     limit = input("Enter the number of articles you want to read:")
#     print (source_articles(source, limit))