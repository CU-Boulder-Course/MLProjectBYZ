from csv import DictReader, DictWriter
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer



#get external data
#read from file
def get_external_data(filename):
    external_d = {}
    o = DictReader(open(filename), ["answer",  "question"])

    for row in o:
        external_d[row['answer']] = row['question']

    return external_d


def get_train_data(filename):
    #1D dict
    train = defaultdict(list);
    for row in DictReader(open(filename)):
        train[row['answer'+str(row['correctAnswer'])]] += [row['question']]
    
    #might have multiple list, join them to a sentence
    for key in train.keys():
        train[key] = [' '.join(train[key])]

    return train

def get_test_data(filename):
    test = defaultdict(dict)
    for row in DictReader(open(filename)):
        test[row['id']]['answerA'] = row['answerA']
        test[row['id']]['answerB'] = row['answerB']
        test[row['id']]['answerC'] = row['answerC']
        test[row['id']]['answerD'] = row['answerD']
        test[row['id']]['question'] = row['question']
    return test

    
#calculate weight from a list of document
def calculate_weight(document):
    #n-gram of n-gram
    vect = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(1, 3))
    tfidf = vect.fit_transform(document)    
    #every word in the text has same weight        
    
    #prediction, first -1 represents comparison with test question,
    #second -1 exclude the test question itself, .A convert matrix to 2D array
    #argsort return index, in ascending order of corresponding element value
    #the last -1 take out the 'A', 'B', 'C' or 'D' of sting like 'answerA'    
    weight = (tfidf * tfidf.T).A[-1][:-1]        
    return weight
     
if __name__ == "__main__":
    train = get_train_data('../original_data/sci_train.csv')
    test = get_test_data('../original_data/sci_test.csv')
    
    external_data1 = get_external_data('../data/wiki.csv')
#    external_data2 = get_external_data('../data/wiki_v2.csv')
    external_data3 = get_external_data('../data/wiki_v3.csv')
    
    for key in external_data1:
        train[key] += [external_data1[key].decode('utf-8')]
        train[key] = [' '.join(train[key])]
        
    for key in external_data3:
        train[key] += [external_data3[key].decode('utf-8')]
        train[key] = [' '.join(train[key])]        

    correct_predict = 0
    o = DictWriter(open("../data/predictions_v4.csv", 'wb'), ["id",  "correctAnswer"])
    o.writeheader()
    
    for key in test.keys():
        documents = []
        answer = []
        for choice in ['answerA', 'answerB', 'answerC', 'answerD']:
            if test[key][choice] in train.keys():
                documents += train[test[key][choice]]
                answer.append(choice)
                
        #test question is the last in the document
        documents += [test[key]['question']]
        
        #calculate weight        
        weight = calculate_weight(documents)
#        print weight        
        
        prediction = answer[weight.argsort()[-1]][-1]
   
        d = {'id': key, 'correctAnswer': prediction}
        o.writerow(d)    



