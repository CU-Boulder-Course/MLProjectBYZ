import json
from collections import defaultdict
import operator
from csv import DictWriter


if __name__ == '__main__':
    with open('../data/trained_coef_v1.json') as data_file:    
        trained_coef_o = json.load(data_file)
    #print dict_o['expands']['Femur']
        
    ##load test data
    with open('../data/post_test_v1.json') as test_data:
        test_o= json.load(test_data)
        
    test_score_o= defaultdict(lambda:defaultdict(int))
    
    for d in test_o.keys():
        test_score_o[d]['A']=0
        test_score_o[d]['B']=0
        test_score_o[d]['C']=0
        test_score_o[d]['D']=0        
        test_score_o[d]['answer']=None        
        
        for word in test_o[d]['words']:
            # find word in coef table            
            if word in trained_coef_o.keys():
                # find feature in coef table
                if test_o[d]['answerA'] in trained_coef_o[word].keys():                               
                    test_score_o[d]['A']+= trained_coef_o[word][test_o[d]['answerA'] ]
                    
        for word in test_o[d]['words']:
            # find word in coef table            
            if word in trained_coef_o.keys():
                # find feature in coef table
                if test_o[d]['answerB'] in trained_coef_o[word].keys():                               
                    test_score_o[d]['B']+= trained_coef_o[word][test_o[d]['answerB'] ]
                    
        for word in test_o[d]['words']:
            # find word in coef table            
            if word in trained_coef_o.keys():
                # find feature in coef table
                if test_o[d]['answerC'] in trained_coef_o[word].keys():                               
                    test_score_o[d]['C']+= trained_coef_o[word][test_o[d]['answerC'] ]
                    
        for word in test_o[d]['words']:
            # find word in coef table            
            if word in trained_coef_o.keys():
                # find feature in coef table
                if test_o[d]['answerD'] in trained_coef_o[word].keys():                               
                    test_score_o[d]['D']+= trained_coef_o[word][test_o[d]['answerD'] ]
                    
    for d in test_score_o.keys():
        dict_temp= {'A':test_score_o[d]['A'], 'B':test_score_o[d]['B'], 'C':test_score_o[d]['C'], 'D':test_score_o[d]['D']}
        test_score_o[d]['answer']= max(dict_temp.iteritems(), key=operator.itemgetter(1))[0]


    o = DictWriter(open("../data/predictions_v1.csv", 'wb'), ["id",  "correctAnswer"])
    o.writeheader()
    for d in test_score_o.keys():
        d = {'id': d, 'correctAnswer': test_score_o[d]['answer']}
        o.writerow(d)        

    
            
    
    