from glob import glob
import json
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
    level=logging.INFO)
from gensim import corpora, models, similarities, matutils
import scipy.stats as stats
import matplotlib.pyplot as plt
import re
import pylab

def convert(f):
    ''' Converting json to dictionary to input pandas'''
    obj = json.loads(f)
    for k, v in obj.items():
        if isinstance(v, list):
            obj[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                obj['%s_%s' % (k, kk)] = vv
            del obj[k]
    return obj   

class MyCorpus(object):
    def __init__(self, fname, stopf = None, V = None):
        self.fname = fname
        self.file = open(fname, "r")
        stoplist = stopf
        self.dictionary = self.make_dict(stoplist, V)
    def reset(self):
        self.file.seek(0)
    def proc(self, line):
        return filter(lambda x: len(x) > 2, map(lambda x: x.strip(), re.sub(r'[0-9]+|\W',' ',line.strip().lower()).split()))
    def make_dict(self, stoplist = [], V = None):
        self.reset()
        dictionary = corpora.Dictionary(self.proc(line) for line in self.read_file())
        stop_ids = [dictionary.token2id[sw] for sw in stoplist if sw in dictionary.token2id]
        dictionary.filter_tokens(stop_ids)
        dictionary.filter_extremes(keep_n = V)
        return dictionary
    def read_file(self):
        for line in self.file:
                txt = json.loads(line)["text"]
                if len(txt) > 5: yield txt
    
    def __iter__(self):
        self.reset()
        for line in self.read_file():
            bow = self.dictionary.doc2bow(self.proc(line))
            if len(bow) >= 5: yield bow

def sym_kl(p,q):
    return np.sum([stats.entropy(p,q),stats.entropy(q,p)])

if __name__ == '__main__':
    stoplist = stopwords.words('english')
    yelpdata = MyCorpus('review_pittsburgh_restaurant.json', stoplist, 10000)
    K = 5
    kl = []
    l = np.array([sum(cnt for _, cnt in doc) for doc in yelpdata])
    for i in range(1,30,1):
        lda = models.ldamodel.LdaModel(corpus = yelpdata, id2word = yelpdata.dictionary, num_topics = K, update_every = 1)
        m1 = lda.expElogbeta
        U,cm1,V = np.linalg.svd(m1)
        lda_topics = lda[yelpdata]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2/cm2norm
        kl.append(sym_kl(cm1,cm2))
    print kl
    plt.plot(kl)
    plt.ylabel('Symmetric KL Divergence')
    plt.xlabel('No of Topics')
    plt.savefig('kldivergence.png', bbox_inches='tight')

