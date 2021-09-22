from sklearn.base import ClusterMixin, BaseEstimator
from sklearn.cluster import AgglomerativeClustering
import numpy as np


class Hierarchical(ClusterMixin, BaseEstimator):
    def __init__(self, cluster_count: int, affinity: str):
        self.cluster_count = cluster_count
        self.affinity = affinity

    def fit_predict(self, x, **kwargs):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.X_ = np.array(l)
        cluster = AgglomerativeClustering(n_clusters=self.cluster_count, affinity=self.affinity, linkage='ward')
        cluster.fit_predict(self.X_)
        return cluster.labels_
