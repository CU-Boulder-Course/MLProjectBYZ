from csv import DictReader, DictWriter
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import csv
import json
from collections import defaultdict


punct = set(string.punctuation)
stop = stopwords.words('english')
stemmer = WordNetLemmatizer()

d = defaultdict(dict)

for row in DictReader(open('../sci_test.csv')):
	words = []
	raw = row['question'].lower()
	sent = ''.join(ch for ch in raw if ch not in punct).split()
	for w in sent:
		ws = stemmer.lemmatize(w)
		if ws not in stop:
			words.append(ws)

	d[row['id']]['words'] = words
	d[row['id']]['answerA'] = row['answerA']
	d[row['id']]['answerB'] = row['answerB']
	d[row['id']]['answerC'] = row['answerC']
	d[row['id']]['answerD'] = row['answerD']

json.dump(d, open('../post_test.json', 'w'))
