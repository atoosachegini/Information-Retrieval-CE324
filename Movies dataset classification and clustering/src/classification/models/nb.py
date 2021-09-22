from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class NaiveBayes(BaseEstimator, ClassifierMixin):
    def __init__(self, kind):
        self.kind = kind

    def fit(self, x, y):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.x_ = np.array(l)
        self.y_ = np.array(y)
        self.priors_ = np.bincount(y) / len(y)
        self.n_classes_ = np.max(y) + 1
        if self.kind == 'gaussian':
            self.means_ = np.array([self.x_[np.where(y == i)].mean(axis=0) for i in range(self.n_classes_)])
            self.stds_ = np.array([self.x_[np.where(y == i)].std(axis=0) for i in range(self.n_classes_)])
            return self
        if self.kind == 'bernoulli':
            X = np.array(self.x_)
            yy = np.array(self.y_)
            self.meanss = np.array(X.mean(axis=0))
            self.medians = np.median(np.array(X), axis=0)
            self.stdd = np.array(X.std(axis=0))
            for i in range(len(X)):
                for j in range(256):
                    if X[i][j] > (self.meanss[j] / 1.1 + self.stdd[j] / 3.6):
                        X[i][j] = 0
                    else:
                        X[i][j] = 1
            count_sample = X.shape[0]
            separated = [[x for x, t in zip(X, yy) if t == c] for c in np.unique(yy)]
            self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
            count = np.array([np.array(i).sum(axis=0) for i in separated]) + 1
            smoothing = 2
            nn = np.array([len(i) + smoothing for i in separated])
            self.feature_prob_ = count / nn[np.newaxis].T
            return self

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        l = np.array(l)
        if self.kind == 'gaussian':
            res = []
            for i in range(len(l)):
                probas = []
                for j in range(self.n_classes_):
                    probas.append((1 / np.sqrt(2 * np.pi * self.stds_[j] ** 2) * np.exp(
                        -0.5 * ((l[i] - self.means_[j]) / self.stds_[j]) ** 2)).prod() * self.priors_[j])
                probas = np.array(probas)
                res.append(probas / probas.sum())
            res = np.array(res)
            return res.argmax(axis=1)
        if self.kind == 'bernoulli':
            for i in range(len(l)):
                for j in range(256):
                    if l[i][j] > (self.meanss[j] / 1.1 + self.stdd[j] / 3.6):
                        l[i][j] = 0
                    else:
                        l[i][j] = 1
            l = np.array(l)
            predicted = [(np.log(self.feature_prob_) * x + np.log(1 - self.feature_prob_) * np.abs(x - 1)).sum(
                axis=1) + self.class_log_prior_ for x in l]
            return np.argmax(predicted, axis=1)
