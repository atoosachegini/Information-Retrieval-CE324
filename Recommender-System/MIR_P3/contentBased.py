import json
import pandas as pd
import numpy as np


def length(l):
    m = 0
    for i in l:
        m += i ** 2
    return m ** 0.5


def cos_similarity(l1, l2):
    if length(l1) == 0 or length(l2) == 0:
        return 0
    c = 0
    for i in range(len(l1)):
        c += l1[i] * l2[i]
    cosine = c / float(length(l1) * length(l2))
    return cosine


def contentBasedRecSys(index, articles_profiles, users_data, articles):
    user_profile = users_data.iloc[index]
    user_cos_scores = []
    for article in range(len(articles_profiles)):
        user_cos_scores.append(cos_similarity(user_profile, articles_profiles[article]))
    sorted_scores = np.argsort(user_cos_scores)[-10:]
    reversed_sorted_scores = []
    for i in range(len(sorted_scores)):
        reversed_sorted_scores.append(sorted_scores[len(sorted_scores) - 1 - i])
    for i in range(len(reversed_sorted_scores)):
        reversed_sorted_scores[i] = articles[reversed_sorted_scores[i]]["id"]
    return list(reversed_sorted_scores)


def CBMain(ind):
    number_of_articles = 2000
    users_data = pd.read_csv("data.csv")
    fname = "CrawledPapers.json"
    f = open(fname, )
    articles = json.load(f)
    list_of_topics = list(users_data.columns.values)
    articles_profiles = [[0 for i in range(len(list_of_topics))] for j in range(number_of_articles)]

    for i in range(len(articles)):
        for topic in articles[i]["related_topics"]:
            if topic == "Artificial intelligence":
                articles_profiles[i][list_of_topics.index("AI")] = 1
            if "algorithm" in topic.lower():
                articles_profiles[i][list_of_topics.index("algorithms")] = 1
            if "computational" in topic.lower():
                articles_profiles[i][list_of_topics.index("computational science")] = 1
            if "computer architecture" in topic.lower():
                articles_profiles[i][list_of_topics.index("computer architecture")] = 1
            if "mining" in topic.lower():
                articles_profiles[i][list_of_topics.index("data mining")] = 1
            if "database" in topic.lower():
                articles_profiles[i][list_of_topics.index("database")] = 1
            if "machine learning" in topic.lower():
                articles_profiles[i][list_of_topics.index("machine learning")] = 1
            if "software engineering" in topic.lower():
                articles_profiles[i][list_of_topics.index("software engineering")] = 1
            for j in list_of_topics:
                if (topic.lower() in j) and (topic.lower() != "cognition" and j != "pattern recognition") \
                        and (topic.lower() != "Communication" and j != "telecommunications"):
                    articles_profiles[i][list_of_topics.index(j)] = 1
    users_data = users_data.fillna(0)
    return contentBasedRecSys(ind, articles_profiles, users_data, articles)

# print(CBMain(0))
