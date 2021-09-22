from sklearn.base import TransformerMixin, ClusterMixin, BaseEstimator
import numpy as np


def cosine_distance(x1, x2):
    distance = 1 - np.dot(x1, x2) / np.sqrt(np.dot(x1, x1) * np.dot(x2, x2))
    return distance


class KMeans(TransformerMixin, ClusterMixin, BaseEstimator):
    def __init__(self, cluster_count: int, max_iteration: int, tolerance, distance_type: str):
        self.cluster_count = cluster_count
        self.max_iteration = max_iteration
        self.tolerance = tolerance
        self.distance_type = distance_type

    def fit(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        self.X_ = np.array(l)
        self.centroids = {}
        for i in range(self.cluster_count):
            self.centroids[i] = self.X_[i]
        for i in range(self.max_iteration):
            self.clfs = {}
            for i in range(self.cluster_count):
                self.clfs[i] = []
            for data in self.X_:
                dists = list()
                if self.distance_type == 'norm':
                    dists = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
                if self.distance_type == 'cos':
                    dists = [cosine_distance(data, self.centroids[centroid]) for centroid in self.centroids]
                clf = dists.index(min(dists))
                self.clfs[clf].append(data)

            before = dict(self.centroids)

            for cl in self.clfs:
                self.centroids[cl] = np.average(self.clfs[cl], axis=0)
            end = True
            for c in self.centroids:
                original_centroid = before[c]
                current_centroid = self.centroids[c]
                if np.sum((current_centroid - original_centroid) / original_centroid * 100.0) > self.tolerance:
                    end = False

            if end:
                break

    def predict(self, x):
        l = []
        for i in range(len(x)):
            l.append(x[i])
        l = np.array(l)
        classs = []
        for test in l:
            dists = []
            if self.distance_type == 'norm':
                dists = [np.linalg.norm(test - self.centroids[centroid]) for centroid in self.centroids]
            if self.distance_type == 'cos':
                dists = [cosine_distance(test, self.centroids[centroid]) for centroid in self.centroids]
            classification = dists.index(min(dists))
            classs.append(classification)
        return classs
