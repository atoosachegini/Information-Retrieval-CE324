import typing as th


def accuracy(y, y_hat) -> float:
    count = 0
    for i in range(len(y)):
        if y[i] == y_hat[i]:
            count += 1
    return round(count / len(y), 3)


def precision(y, y_hat, label=1) -> float:
    soorat = 0
    for i in range(len(y)):
        if y[i] == label:
            if y_hat[i] == label:
                soorat += 1
    makhraj = 0
    for i in range(len(y_hat)):
        if y_hat[i] == label:
            makhraj += 1
    return round(soorat/makhraj, 3)


def recall(y, y_hat, label=1) -> float:
    makhraj = 0
    soorat = 0
    for i in range(len(y)):
        if y[i] == label:
            makhraj += 1
            if y_hat[i] == label:
                soorat += 1
    return round(soorat/makhraj, 3)


def f1(y, y_hat, beta: float = 1., alpha: float = 0.5, label=1):
    prec = precision(y, y_hat, label)
    rec = recall(y, y_hat, label)
    f1 = (1 + beta * beta) * (prec * rec) / (beta * beta * prec + rec)
    return round(f1, 3)


def evaluate(y, y_hat, alpha, beta) -> th.Dict[str, float]:
    evaluations = {'accuracy': accuracy(y, y_hat), 'f1_pos': f1(y, y_hat, beta, alpha, 1), 'f1_neg': f1(y, y_hat, beta, alpha, 0),
                   'precision_pos': precision(y, y_hat, 1), 'recall_pos': recall(y, y_hat, 1), 'precision_neg': precision(y, y_hat, 0), 'recall_neg': recall(y, y_hat, 0)}
    return evaluations
