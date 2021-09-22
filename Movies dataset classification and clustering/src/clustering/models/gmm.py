from sklearn.base import DensityMixin, BaseEstimator
import numpy as np
from sklearn.mixture import GaussianMixture


class GMM(DensityMixin, BaseEstimator):
    def __init__(self, cluster_count: int, max_iteration: int, covariance_type: str):
        self.cluster_count = cluster_count
        self.max_iteration = max_iteration
        self.covariance_type = covariance_type

    def fit(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.X_ = l
        self.clf = GaussianMixture(n_components=self.cluster_count, max_iter=self.max_iteration,
                                   covariance_type=self.covariance_type)
        self.clf.fit(self.X_)
        return self

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        X = np.array(l)
        return self.clf.predict(X)
