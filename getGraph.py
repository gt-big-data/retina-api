import calendar, datetime
from datetime import *
from dbco import *

def dateGraph(day):
	thisDay =  datetime.strptime(day, '%Y-%m-%d')
	nextDay = datetime.utcfromtimestamp(calendar.timegm(thisDay.timetuple()) + 86400)
	return list(db.graph_topics.find({'date': {'$lt': nextDay, '$gte': thisDay}}).limit(1))