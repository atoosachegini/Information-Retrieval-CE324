import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator
import json


def related_article_topic(list_of_topics, articles):
    number_of_articles = 2000
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
    return articles_profiles


def similar_users(user_id, matrix, k=3):
    user = matrix[matrix.index == user_id]
    other_users = matrix[matrix.index != user_id]
    similarities = cosine_similarity(user, other_users)[0].tolist()
    indices = other_users.index.tolist()
    index_similarity = dict(zip(indices, similarities))
    index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1))
    index_similarity_sorted.reverse()
    top_users_similarities = index_similarity_sorted[:k]
    users = [u[0] for u in top_users_similarities]
    return users


def recommend_item(similar_user_indices, matrix):
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    similar_users = similar_users.mean(axis=0)
    similar_users_df = pd.DataFrame(similar_users, columns=['mean'])
    similar_users_df_ordered = similar_users_df.sort_values(by=['mean'], ascending=False)
    best_items = similar_users_df_ordered.index.tolist()
    return best_items, similar_users


def recommended_articles(user_index, N, users_data, list_of_topics, articles):
    similar_user_indices = similar_users(user_index, users_data, k=N)
    recommend_topics, new_user = recommend_item(similar_user_indices, users_data)
    articles_profiles = related_article_topic(list_of_topics, articles)
    best_articles = []
    for i in recommend_topics:
        if len(best_articles) >= 10:
            break
        index = list_of_topics.index(i)
        for j in range(len(articles_profiles)):
            if articles_profiles[j][index] == 1:
                best_articles.append(articles[j]["id"])
    return best_articles[-10:], new_user


def CFMain(user_index, N):
    users_data = pd.read_csv("data.csv")
    users_data = users_data.fillna(0)
    users_data = users_data.iloc[0:10000, :]
    list_of_topics = list(users_data.columns.values)
    fname = "CrawledPapers.json"
    f = open(fname, )
    articles = json.load(f)
    best_articles, normalized_user_profile = recommended_articles(user_index, N, users_data, list_of_topics, articles)
    return best_articles, normalized_user_profile


# a, b = CFMain(4, 10)
# print(a)
# print(list(b))
