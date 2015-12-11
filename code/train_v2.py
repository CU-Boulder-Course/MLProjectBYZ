import json
from collections import defaultdict

with open("../data/numberOfTopics.json") as numberOfTopic_file:
    numTopics= json.load(numberOfTopic_file)['numberOfTopics']
topics= list()
for i in xrange(numTopics):
    topics.append("topic"+str(i))

if __name__== "__main__":
    with open('../data/post_train_v2.json') as data_file:    
        train_data = json.load(data_file)
    
    dict_o= defaultdict(lambda:defaultdict(int))
    
  
    for d in train_data.keys():
        for word in topics:
            #add the weight of topics
            dict_o[word][train_data[d]['answer'] ] += abs(train_data[d][word])

#    print dict_o['expands']['Femur']
    
    json.dump(dict_o, open('../data/trained_coef_v2.json', 'w'))
    
    