from word2vec_c import Word2Vec
import numpy as np
from scipy import spatial
from sklearn.neighbors import KNeighborsClassifier



model = Word2Vec.load_word2vec_format(fname='wiki_vec300.bin', binary=True)
pairs = []

vecs = []  # list of entity vector lists
X = []  # vectors for every documents (mean of entity vectors)
w_vecs = []
docs = []


def try_hash(model, word):
    r = None
    try:
        r = model[word]
        return r
    except:
        return None


print
model['Eid1']

for line in open('249train_tags_id.txt'):
    line = line.rstrip('\n').split('\t')
    docs.append(line)

print
"249_training_tags_id loaded"

count = 1
for line in docs:
    new_vec = []
    for l in line:
        v = try_hash(model, l)
        if v != None:
            new_vec.append(v)
    vecs.append(new_vec)
    if len(new_vec) == 0:
        print
        count
    count += 1
    X.append(np.mean(new_vec, axis=0))

print
"all mean_vecs:", str(len(mean_vecs))

y = []  # categories
with open('249train_cate.txt') as f_cate:
    for c in f_cate:
        c = int(c.rstrip('\n'))
        y.append(c)

# kNN classification
neigh = KNeighborsClassifier(n_neighbors=10)
neigh.fit(X, y)


