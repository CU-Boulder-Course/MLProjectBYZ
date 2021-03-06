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
        answer_words.add(row['answerA'])
        answer_words.add(row['answerB'])
        answer_words.add(row['answerC'])
        answer_words.add(row['answerD'])
        
    for row in DictReader(open(test_filename)):  
        answer_words.add(row['answerA'])
        answer_words.add(row['answerB'])
        answer_words.add(row['answerC'])
        answer_words.add(row['answerD'])
    
    return list(answer_words)


if __name__ == "__main__":
    AnswerSet = get_answer_words('../../original_data/sci_train.csv', '../../original_data/sci_test.csv')

    fileHandler = open("../../data/wiki_v11_1.csv", 'wb')
    o = DictWriter(fileHandler, ["answer",  "question"])
    o.writeheader()
    
    questions= []
    print "size of AnswerSet", len(AnswerSet)
    
    for i in xrange(len(AnswerSet)):
#    for i in xrange(3):        
        print i
        answer = AnswerSet[i]
        print "answer", answer
        search = wikipedia.search(answer)
#        print "search[0]", search[0]
        question = ''
        for s in search[0:3]:
            print s
            try:
                page = wikipedia.page(title=s, pageid=None, auto_suggest=False)
            except wikipedia.exceptions.DisambiguationError as de:
                print "de.options", de.options
                if de.options[0] != s.lower():
                    page = wikipedia.page(title=de.options[0], pageid=None, auto_suggest=False)
                else:
                    print "Error", de.options[0]
                    continue
            
            question += ' '.join(str(page.content.encode('utf-8')).split('\n')[0:3])
#        print question        
        questions.append(question)
    
#    for i in xrange(3):
    for i in xrange(len(AnswerSet)):
        answer = AnswerSet[i]
        question = questions[i]    
        d = {'answer': answer, 'question': question}
        o.writerow(d)
        
    fileHandler.close()
   
