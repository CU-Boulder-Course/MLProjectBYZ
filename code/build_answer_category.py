# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:25:18 2015

@author: BYZ
"""

import re
from collections import defaultdict
from csv import DictReader

"""
    return category if a answer has one
    category should have the form
    Hamiltonian (quantum mechanics)
    group (mathematics)
    doesn't have one, return "", represents other category
    
"""

def get_category(answer):
    if re.search(r'(?<=\()(.+)(?=\))', answer) is None:
        return ""
    else:
        return re.search(r'(?<=\()(.+)(?=\))', answer).group()
        
#return category
def get_category_words(train_filename):
    category = set()   
    for row in DictReader(open(train_filename)):
        category.add(get_category(row['answerA'].lower()))
        category.add(get_category(row['answerB'].lower()))
        category.add(get_category(row['answerC'].lower()))
        category.add(get_category(row['answerD'].lower()))

    category = list(category)
    return category
        
#return answer words
def get_answer_words(train_filename, test_filename):
    answer_words = set()
    for row in DictReader(open(train_filename)):
        answer_words.add(row['answer'+str(row['correctAnswer'])].lower())
        
    for row in DictReader(open(test_filename)):  
        answer_words.add(row['answerA'].lower())
        answer_words.add(row['answerB'].lower())
        answer_words.add(row['answerC'].lower())
        answer_words.add(row['answerD'].lower())
    
    return list(answer_words)
    

train_data_file_dir = '../original_data/sci_train.csv'
test_data_file_dir = '../original_data/sci_test.csv'

if __name__ == "__main__":
#      
      
    answer_words = get_answer_words(train_data_file_dir, test_data_file_dir)
    answer_category = get_category_words(train_data_file_dir)
