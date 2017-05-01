from gensim import corpora, models
from nltk.corpus import stopwords
import json
import re
import ijson
import pandas as pd
from pandas import *
import ast

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


if __name__ == '__main__':
    
    businessJsonFile = "./dataset//yelp_academic_dataset_business.json"
    df = pd.DataFrame([convert(line) for line in file(businessJsonFile)])
    df1 = df[["business_id","name","city",'categories']]
    df2 = df1[df1.city == "Pittsburgh"]
    bus_id = df2['business_id'].tolist()
    bus_id = set(bus_id)

    reviewJsonFile = "./dataset//yelp_academic_dataset_review.json"
    finalReviewJsonFile = "review_pittsburgh_restaurant.json"
    outfile = open (finalReviewJsonFile,"w")
    data = []
    rowcnt = 0
    #Filter out review data for business ids in pittsburgh
    with open(reviewJsonFile, 'r') as f:
        for row in f:
            rowcnt = rowcnt + 1           
            if ast.literal_eval(row)["business_id"] in bus_id:                
                data.append(row)
    
    #Write data to the file  
    for item in data:
        outfile.write(item)
    
    

