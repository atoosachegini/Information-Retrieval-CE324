from sklearn.neural_network import MLPClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class NeuralNetwork(BaseEstimator, ClassifierMixin):
    def __init__(self, iters, activation, hidden_layer_sizes=100, solver='adam'):
        self.iters = iters
        self.activation = activation
        self.hidden_layer_sizes = hidden_layer_sizes
        self.solver = solver

    def fit(self, x, y):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.X_ = np.copy(np.array(l))
        self.y_ = np.copy(np.array(y))
        self.clf = MLPClassifier(random_state=1, max_iter=self.iters, activation=self.activation,
                                 hidden_layer_sizes=self.hidden_layer_sizes, solver=self.solver)
        self.clf.fit(self.X_, self.y_)
        return self

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        X = np.array(l)
        return self.clf.predict(X)
