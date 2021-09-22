import typing as th
import numpy as np
from sklearn import metrics
from sklearn.metrics.cluster import adjusted_rand_score


def purity(y, y_hat):
    contingency_matrix = metrics.cluster.contingency_matrix(y, y_hat)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)


def adjusted_rand_index(y, y_hat) -> float:
    return adjusted_rand_score(y, y_hat)


evaluation_functions = dict(purity=purity, adjusted_rand_index=adjusted_rand_index)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
