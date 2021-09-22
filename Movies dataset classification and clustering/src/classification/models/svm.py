from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn import svm
import numpy as np


class SVM(BaseEstimator, ClassifierMixin):
    def __init__(self, c):
        self.c = c

    def fit(self, x, y):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.X_ = np.copy(np.array(l))
        self.y_ = np.copy(np.array(y))
        self.clf = svm.SVC(C=self.c)
        self.clf.fit(self.X_, self.y_)
        return self

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        X = np.array(l)
        return self.clf.predict(X)
