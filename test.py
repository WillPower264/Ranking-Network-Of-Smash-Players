# test.py - test script for pageranker.py

from pageranker import PageRanker
import networkx as nx
import sys

startDate = 0
endDate = float("inf")
weighted = False

ranker = PageRanker('ultimate_sets_clean.csv',
                    'ultimate_player_ids.csv', startDate, endDate, False)

el = ranker.build_edgelist()
g = ranker.build_digraph(el)
pr = ranker.pagerank(g)
pr_sort = ranker.pagerank_sort(pr)
ranker.pagerank_write(pr_sort, 'rank.csv')

print(ranker.leaderboard(20, 'rank.csv'))

print("Number of edges:")
print(g.size())
print("Number of nodes:")
print(g.order())
print("Number of weakly connected components")
print(nx.number_weakly_connected_components(g))