from dbco import *
import time

def articlesXHours(hours):
    return list(db.qdoc.find({'timestamp': {'$gte': time.time()- int(hours)*60*60}}))