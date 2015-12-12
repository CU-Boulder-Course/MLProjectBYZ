from csv import DictReader
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from random import sample

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer

def tokenize_stem(vectorizer, s):
#    vectorizer = CountVectorizer(token_pattern=u'(?u)\\b\\w\\w+\\b', max_features=None)
    tokenizer= vectorizer.build_tokenizer()
    str1= tokenizer(s)
    rs= [ss for ss in str1 if ss not in stopwords.words('english')]
    
#    res_t = ' '.join(rs)
    
#    stemmer=PorterStemmer()
#    res_t = " ".join([ stemmer.stem(kw) for kw in rs])

#    wordnet_lemmatizer=WordNetLemmatizer()
#    res_t = " ".join([ wordnet_lemmatizer.lemmatize(kw) for kw in rs])

#    lancaster_stemmer = LancasterStemmer()
#    res_t = " ".join([ lancaster_stemmer.stem(kw) for kw in rs])

    snowball_stemmer = SnowballStemmer('english')
    res_t = " ".join([ snowball_stemmer.stem(kw) for kw in rs])        
    return res_t


#get external data
#read from file
def get_external_data(filename):
    external_d = {}
    o = DictReader(open(filename), ["answer",  "question"])

    for row in o:
        external_d[row['answer']] = row['question']

    return external_d


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
    vectorizer = CountVectorizer(token_pattern=u'(?u)\\b\\w\\w+\\b', max_features=None)    
    
    n_data = 5441; percentage = 0.1
    train, test = get_cross_validation('../original_data/sci_train.csv', n_data, percentage)
    
#    external_data1 = get_external_data('../data/wiki.csv')
    external_data3 = get_external_data('../data/wiki_v3_1.csv')
    
#    external_data_xz = get_external_data('../data/wikitrainxz.csv')
    
#    for key in external_data1:
#        train[key] += [external_data1[key].decode('utf-8')]
#        train[key] = [' '.join(train[key])]
    
    for key in external_data3:
        train[key] += [external_data3[key].decode('utf-8')]
        train[key] = [' '.join(train[key])]

#    for key in external_data_xz:
#        train[key] += [external_data_xz[key].decode('latin-1')]
#        train[key] = [' '.join(train[key])]
    
#    #tokenize
#    for key in train:
#        train[key] = [tokenize_stem(vectorizer, ' '.join(train[key]))]

    correct_predict = 0
    threshold_counter = 0
    len_counter = 0
    for key in test.keys():
        documents = []
        answer = []
        for choice in ['answerA', 'answerB', 'answerC', 'answerD']:
            if test[key][choice] in train.keys():
                #tokenize and stem here
                documents += [tokenize_stem(vectorizer, ''.join(train[test[key][choice]]) ) ]
#                documents += train[test[key][choice]]
                answer.append(choice)
                
        #test question is the last in the document
        #tokenize and stem here
        documents += [tokenize_stem(vectorizer, test[key]['question']) ]
#        documents += [test[key]['question']]
        
        #calculate weight        
        weight = calculate_weight(documents)
        print weight

        if(max(weight) < 0.01):
            threshold_counter += 1
        
        pred = answer[weight.argsort()[-1]][-1]

        if pred == test[key]['correctAnswer']:
            correct_predict += 1
#        else:
#            print 'answerA', test[key]['answerA']
#            print 'answerB', test[key]['answerB']
#            print 'answerC', test[key]['answerC']
#            print 'answerD', test[key]['answerD']
#            print 'correctAnswer', test[key]['answer'+test[key]['correctAnswer']]
#            print 'pred', test[key]['answer'+pred]
#            print 'weight', weight
            
        if(len(weight)<4):
            len_counter += 1
    
    print float(correct_predict)/float(len(test.keys()))
    print float(threshold_counter)/float(len(test.keys()))
    print float(len_counter)/float(len(test.keys()))
    
#    print tokenize_stem(vectorizer, "statistical mechanics statistical statistical statistical")



