import json
import numpy as np


class Graph:
    def __init__(self):
        self.nodes = []

    def contains(self, name):
        for node in self.nodes:
            if node.name == name:
                return True
        return False

    def find(self, name):
        if not self.contains(name):
            new_node = Node(name)
            self.nodes.append(new_node)
            return new_node
        else:
            return next(node for node in self.nodes if node.name == name)

    def add_edge(self, parent, child):
        parent_node = self.find(parent)
        child_node = self.find(child)
        parent_node.link_child(child_node)
        child_node.link_parent(parent_node)

    def sort_nodes(self):
        self.nodes.sort(key=lambda node: node.name)

    def normalize_auth_hub(self):
        auth_sum = sum(node.auth for node in self.nodes)
        hub_sum = sum(node.hub for node in self.nodes)

        for node in self.nodes:
            node.auth /= auth_sum
            node.hub /= hub_sum


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.auth = 1.0
        self.hub = 1.0

    def link_child(self, new_child):
        for child in self.children:
            if child.name == new_child.name:
                return None
        self.children.append(new_child)

    def link_parent(self, new_parent):
        for parent in self.parents:
            if parent.name == new_parent.name:
                return None
        self.parents.append(new_parent)

    def update_auth(self):
        self.auth = sum(node.hub for node in self.parents)

    def update_hub(self):
        self.hub = sum(node.auth for node in self.children)


def init_graph(fname):
    f = open(fname, )
    articles = json.load(f)
    graph = Graph()
    for article1 in articles:
        for article2 in articles:
            for authorX in article1["authors"]:
                for authorY in article2["authors"]:
                    if (article2["id"] in article1["references"]) and (authorX != authorY):
                        graph.add_edge(authorX, authorY)
    graph.sort_nodes()
    return graph


def HITS_one_iter(graph):
    node_list = graph.nodes
    for node in node_list:
        node.update_auth()
    for node in node_list:
        node.update_hub()
    graph.normalize_auth_hub()


def HITS(graph, iteration=5):
    for i in range(iteration):
        HITS_one_iter(graph)


def HITSMain(number_of_best_authors=10):
    iteration = 5
    graph = init_graph('CrawledPapers.json')
    HITS(graph, iteration)
    authorities = {}
    for node in graph.nodes:
        authorities[node.name] = node.auth
    sorted_authorities = sorted(authorities.items(), key=lambda x: x[1], reverse=True)
    with open('HITStest.json', 'w') as f:
        json.dump(sorted_authorities, f)
    best_authors = {}
    for i in range(number_of_best_authors):
        best_authors[sorted_authorities[i][0]] = str(sorted_authorities[i][1])
    return best_authors


best_authors = HITSMain()
# print(best_authors)
