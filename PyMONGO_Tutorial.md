# Basic MongoDB queries to know for python:

**What file do you import to connect to the database?**

```
from dbco import *
```


How do you count the number of articles in collection ''tweet''?
```
number_articles = db.tweet.find().count()
```

How do you select articles that come from the source ``cnn''?
```
articles_source = db.qdoc.find_one({"source" : "cnn"})
```

Given a pymongo object, how do you iterate over it?
```
articles = db.qdoc.find().limit(100)
articles = list(articles)

```
OR
```
articles = db.qdoc.find().limit(100)
for a in articles:
	
```

How do you select articles that have a key named ``topic'' (where the key 'topic' exists)?
```
```

How do you select articles from the last hour?
```
db.qdoc.find({"timestamp":{'$gte':time.time()-3600}}).sort('timestamp', pymongo.DESCENDING)
```

How do you select the most recent 100 articles?
```
db.qdoc.find().sort('timestamp', pymongo.DESCENDING).limit(100)
```

How do you find the number of articles in a topic?
```
db.qdoc.find({'topic': 293}).count()
```

How do you use aggregate queries to count the number of articles per keyword?

