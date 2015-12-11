import json
from collections import defaultdict


if __name__== "__main__":
    with open('../data/post_train_v1.json') as data_file:    
        train_data = json.load(data_file)
    
    dict_o= defaultdict(lambda:defaultdict(int))
    
    for d in train_data.keys():
        for word in train_data[d]['words']:
            dict_o[word][train_data[d]['answer'] ] +=1

#    print dict_o['expands']['Femur']
    
    json.dump(dict_o, open('../data/trained_coef_v1.json', 'w'))
    
    