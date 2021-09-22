from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


def cosine_distance(x1, x2):
    distance = 1 - np.dot(x1, x2) / np.sqrt(np.dot(x1, x1) * np.dot(x2, x2))
    return distance


class KNN(BaseEstimator, ClassifierMixin):
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        l = []
        for i in range(len(X)):
            l.append(X[i])
        self.X_ = np.array(l)
        self.y_ = np.array(y)
        return self

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        X = np.array(l)
        return np.array(list(map(self.predictS, X)))

    def predictS(self, x):  # input: x->np_array(1*D)       output: one label
        labels = self.get_neighbors_labels(x, self.k)
        return max(set(labels), key=labels.count)

    def get_neighbors_labels(self, x, k):
        distances = list()
        for train_x, train_y in zip(self.X_, self.y_):
            dist = cosine_distance(x, train_x)
            distances.append((train_y, dist))
        distances.sort(key=lambda t: t[1])
        return [t[0] for t in distances[:k]]
