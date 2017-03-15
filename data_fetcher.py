from sklearn.datasets import fetch_20newsgroups
import numpy as np


class DataFetcher:
    def __init__(self, balanced_categories=None, imbalanced_categories=None, discard=0):
        self.balanced_categories = balanced_categories
        self.imbalanced_categories = imbalanced_categories
        self.discard = discard

    def set_balanced_categories(self, balanced_categories):
        self.balanced_categories = balanced_categories

    def set_imbalanced_categories(self, imbalanced_categories):
        self.imbalanced_categories = imbalanced_categories

    def set_discard(self, discard):
        self.discard = discard

    def get_data(self):
        """
        balanced_categories are the balanced topics.
        imbalanced_categories are the imbalanced topics.
        d is the fraction of the documents to discard for the imbalanced topics.
        If no params given then all the data will be fetched.
        If only balanced categories are given then only those will be fetched.
        """
        if self.imbalanced_categories == None:
            if self.balanced_categories == None:
                dataset = fetch_20newsgroups(subset='all', shuffle=True, random_state=1,
                                             remove=('headers', 'footers', 'quotes'))
                return dataset
            else:
                dataset = fetch_20newsgroups(subset='all', categories=self.balanced_categories, shuffle=True,
                                             random_state=1, remove=('headers', 'footers', 'quotes'))
                return dataset.data
        else:
            documents = fetch_20newsgroups(subset='all', categories=self.balanced_categories, shuffle=True,
                                           random_state=1, remove=('headers', 'footers', 'quotes')).data
            for c in self.imbalanced_categories:
                # shuffle=False to get a consistent imbalanced dataset
                docs = fetch_20newsgroups(subset='all', categories=[c], shuffle=False, random_state=1,
                                          remove=('headers', 'footers', 'quotes')).data
                documents += docs[:int(len(docs) * (1 - self.discard))]
            np.random.shuffle(documents)
            return documents

    def get_classified_training_data(self):
        """
        balanced_categories are the balanced topics.
        imbalanced_categories are the imbalanced topics.
        d is the fraction of the documents to discard for the imbalanced topics.
        If no params given then all the data will be fetched.
        If only balanced categories are given then only those will be fetched.
        """
        if self.imbalanced_categories == None:
            if self.balanced_categories == None:
                dataset = fetch_20newsgroups(subset='train', shuffle=False, random_state=1,
                                             remove=('headers', 'footers', 'quotes'))
                return [dataset.data, dataset.target]
            else:
                dataset = fetch_20newsgroups(subset='train', categories=self.balanced_categories, shuffle=True,
                                             random_state=1, remove=('headers', 'footers', 'quotes'))
                return dataset.data
        else:
            documents = fetch_20newsgroups(subset='train', categories=self.balanced_categories, shuffle=True,
                                           random_state=1, remove=('headers', 'footers', 'quotes')).data
            for c in self.imbalanced_categories:
                # shuffle=False to get a consistent imbalanced dataset
                docs = fetch_20newsgroups(subset='train', categories=[c], shuffle=False, random_state=1,
                                          remove=('headers', 'footers', 'quotes')).data
                documents += docs[:int(len(docs) * (1 - self.discard))]
            np.random.shuffle(documents)
            return documents