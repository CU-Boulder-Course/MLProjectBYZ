# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:25:18 2015

@author: BYZ
"""

import wikipedia

from csv import DictReader, DictWriter

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


if __name__ == "__main__":
    AnswerSet = get_answer_words('../../original_data/sci_train.csv', '../../original_data/sci_test.csv')

    o = DictWriter(open("../../data/wiki_v2.csv", 'wb'), ["answer",  "question"])
    o.writeheader()
    
    for i in xrange(len(AnswerSet)):
        print i
        answer = AnswerSet[i]
        print "answer", answer
        search = wikipedia.search(answer)
        print "search[0]", search[0]
        try:
            page = wikipedia.page(title=search[0], pageid=None, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as de:
            print "de.options", de.options
            page = wikipedia.page(title=de.options[0], pageid=None, auto_suggest=False)            
            
        question = str(page.content.encode('utf-8')).split('\n')[0]
        print question
    
        d = {'answer': answer, 'question': question}
        o.writerow(d)
