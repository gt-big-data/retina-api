from getTopics import *
from collections import Counter
from dbco import *

def hasNumbers(str):
	return any(char.isdigit() for char in str)

t = largestTopicsTimelines(2,3)[2]

bucketLength = t['timeline'][1]['timestamp']-t['timeline'][0]['timestamp']
numBuckets = len(t['timeline'])

match = {'$match': {'topic': t['topic']}}
project = {'$project': {'title': True, 'keywords': True, 'timestamp': True, 'tsMod': {'$subtract': ['$timestamp', {'$mod': ['$timestamp', bucketLength]}]}}}
sort = {'$sort': {'timestamp': 1}}

articles = list(db.qdoc.aggregate([match, project, sort]))
keywordPerBucket = {}
titlesPerBucket = {}
totalKeywords = []

for a in articles:
	thisBucket = int(a['tsMod'])
	if thisBucket not in keywordPerBucket:
		keywordPerBucket[thisBucket] = [];
		titlesPerBucket[thisBucket] = [];
	if 'keywords' in a:
		kws = [k for k in a['keywords'] if not hasNumbers(k)]
		keywordPerBucket[thisBucket].extend(kws)
		totalKeywords.extend(kws)
	titlesPerBucket[thisBucket].append(a['title'])

totalKeywordsCount = float(len(totalKeywords))
totalKeywords = Counter(totalKeywords)

i = 1
for bucket in keywordPerBucket:
	bucketSize = len(titlesPerBucket[bucket])
	if bucketSize > 2:
		print "---------------------------"
		print "BUCKET ", i, " [size: ", bucketSize, "]", bucketLength
		keywordPerBucket[bucket] = Counter(keywordPerBucket[bucket])
		keywordScores = {}
		for kw in keywordPerBucket[bucket]:
			# print float(sum(keywordPerBucket[bucket].values()))
			keywordScores[kw] = (keywordPerBucket[bucket][kw]/float(sum(keywordPerBucket[bucket].values())))/(totalKeywords[kw]/totalKeywordsCount)
			# print kw, " => ", score
		bestKw = sorted(keywordScores, key=keywordScores.get, reverse=True)
		# for kw in bestKw:
		# 	print kw, " => ", keywordScores[kw]
		for title in titlesPerBucket[bucket]:
			words = title.split(' ')
			titleScore = sum([keywordScores[w] for w in words if w in keywordScores])*pow(0.98, (len(words)-5))
			print title.encode('utf-8'), "=>", titleScore
		print "---------------------------"
		# print bucket, "-> ", keywordPerBucket[bucket]
	i += 1