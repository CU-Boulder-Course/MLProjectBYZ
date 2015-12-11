# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:25:18 2015

@author: BYZ
"""

import json
from sklearn.feature_extraction.text import CountVectorizer

train_data_file_dir = "../data/post_train_v1.csv"

def get_train_words(filename):
    train_words = []    
    with open(filename) as data_file:    
        train_data = json.load(data_file)        
    for key in train_data.keys():
        train_words.append(" ".join(train_data[key]['words']) )        
    return train_words

def get_train_answer(filename):
    train_answer = []    
    with open(filename) as data_file:    
        train_data = json.load(data_file)        
    for key in train_data.keys():
        train_answer.append(train_data[key]['answer'])        
    return train_answer    


if __name__ == "__main__":
    train_words = get_train_words('../data/post_train_v1.json')
    train_answer = get_train_answer('../data/post_train_v1.json')

    vectorizer = CountVectorizer()
    train_data = vectorizer.fit_transform(train_words)

    print type(train_data)
