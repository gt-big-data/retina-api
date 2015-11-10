from bson.code import Code
from dbco import *
import time

def dateGraphMR(nextDayTs):
	#this works, it should not be used because it is slow
	thisDayTs = nextDayTs-2*86400;

	map = Code("function() {	var me = this;	arts.forEach(function(z) {		var me2 = z;		if(!me2._id.equals(me._id)) {			me2.keywords.forEach(function(k) {				if(me.keywords.indexOf(k) >= 0) {					emit([me.title, me2.title], 1)				}			});		}	});}")

	reduce = Code("function(key, values) {var tot = 0; for(var i = 0; i < values.length; i++) {tot += values[i];} return tot;}") #

	listAll = db.qdoc.find({'timestamp': {'$lt': nextDayTs, '$gte': thisDayTs}},['title', 'keywords'])

	result = db.qdoc.map_reduce(map, reduce, 'myresults', scope={'arts': list(listAll)}, query={'timestamp': {'$lt': nextDayTs, '$gte': thisDayTs}})
	result = result.find({'value': {'$gte': 2}})
	for comp in result:
		print comp
if __name__ == '__main__':
	dateGraph(time.time()-1.5*24*60*60, time.time());