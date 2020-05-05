from pageranker import PageRanker
import networkx as nx
import sys

ranker = PageRanker('ultimate_sets_clean.csv',
                    'ultimate_player_ids.csv')

el_w = ranker.build_edgelist_weighted()
g_w = ranker.build_digraph(el_w)
pr_w = ranker.pagerank(g_w)
pr_sort_w = ranker.pagerank_sort(pr_w)
ranker.pagerank_write_weighted(pr_sort_w)

print(ranker.leaderboard_weighted(20))

print("Number of edges:")
print(g_w.size())
print("Number of nodes:")
print(g_w.order())
print("Number of weakly connected components")
print(nx.number_weakly_connected_components(g_w))