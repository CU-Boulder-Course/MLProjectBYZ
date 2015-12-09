from csv import DictReader, DictWriter
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import csv
import json
from collections import defaultdict



# o = DictWriter(open('../post_train.csv', 'w'), ['id', 'words', 'answer'])
# o.writeheader()
punct = set(string.punctuation)
stop = stopwords.words('english')
stemmer = WordNetLemmatizer()

d = defaultdict(dict)

for row in DictReader(open('../sci_train.csv')):
	words = []
	raw = row['question'].lower()
	sent = ''.join(ch for ch in raw if ch not in punct).split()
	for w in sent:
		ws = stemmer.lemmatize(w)
		if ws not in stop:
			words.append(ws)

	if row['correctAnswer'] == 'A':
		answer = row['answerA']
	elif row['correctAnswer'] == 'B':
		answer = row['answerB']
	elif row['correctAnswer'] == 'C':
		answer = row['answerC']
	else:
		answer = row['answerD']

	d[row['id']]['words'] = words
	d[row['id']]['answer'] = answer
	# o.writerow({'id':row['id'], 'words': words, 'answer':answer})


json.dump(d, open('../post_train.json', 'w'))
