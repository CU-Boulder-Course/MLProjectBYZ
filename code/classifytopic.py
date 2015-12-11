# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause


from time import time
from csv import DictReader, DictWriter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
#from sklearn.datasets import fetch_20newsgroups
#import sys
import numpy as np

n_features = 5000
n_topics = 2
n_top_words = 50

# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

t0 = time()
print("Loading dataset and extracting TF-IDF features...")

question = []
for row in DictReader(open('../original_data/sci_train.csv')):
	question += [row['question']]

for row in DictReader(open('../original_data/sci_test.csv')):
	question += [row['question']]

#dataset = fetch_20newsgroups(shuffle=True, random_state=1,
#                             remove=('headers', 'footers', 'quotes'))

vectorizer = TfidfVectorizer(max_df=0.90, min_df=1, max_features=n_features,
                             stop_words='english')

tfidf = vectorizer.fit_transform(question)
print("done in %0.3fs." % (time() - t0))

# Fit the NMF model
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))

topics = []
for ii in nmf.transform(tfidf):
	topics.append(np.argsort(ii)[-1])

