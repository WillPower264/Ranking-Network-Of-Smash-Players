# test.py - test script for pageranker.py

from pageranker import PageRanker
import networkx as nx
import sys

ranker = PageRanker('ultimate_sets_clean.csv',
                    'ultimate_player_ids.csv')

el = ranker.build_edgelist()
g = ranker.build_digraph(el)
pr = ranker.pagerank(g)
pr_sort = ranker.pagerank_sort(pr)
ranker.pagerank_write(pr_sort)

print(ranker.leaderboard(20))

print("Number of edges:")
print(g.size())
print("Number of nodes:")
print(g.order())
print("Number of weakly connected components")
print(nx.number_weakly_connected_components(g))