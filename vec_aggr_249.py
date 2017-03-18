from word2vec_c import Word2Vec
import numpy as np
from scipy import spatial
from sklearn.neighbors import KNeighborsClassifier


def load_doc_vec(path):
    vecs = []  # list of entity vector lists
    X = []  # vectors for every documents (mean of entity vectors)

    for line in open(path):
        line = line.rstrip('\n').split('\t')
        docs.append(line)

    print
    "tags_id loaded"

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
    "all mean_vecs:", str(len(X))
    return X


model = Word2Vec.load_word2vec_format(fname='wiki_vec300.bin', binary=True)
pairs = []

vecs = []  # list of entity vector lists
X = []  # vectors for every documents (mean of entity vectors)
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

X_train=load_doc_vec('249train_tags_id.txt')

y_train = []  # categories
with open('249train_cate.txt') as f_cate:
    for c in f_cate:
        c = int(c.rstrip('\n'))
        y_train.append(c)

# kNN classification
neigh = KNeighborsClassifier(n_neighbors=10, weights = 'uniform')
neigh.fit(X_train, y_train)

X_test=load_doc_vec('249test_tags_id.txt')
y_test=[]
with open('249test_cate.txt') as f_cate2:
    for c in f_cate2:
        c = int(c.rstrip('\n'))
        y_test.append(c)
y_predict=neigh.predict(X_test)
N_test=len(y_test)

n_error=len(np.nonzero(y_predict-y_test))
accuracy=1- n_error/N_test
print accuracy