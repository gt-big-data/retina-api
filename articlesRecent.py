from dbco import *

def recentArticles(page, perPage):
    page = int(page); perPage = int(perPage)
    articles = list(db.qdoc.find(projection={'content': False}).sort('timestamp', -1).limit(perPage).skip((page - 1) * perPage))
    for article in articles:
        article['_id'] = str(article['_id'])
    return articles