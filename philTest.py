from dbco import *
import pymongo

arti = dd.qdoc.find().sort('timestamp', pymongo.DESCENDING).limit(10000)