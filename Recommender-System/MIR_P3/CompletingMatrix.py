import pandas as pd
import numpy as np
import json


def CMMain(iterations=60):
    users_data = pd.read_csv("data.csv")
    users_data = users_data.fillna(0)
    users_data = users_data.iloc[0:10000, :]
    users_data = np.array(users_data)
    number_of_observed_values = 0
    for i in range(len(users_data)):
        for j in range(len(users_data[i])):
            if users_data[i][j] != 0:
                number_of_observed_values += 1
    number_of_test_values = int(0.2 * number_of_observed_values)
    train_users_data = np.array(users_data, copy=True)
    for i in range(len(train_users_data)):
        for j in range(len(train_users_data[i])):
            if (number_of_test_values != 0) and (train_users_data[i][j] != 0):
                train_users_data[i][j] = 0
                number_of_test_values -= 1

    n = 10000
    m = 34
    k = 2
    U, s, V = np.linalg.svd(train_users_data)
    sigma = [[0 for i in range(k)] for j in range(k)]
    for i in range(k):
        sigma[i][i] = s[i]
    q = V.T
    p = U[0:n, 0:k]
    q = q[0:k, 0:m]
    p = np.matmul(p, sigma)

    test_users_data = [[0 for i in range(m)] for j in range(n)]
    test_users_data = np.array(test_users_data)
    number_of_test_values = int(0.2 * number_of_observed_values)
    for i in range(len(users_data)):
        for j in range(len(users_data[i])):
            if (number_of_test_values != 0) and (users_data[i][j] != 0):
                test_users_data[i][j] = users_data[i][j]
                number_of_test_values -= 1

    # Train
    learning_rate = 0.00008
    train_losses = []
    for itr in range(iterations):
        ll = "iteration: " + str(itr)
        print(ll)
        for i in range(n):
            for t in range(2):
                sums = 0
                for j in range(m):
                    if train_users_data[i][j] != 0:
                        sums += (train_users_data[i][j] - np.dot(p[i], q.T[j])) * q[t][j]
                p[i][t] = p[i][t] + learning_rate * 2 * sums
        for t in range(2):
            for j in range(m):
                sums = 0
                for i in range(n):
                    if train_users_data[i][j] != 0:
                        sums += (train_users_data[i][j] - np.dot(p[i], q.T[j])) * p[i][t]
                q[t][j] = q[t][j] + learning_rate * 2 * sums
        m_tilda = np.matmul(p, q)
        xx = 0
        for i in range(len(train_users_data)):
            for j in range(len(train_users_data[i])):
                xx += (train_users_data[i][j] - m_tilda[i][j]) ** 2
        pp = "Train Error: " + str(xx)
        print(pp)
        train_losses.append(ll + " " + pp)
        # learning rate decay
        if itr % 5 == 0:
            learning_rate = learning_rate / 2

    # Test
    test_loss = 0
    m_tilda = np.matmul(p, q)
    for i in range(len(test_users_data)):
        for j in range(len(test_users_data[i])):
            test_loss += (test_users_data[i][j] - m_tilda[i][j]) ** 2
    test_loss = "Test Error: " + str(test_loss)
    print(test_loss)
    with open('train_losses.json', 'w') as f:
        json.dump(train_losses, f)
    with open('test_loss.json', 'w') as f:
        json.dump(test_loss, f)

    return train_losses, test_loss

    # Error on test dataset is 1280.33

# train_losses, test_loss = CMMain(5)
# print(train_losses)
# print(test_loss)
