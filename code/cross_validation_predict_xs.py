from csv import DictReader
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from random import sample

#get cross_validation
#train data and test are in different format
def get_cross_validation(filename, n_data, percentage):
    test_sample = sample(range(0, n_data), int(percentage*n_data) )
    counts = 0
    #1D dict and 2D dict
    train = defaultdict(list); test = defaultdict(dict)
    for row in DictReader(open(filename)):
        if counts in test_sample:
            test[row['id']]['answerA'] = row['answerA']
            test[row['id']]['answerB'] = row['answerB']
            test[row['id']]['answerC'] = row['answerC']
            test[row['id']]['answerD'] = row['answerD']
            test[row['id']]['question'] = row['question']
            test[row['id']]['correctAnswer'] = row['correctAnswer']
        else:
            train[row['answer'+str(row['correctAnswer'])]] += [row['question']]
        
        counts += 1
    
    #might have multiple list, join them to a sentence
    for key in train.keys():
        train[key] = [' '.join(train[key])]
    
    return train, test
    
#calculate weight from a list of document
def calculate_weight(document):
    vect = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(1, 2))
    tfidf = vect.fit_transform(documents)    
    #every word in the text has same weight        
    
    #prediction, first -1 represents comparison with test question,
    #second -1 exclude the test question itself, .A convert matrix to 2D array
    #argsort return index, in ascending order of corresponding element value
    #the last -1 take out the 'A', 'B', 'C' or 'D' of sting like 'answerA'    
    weight = (tfidf * tfidf.T).A[-1][:-1]        
    return weight
     
if __name__ == "__main__":
    n_data = 5441; percentage = 0.1
    train, test = get_cross_validation('../original_data/sci_train.csv', n_data, percentage)

    correct_predict = 0
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
        
        pred = answer[weight.argsort()[-1]][-1]

        if pred == test[key]['correctAnswer']:
            correct_predict += 1
    
    print float(correct_predict)/float(len(test.keys()))
