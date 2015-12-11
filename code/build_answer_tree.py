# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:25:18 2015

@author: BYZ
"""
from collections import defaultdict
from csv import DictReader, DictWriter
import re



#take text, reaturn dict[name]= label
#this can be done using vectorizer
def text_to_dict():
    return dict()
    
#build tree, take a list of labels as input
def create_tree(label):
    tree= []
    return tree
    
#take tree and list of word label as input, return a distinct number as it's label
def get_label_from_word_id():
    return 0
    
#take tree and text as input, return a distinct number as it's label
def get_label_from_text():
    return 0
    
"""
    return category if a answer has one
    category should have the form
    Hamiltonian (quantum mechanics)
    group (mathematics)
    
"""
def get_category(answer):
    if re.search(r'(?<=\()(.+)(?=\))', answer) is None:
        return ""
    else:
        return re.search(r'(?<=\()(.+)(?=\))', answer).group()   

if __name__ == "__main__":
    d = defaultdict(dict)
    answer_words = set()
    category = set()
        
    for row in DictReader(open('../original_data/sci_train.csv')):
        category.add(get_category(row['answerA'].lower()))
        category.add(get_category(row['answerB'].lower()))
        category.add(get_category(row['answerC'].lower()))
        category.add(get_category(row['answerD'].lower()))
        
        answer_words.add(row['answerA'].lower())
        answer_words.add(row['answerB'].lower())
        answer_words.add(row['answerC'].lower())
        answer_words.add(row['answerD'].lower())
      
    answer_words = list(answer_words)
    category = list(category)



 
   
    
    

