import json


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
        self.nodes.sort(key=lambda node: int(node.name))

    def normalize_pagerank(self):
        pagerank_sum = sum(node.pagerank for node in self.nodes)
        for node in self.nodes:
            node.pagerank /= pagerank_sum


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.pagerank = 1.0

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

    def update_pagerank(self, alpha, n):
        in_neighbors = self.parents
        pagerank_sum = sum((node.pagerank / len(node.children)) for node in in_neighbors)
        random_jumping = alpha / n
        self.pagerank = random_jumping + (1 - alpha) * pagerank_sum


def init_graph(fname):
    f = open(fname, )
    articles = json.load(f)
    graph = Graph()
    for article in articles:
        for ref in article["references"]:
            graph.add_edge(article["id"], ref)
    graph.sort_nodes()
    return graph


def PageRank_one_iter(graph, alpha):
    node_list = graph.nodes
    for node in node_list:
        node.update_pagerank(alpha, len(graph.nodes))


def PageRank(graph, alpha, iteration=100):
    for i in range(iteration):
        PageRank_one_iter(graph, alpha)


def pageRankMain(alpha):
    iteration = 100
    graph = init_graph('CrawledPapers.json')
    graph.normalize_pagerank()
    PageRank(graph, alpha, iteration)
    pageRanks = {}
    for node in graph.nodes:
        pageRanks[node.name] = node.pagerank
    with open('PageRank.json', 'w') as f:
        json.dump(pageRanks, f)


pageRankMain(0.15)
