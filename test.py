from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from dbco import *
from getTopics import *

topic = largestTopics(2, 1)[0]['_id']

print topic

articles = list(db.qdoc.find({'topic': topic}))
articleContents = [a['content'] for a in articles]

count_vect = CountVectorizer(stop_words='english', ngram_range = (3,4), binary=True)

tfidf_trans = TfidfTransformer() #initialize our tfidf transformer

matrixCount = count_vect.fit_transform(articleContents)

totalCount = matrixCount.mean(axis=0).A[0]

vocabValue = count_vect.vocabulary_.keys()
vocabIndex = count_vect.vocabulary_.values()


tenBestI = totalCount.argsort()[-30:][::-1]
tenBest = [vocabValue[vocabIndex.index(i)].encode('ascii', 'ignore') for i in tenBestI]

print tenBest