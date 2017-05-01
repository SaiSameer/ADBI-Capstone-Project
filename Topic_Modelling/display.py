import logging

from gensim.models import LdaModel
from gensim import corpora
from settings import Settings
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w{3,}')

reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "models/dictionary.dict"
corpus_path = "models/corpus.lda-c"
lda_num_topics = 6
lda_model_path = "models/lda_model_50_topics.lda"

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path)
lda = LdaModel.load(lda_model_path)

i = 0
topics = {}
testTopics = lda.show_topics(lda_num_topics)

for topic in lda.show_topics(lda_num_topics):
    i += 1
    keyWord = {}
    topicAndWordList = list(topic)
    topics[topicAndWordList[0]]=topicAndWordList[1]
    
    for key in topics:	
        keyWord[key] = []
        temp = []
        temp = topics[key].split('+')
        for elem in temp:
            keyWord[key].append(elem.split("*")[1])

print '\n'   

count = 0
reviews_cursor = reviews_collection.find()

topicSum = [float(0) for elem in topics]
topicAverageRating = [float(0) for elem in topics]
totalWordCount = [float(0) for elem in topics]

reviews_cursor = reviews_collection.find()

for dataPoint in reviews_cursor:
    tokens = tokenizer.tokenize(raw)
    raw = dataPoint['text'].lower()
    for word in tokens:
        for key in topics:
            if dataPoint['business'] == 'SsGNAc9U-aKPZccnaDtFkA':
                if word in keyWord[key]:
                    topicSum[key] = topicSum[key] + float(dataPoint['stars'])
                    totalWordCount[key] = totalWordCount[key] + 1
                if totalWordCount[key] > 0:
                    topicAverageRating[key] = topicSum[key]/totalWordCount[key]


businessRating = {}

class businessRatingClass:
    ratingCount = 0
    averageRating = 0
    
    def __init__(self, rating, count):
        self.averageRating = rating
        self.ratingCount = count
    
    def getAverageRating(self):
        return self.averageRating


for index in range(0,len(topics)):
    newBusinessObject = businessRatingClass(topicAverageRating[index], totalWordCount[index])
    businessRating[index] = newBusinessObject
  
sortedbusinessRating = sorted(businessRating.items(), key=lambda value : value[1].averageRating)

minRatingCount = 0
minRating = 5
minIndex = 0

for element in sortedbusinessRating: 
    if element[1].averageRating < minRating and element[1].ratingCount > 0:
        minRating = element[1].averageRating
        minIndex = element[0]
        minRatingCount = element[1].ratingCount


print '\n'
print 'Topic with minimum rating', ' ',minIndex
for elem in testTopics:
    if int(elem[0]) == minIndex:
        print elem[1]
print 'Rating ', ' - ', minRating
print '\n'
print 'Topic with maximum rating', ' ',sortedbusinessRating[-1][0]
for elem in testTopics:
    if int(elem[0]) == sortedbusinessRating[-1][0]:
        print elem[1]
print 'Rating ', ' - ', sortedbusinessRating[-1][1].averageRating
