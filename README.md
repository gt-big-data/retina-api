Retina API
=========

About
-----
REal-Time Intelligent News Application API.
Get access to our annotated articles with keywords, topics, entities.

Search for Articles
------------

#### http://api.retinanews.net/article/recent/{limit}
Parameters: {limit} replace that by an integer between 1 and 1000. Will return a list of articles {limit} most recent articles in RetinaNews.

Search for Articles by Keywords
-------------

#### http://api.retinanews.net/article/keywords/{keywords}
Parameters: {keywords} replace keywords with strings of keywords seperated by commas. Returns list of articles associated with the keywords inputted.

Tools
-----

###MongoDB
MongoDB (from "humongous") is an open-source document database, and the leading NoSQL database. The [documentation](http://docs.mongodb.org/manual/) is superb.
